import hashlib
import json
from pathlib import Path

import pytest

from tests.config import CONFIG_DATA_FOLDER, REFERENCE_DATA_FOLDER, REFERENCE_VERSION
from zospy.analyses.base import AnalysisResult, BaseAnalysisWrapper
from zospy.analyses.psf.huygens_psf import BaseHuygensPSF
from zospy.analyses.systemviewers.base import SystemViewerWrapper


def pytest_make_parametrize_id(config, val, argname):  # noqa: ARG001
    """Custom hook to control the name of dictionaries in the description."""
    if isinstance(val, dict):
        return hashlib.md5(json.dumps(val, sort_keys=True).encode("utf-8")).hexdigest()

    # Default ID for non-dictionary parameters
    return None


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

    return AnalysisResult.from_json(data_file.read_text(encoding="utf-8"))


@pytest.fixture
def reference_data(request) -> AnalysisResult:
    filename = f"{REFERENCE_VERSION}-{request.fspath.basename}-{request.node.name}"
    filename = filename.replace("matches_reference_data", "returns_correct_result")

    data_file = request.config.rootpath / REFERENCE_DATA_FOLDER / f"{filename}.json"

    if not data_file.exists():
        pytest.skip(f"Data file {data_file} does not exist")

    return AnalysisResult.from_json(data_file.read_text(encoding="utf-8"))


def _all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in _all_subclasses(c)])


_analysis_wrapper_classes = [
    c for c in _all_subclasses(BaseAnalysisWrapper) if c not in {BaseHuygensPSF, SystemViewerWrapper}
]


@pytest.fixture(scope="module", params=_analysis_wrapper_classes)
def analysis_wrapper_class(request):
    return request.param
