from __future__ import annotations

import inspect
import json
from dataclasses import fields
from datetime import datetime
from types import SimpleNamespace

import numpy as np
import pytest
from pandas import DataFrame
from pydantic import Field
from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo

from zospy import constants
from zospy.analyses.new.base import (
    AnalysisData,
    AnalysisMetadata,
    AnalysisResult,
    AnalysisSettings,
    BaseAnalysisWrapper,
)
from zospy.analyses.new.decorators import analysis_settings
from zospy.analyses.new.parsers.types import ValidatedDataFrame
from zospy.analyses.new.reports.surface_data import SurfaceDataSettings
from zospy.analyses.new.systemviewers.base import SystemViewerWrapper


def all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])


analysis_wrapper_classes = all_subclasses(BaseAnalysisWrapper)
analysis_wrapper_classes.remove(SystemViewerWrapper)


@dataclass
class MockAnalysisData:
    int_data: int = 1
    string_data: str = "a"


@analysis_settings
class MockAnalysisSettings:
    int_setting: int = Field(default=1, description="An integer setting")
    string_setting: str = Field(default="a", description="A string setting")


class MockAnalysis(BaseAnalysisWrapper[MockAnalysisData, MockAnalysisSettings]):
    TYPE = "MockAnalysis"

    _needs_config_file = False
    _needs_text_output_file = False

    def __init__(
        self,
        *,
        int_setting: int = 1,
        string_setting: str = "a",
        block_remove_temp_files: bool = False,
    ):
        super().__init__(settings_kws=locals())

        self.block_remove_temp_files = block_remove_temp_files

    def _create_analysis(self):
        self._analysis = SimpleNamespace(
            metadata=AnalysisMetadata(DateTime=datetime.now(), LensFile="", LensTitle="", FeatureDescription=""),
            header_data=None,
            messages=[],
            Close=lambda: None,
        )

    def run_analysis(self) -> AnalysisData:
        if self.block_remove_temp_files:
            self._remove_config_file = False
            self._remove_text_output_file = False

        return MockAnalysisData()


MockOpticStudioSystem = type("OpticStudioSystem", (), {})


class TestAnalysisWrapper:
    @staticmethod
    def get_settings_defaults(settings_class):
        result = {}

        for field in fields(settings_class):
            if isinstance(field.default, FieldInfo):
                result[field.name] = field.default.default
            else:
                result[field.name] = field.default

        return result

    def test_get_settings_type(self):
        assert MockAnalysis._settings_type == MockAnalysisSettings  # noqa: SLF001

    def test_settings_type_is_specified(self):
        assert MockAnalysis._settings_type is not AnalysisSettings  # noqa: SLF001

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_analyses_correct_analysis_name(self, cls):
        assert cls.TYPE is not None
        assert hasattr(constants.Analysis.AnalysisIDM, cls.TYPE)

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_init_all_keyword_only_parameters(self, cls):
        all(p.kind.name == "KEYWORD_ONLY" for _, p in inspect.signature(cls).parameters.items())

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_init_contains_all_settings(self, cls):
        if cls().settings is None:
            return

        init_signature = inspect.signature(cls.__init__)
        settings_fields = fields(cls().settings)

        assert all(field.name in init_signature.parameters for field in settings_fields)

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_analyses_default_values(self, cls):
        if cls().settings is None:
            return

        settings_defaults = self.get_settings_defaults(type(cls().settings))
        init_signature = inspect.signature(cls.__init__)

        for field_name, default_value in settings_defaults.items():
            assert field_name in init_signature.parameters
            assert init_signature.parameters[field_name].default == default_value

    def test_change_settings_from_parameters(self):
        analysis = MockAnalysis(int_setting=2, string_setting="b")

        assert analysis.settings.int_setting == 2
        assert analysis.settings.string_setting == "b"

    def test_change_settings_from_object(self):
        settings = MockAnalysisSettings(int_setting=2, string_setting="b")
        analysis = MockAnalysis.from_settings(settings)

        assert analysis.settings.int_setting == 2
        assert analysis.settings.string_setting == "b"

    def test_settings_object_is_copied(self):
        settings = MockAnalysisSettings(int_setting=2, string_setting="b")
        analysis = MockAnalysis.from_settings(settings)

        assert analysis.settings is not settings
        assert analysis.settings == settings

    @pytest.mark.parametrize(
        "temp_file_type,filename",
        [
            ("text_output_file", "test.txt"),
            ("text_output_file", None),
            ("config_file", "test.CFG"),
            ("config_file", None),
        ],
    )
    def test_create_temp_file(self, temp_file_type, filename, tmp_path, monkeypatch):
        analysis = MockAnalysis(block_remove_temp_files=True)
        monkeypatch.setattr(analysis, f"_needs_{temp_file_type}", True)

        if filename:
            path = tmp_path / filename
            path.touch()
        else:
            path = None

        analysis.run(oss=MockOpticStudioSystem(), **{temp_file_type: path})

        if filename:
            assert getattr(analysis, temp_file_type) == path

        assert getattr(analysis, temp_file_type).exists()
        assert getattr(analysis, temp_file_type).is_file()

    @pytest.mark.parametrize(
        "temp_file_type,filename",
        [
            ("text_output_file", "test.ABC"),
            ("text_output_file", "test.TXT"),
            ("config_file", "test.ABC"),
            ("config_file", "test.cfg"),
        ],
    )
    def test_temp_file_wrong_filename(self, temp_file_type, tmp_path, filename, monkeypatch):
        analysis = MockAnalysis()
        monkeypatch.setattr(analysis, f"_needs_{temp_file_type}", True)

        with pytest.raises(ValueError, match="File path should end with ."):
            analysis.run(oss=MockOpticStudioSystem(), **{temp_file_type: tmp_path / filename})

    @pytest.mark.parametrize(
        "temp_file_type,filename",
        [
            ("text_output_file", "test.txt"),
            ("text_output_file", None),
            ("config_file", "test.CFG"),
            ("config_file", None),
        ],
    )
    def test_remove_temp_file(self, temp_file_type, filename, tmp_path, monkeypatch):
        analysis = MockAnalysis()
        monkeypatch.setattr(analysis, f"_needs_{temp_file_type}", True)

        if filename:
            path = tmp_path / filename
            path.touch()
        else:
            path = None

        analysis.run(oss=MockOpticStudioSystem(), **{temp_file_type: path})

        if path:
            assert path.exists()
        else:
            assert not getattr(analysis, temp_file_type).exists()


class TestAnalysisResultJSONConversion:
    settings = SurfaceDataSettings()

    # Only test for non-dataclass results, because dataclass results are tested separately in the corresponding
    # analysis' tests.
    @pytest.mark.parametrize(
        "result_type,result_value,type_info",
        [
            (DataFrame, DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}), {"data_type": "dataframe"}),
            (np.ndarray, np.array([1, 2, 3]), {"data_type": "ndarray"}),
        ],
    )
    def test_data_to_json(self, result_type, result_value, type_info):
        result = AnalysisResult[result_type, MockAnalysisSettings](
            data=result_value,
            settings=MockAnalysisSettings(),
            metadata=AnalysisMetadata(datetime.now(), "", "", ""),
            header=None,
            messages=None,
        )

        result_json = result.to_json()
        result_dict = json.loads(result_json)

        assert "__analysis_data__" in result_dict
        assert result_dict["__analysis_data__"] == type_info

    def test_settings_to_json(self):
        result = AnalysisResult[ValidatedDataFrame, MockAnalysisSettings](
            data=DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}),
            settings=MockAnalysisSettings(),
            metadata=AnalysisMetadata(datetime.now(), "", "", ""),
            header=None,
            messages=None,
        )

        result_json = result.to_json()
        result_dict = json.loads(result_json)

        assert "__analysis_settings__" in result_dict
        assert result_dict["__analysis_settings__"] == {
            "data_type": "dataclass",
            "name": "MockAnalysisSettings",
            "module": "tests.analyses.new.test_base",
        }

    @pytest.mark.parametrize(
        "result_type,result_value",
        [
            (ValidatedDataFrame, DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})),
            (np.ndarray, np.array([1, 2, 3])),
        ],
    )
    def test_roundtrip(self, result_type, result_value):
        result = AnalysisResult[result_type, MockAnalysisSettings](
            data=result_value,
            settings=self.settings,
            metadata=AnalysisMetadata(datetime.now(), "", "", ""),
            header=None,
            messages=None,
        )

        result_json = result.to_json()

        result_roundtrip = AnalysisResult.from_json(result_json)
        assert all(result_roundtrip.data == result.data)
        assert result_roundtrip.settings == result.settings
        assert result_roundtrip.metadata == result.metadata
        assert result_roundtrip.header == result.header
        assert result_roundtrip.messages == result.messages
