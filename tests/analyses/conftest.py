from pathlib import Path

import pytest

from tests.config import CONFIG_DATA_FOLDER, REFERENCE_DATA_FOLDER, REFERENCE_VERSION
from zospy.analyses.base import AnalysisResult


@pytest.fixture(scope="class")
def cfg_file(request) -> Path:
    # TODO check if we can programmatically write these files
    filename = f"{request.node.parent.name}-{request.node.name}"
    return request.config.rootpath / CONFIG_DATA_FOLDER / f"{filename}.CFG"


@pytest.fixture
def expected_data(request, optic_studio_version) -> AnalysisResult:
    filename = f"{optic_studio_version}-{request.fspath.basename}-{request.node.name}"

    data_file = request.config.rootpath / REFERENCE_DATA_FOLDER / f"{filename}.json"

    if not data_file.exists():
        pytest.skip(f"Data file {data_file} does not exist")

    with open(data_file, "r") as f:
        return AnalysisResult.from_json(f.read())


@pytest.fixture
def reference_data(request) -> AnalysisResult:
    filename = f"{REFERENCE_VERSION}-{request.fspath.basename}-{request.node.name}"
    filename = filename.replace("matches_reference_data", "returns_correct_result")

    data_file = request.config.rootpath / REFERENCE_DATA_FOLDER / f"{filename}.json"

    if not data_file.exists():
        pytest.skip(f"Data file {data_file} does not exist")

    with open(data_file, "r") as f:
        return AnalysisResult.from_json(f.read())
