from __future__ import annotations

import os
import re
import traceback
from operator import attrgetter
from pathlib import Path
from typing import Any, Callable, Literal

import yaml
from pydantic import BaseModel, root_validator, validator

import zospy as zp
from scripts.generate_test_reference_data import systems

CONFIG_FILE = "tests.yaml"
OPTIC_STUDIO_VERSION: str
OUTPUT_DIRECTORY: Path = Path("test_output")


class TestConfiguration(BaseModel):
    model: Callable[[zp.zpcore.OpticStudioSystem], zp.zpcore.OpticStudioSystem]
    analysis: Callable[[zp.zpcore.OpticStudioSystem, ...], zp.analyses.base.AnalysisResult]
    file: str
    test: str
    parameters: list[dict[str, Any]] = [{}]
    parametrized: tuple[str, ...] | None = None

    @validator("analysis", pre=True)
    def validate_analysis(cls, v: str):
        return attrgetter(v)(zp.analyses)

    @validator("model", pre=True)
    def validate_model(cls, v: str):
        return getattr(systems, v)

    @validator("file")
    def validate_filename(cls, v: str):
        assert v.startswith("test") and v.endswith(".py"), "file should start with 'test_' and have extension '.py'"

        return v

    @validator("test")
    def validate_testname(cls, v: str):
        assert v.startswith("test"), "test name should start with 'test_'"

        return v

    @root_validator
    def validate_parametrized(cls, values):
        if len(parameters := values.get("parameters")) > 1:
            parametrized = values.get("parametrized")
            assert parametrized is not None, "Multiple sets of parameters are only allowed if parametrized is specified"
            assert all(p in parameters[0].keys() for p in parametrized), "Invalid values encountered in parametrized"

        return values


class Configuration(BaseModel):
    connection_mode: Literal["standalone", "extension"]
    output_directory: Path
    redact_patterns: list[re.Pattern] = []
    tests: list[TestConfiguration]

    @validator("redact_patterns", pre=True, each_item=True)
    def validate_redact_patterns(cls, v):
        regex = re.compile(v, re.MULTILINE | re.IGNORECASE)

        assert regex.groups == 0, (
            "Redaction patterns are not allowed to contain capturing groups. Use non-capturing "
            "groups (?:<characters>) instead."
        )

        return regex


def _optic_studio_version(zos: zp.zpcore.ZOS) -> str:
    application = zos.Application

    version = f"{application.ZOSMajorVersion}.{application.ZOSMinorVersion}.{application.ZOSSPVersion}"

    return version


def _redact_json(json_string: str, patterns: list[re.Pattern]) -> tuple[str, list[str]]:
    matches = []

    for p in patterns:
        matches.extend(re.findall(p, json_string))
        json_string = re.sub(p, "REDACTED", json_string)

    return json_string, matches


def process_test(oss: zp.zpcore.OpticStudioSystem, test: TestConfiguration, config: Configuration):
    analysis = test.analysis
    test_file = test.file
    test_name = test.test

    test_parameters = test.parameters
    parametrized = test.parametrized

    for parameters in test_parameters:
        result_file_name = f"{OPTIC_STUDIO_VERSION}-{test_file}-{test_name}"

        if parametrized:
            result_file_name += f"[{'-'.join(str(parameters[p]) for p in parametrized)}]"

        output_json = config.output_directory / f"{result_file_name}.json"
        output_zos = config.output_directory / f"{result_file_name}.zos"

        if output_json.exists():
            print(f"Skipping {result_file_name} because it already exists")
            continue

        print(f"Processing {result_file_name}")

        # Build model
        test.model(oss)

        result = analysis(oss, **parameters, oncomplete="Release")

        try:
            result_json = result.to_json()
            result_json, redacted_strings = _redact_json(result_json, config.redact_patterns)

            if redacted_strings:
                print("\tRedacted strings:", *redacted_strings, sep="\n\t\t")

            with open(output_json, "w") as f:
                f.write(result_json)
        except TypeError as e:
            print(f"Failed to serialize {result_file_name}", traceback.format_exc())

        oss.save_as(str(output_zos.absolute()))


os.chdir(Path(__file__).parent)

with open(CONFIG_FILE, "r") as f:
    config: Configuration = Configuration.parse_obj(yaml.safe_load(f.read()))

zos = zp.ZOS()
zos.wakeup()

if config.connection_mode == "extension":
    assert zos.connect_as_extension(), "Failed to connect to Zemax in extension mode"
elif config.connection_mode == "standalone":
    assert zos.create_new_application(), "Failed to connect to Zemax in standalone mode"

OPTIC_STUDIO_VERSION = _optic_studio_version(zos)

oss = zos.get_primary_system()

for t in config.tests:
    process_test(oss, t, config)

re.compile(r"(?:[a-zA-Z]:|(?:\\\\)+[\w\s\.]+\\[\w\s\.$]+)\\+(?:[\w\s\.]+\\+)*[\w\s.]*?$")
re.compile(r"[a-z]:(\\\\[\w\s.]+)+")
