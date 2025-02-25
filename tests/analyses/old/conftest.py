import pytest

from tests.config import REFERENCE_DATA_FOLDER, REFERENCE_VERSION
from zospy.analyses.old.base import AnalysisResult


@pytest.fixture
def expected_data(request, optic_studio_version) -> AnalysisResult:
    filename = f"{optic_studio_version}-{request.fspath.basename}-{request.node.name}"

    data_file = request.config.rootpath / REFERENCE_DATA_FOLDER / "old" / f"{filename}.json"

    if not data_file.exists():
        pytest.skip(f"Data file {data_file} does not exist")

    with open(data_file) as f:
        return AnalysisResult.from_json(f.read())


@pytest.fixture
def reference_data(request) -> AnalysisResult:
    filename = f"{REFERENCE_VERSION}-{request.fspath.basename}-{request.node.name}"
    filename = filename.replace("matches_reference_data", "returns_correct_result")

    data_file = request.config.rootpath / REFERENCE_DATA_FOLDER / "old" / f"{filename}.json"

    if not data_file.exists():
        pytest.skip(f"Data file {data_file} does not exist")

    with open(data_file) as f:
        return AnalysisResult.from_json(f.read())
