from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
import traceback
from argparse import ArgumentParser
from operator import attrgetter
from pathlib import Path
from typing import Annotated, Any, Callable, Literal

import systems
import yaml
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError

import zospy as zp
from zospy.analyses.base import BaseAnalysisWrapper  # noqa: TCH001

logger = logging.getLogger("generate_test_reference_data")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


TestParameters = dict[str, Any]


class VersionDependentParameters(BaseModel):
    opticstudio: str
    parameters: TestParameters = {}


class TestConfiguration(BaseModel):
    model: Callable[[zp.zpcore.OpticStudioSystem], zp.zpcore.OpticStudioSystem]
    analysis: type[BaseAnalysisWrapper]
    file: str
    test: str
    parameters: list[VersionDependentParameters | TestParameters] = [{}]
    parametrized: tuple[str, ...] | None = None

    @field_validator("analysis", mode="before")
    @classmethod
    def validate_analysis(cls, v: str):
        return attrgetter(v)(zp.analyses)

    @field_validator("model", mode="before")
    @classmethod
    def validate_model(cls, v: str):
        return getattr(systems, v)

    @field_validator("file")
    @classmethod
    def validate_filename(cls, v: str):
        assert v.startswith("test"), "file should start with 'test_'"
        assert v.endswith(".py"), "file should have extension '.py'"

        return v

    @field_validator("test")
    @classmethod
    def validate_testname(cls, v: str):
        assert v.startswith("test"), "test name should start with 'test_'"

        return v

    @model_validator(mode="after")
    @classmethod
    def validate_parametrized(cls, values: TestConfiguration):
        if len(parameters := values.parameters) > 1:
            parametrized = values.parametrized
            assert parametrized is not None, "Multiple sets of parameters are only allowed if parametrized is specified"

            for p in parameters:
                params = p.parameters if isinstance(p, VersionDependentParameters) else p

                if not all(p in params for p in parametrized):
                    raise PydanticCustomError(
                        error_type="invalid_parameters",
                        message_template=(
                            "All sets of parameters should contain the same keys as parametrized. Allowed keys: "
                            "{parametrized}, found keys: {params}"
                        ),
                        context={"parametrized": parametrized, "params": params.keys()},
                    )

        return values


class Configuration(BaseModel):
    redact_patterns: list[Annotated[re.Pattern, BeforeValidator(Configuration.validate_redact_patterns)]] = []
    tests: list[TestConfiguration]

    @staticmethod
    def validate_redact_patterns(v):
        regex = re.compile(v, re.MULTILINE | re.IGNORECASE)

        assert regex.groups == 0, (
            "Redaction patterns are not allowed to contain capturing groups. Use non-capturing "
            "groups (?:<characters>) instead."
        )

        return regex


AbsolutePath = Annotated[Path, AfterValidator(lambda p: p.resolve(strict=False))]


class CommandLineArguments(BaseModel):
    config: AbsolutePath
    connection_mode: Literal["standalone", "extension"]
    opticstudio_directory: AbsolutePath | None
    output_directory: Path


def _redact_json(json_string: str, patterns: list[re.Pattern]) -> tuple[str, list[str]]:
    matches = []

    for p in patterns:
        matches.extend(re.findall(p, json_string))
        json_string = re.sub(p, "REDACTED", json_string)

    return json_string, matches


def _map_parameter_names(parameters: TestParameters):
    """A function to create and apply a mapping for test parameters of the dict type to have consistent test naming.

    Mappings will be saved in 'dictionary_parameter_mapping.json' within the output directory.

    Parameters
    ----------
    parameters : dict
        A dictionary containing the test parameters in the form {param_name: param_value}.

    Returns
    -------
    dict
        A mapped parameters dictionary
    """
    if any(isinstance(value, dict) for value in parameters.values()):
        mapped_parameters = parameters.copy()

        for param_name, param in mapped_parameters.items():
            if isinstance(param, dict):
                mapped_name = hashlib.md5(json.dumps(param, sort_keys=True).encode("utf-8")).hexdigest()  # noqa: S324

                mapped_parameters[param_name] = mapped_name

        return mapped_parameters

    return parameters


def process_test(
    oss: zp.zpcore.OpticStudioSystem, test: TestConfiguration, args: CommandLineArguments, config: Configuration
):
    analysis = test.analysis
    test_file = test.file
    test_name = test.test

    test_parameters = test.parameters
    parametrized = test.parametrized

    optic_studio_version = str(oss.ZOS.version)

    for parameters in test_parameters:
        result_file_name = f"{optic_studio_version}-{test_file}-{test_name}"

        if isinstance(parameters, VersionDependentParameters):
            if not oss.ZOS.version.match(parameters.opticstudio):
                logger.info(f"Skipping {result_file_name} because it requires OpticStudio {parameters.opticstudio}")
                continue

            parameters = parameters.parameters  # noqa: PLW2901

        if parametrized:
            mapped_parameters = _map_parameter_names(parameters=parameters)

            result_file_name += f"[{'-'.join(str(mapped_parameters[p]) for p in parametrized)}]"

        output_json = args.output_directory / f"{result_file_name}.json"
        output_zos = args.output_directory / f"{result_file_name}.zmx"

        if output_json.exists():
            logger.info(f"Skipping {result_file_name} because it already exists")
            continue

        logger.info(f"Processing {result_file_name}")

        # Build model
        test.model(oss)

        try:
            # Run analysis
            result = analysis(**parameters).run(oss, oncomplete="Release")
        except Exception:
            logger.exception("Failed to run analysis %s. Traceback: %s", analysis.__name__, traceback.format_exc())
            continue

        try:
            result_json = result.to_json()
            result_json, redacted_strings = _redact_json(result_json, config.redact_patterns)

            if redacted_strings:
                logger.warning("\tRedacted strings: %s", "\n\t".join(redacted_strings))

            with open(output_json, "w", encoding="utf-8") as f:
                f.write(result_json)

            try:
                oss.save_as(str(output_zos.resolve()))
            except Exception:
                logger.exception("Failed to save Zemax file %s. Traceback: %s", output_zos, traceback.format_exc())
                output_zos.with_suffix(".txt").resolve().write_text("Failed to save OpticStudio model.")

                # Reconnect to OpticStudio to avoid potential issues
                zos = zp.ZOS(opticstudio_directory=args.opticstudio_directory)
                oss = zos.connect(mode=args.connection_mode)

        except TypeError:
            logger.exception("Failed to serialize %s. Traceback: %s", result_file_name, traceback.format_exc())


def main(args):
    args = CommandLineArguments.model_validate(args, from_attributes=True)

    if not args.config.exists():
        logger.fatal(
            f"Configuration file {args.config} does not exist. When running with the default arguments, "
            f"make sure you are running the script from the project root."
        )

        return 1

    if not args.output_directory.exists():
        logger.fatal(
            f"Output directory {args.output_directory} does not exist. When running with the default "
            f"arguments, make sure you are running the script from the project root."
        )

        return 1

    with open(args.config) as f:
        config = Configuration.model_validate(yaml.safe_load(f.read()))

    zos = zp.ZOS(opticstudio_directory=args.opticstudio_directory)
    oss = zos.connect(mode=args.connection_mode)

    if args.connection_mode == "extension":
        # Turn off UI updates for faster processing
        zos.Application.ShowChangesInUI = False

    logger.info(f"Generating test data files using OpticStudio {zos.version} and ZOSPy {zp.__version__}")

    for t in config.tests:
        process_test(oss, t, args, config)

    # Clean up Zemax workspace files
    logger.info("Removing Zemax workspace (.ZDA) files...")
    for f in args.output_directory.glob("*.ZDA"):
        f.unlink()

    return 0


argument_parser = ArgumentParser(description="Generate reference data files for ZOSPy unit tests.")
argument_parser.add_argument(
    "--config",
    type=Path,
    default=Path("scripts/generate_test_reference_data/tests.yaml"),
    help="Path to the configuration file.",
)
argument_parser.add_argument(
    "--connection-mode",
    choices=["standalone", "extension"],
    default="standalone",
    help="Connection mode to use with OpticStudio.",
)
argument_parser.add_argument(
    "--output-directory",
    type=Path,
    default=Path("tests/data/reference"),
    help="Path to the directory where the reference data files will be saved.",
)
argument_parser.add_argument(
    "--opticstudio-directory",
    type=Path,
    help="Path to the OpticStudio installation directory. This allows to choose a different version of OpticStudio.",
    required=False,
)

sys.exit(main(argument_parser.parse_args()))
