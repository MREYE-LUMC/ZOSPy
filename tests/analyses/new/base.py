import inspect
from dataclasses import fields
from types import SimpleNamespace

import pytest
from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo

from zospy import constants
from zospy.analyses.new.base import AnalysisData, AnalysisWrapper

analysis_wrapper_classes = AnalysisWrapper.__subclasses__()


@dataclass
class MockAnalysisData:
    int_data: int = 1
    string_data: str = "a"


@dataclass
class MockAnalysisSettings:
    int_setting: int = 1
    string_setting: str = "a"


class MockAnalysis(AnalysisWrapper[MockAnalysisData, MockAnalysisSettings]):
    TYPE = "MockAnalysis"

    _needs_config_file = False
    _needs_text_output_file = False

    def __init__(self, int_setting: int = 1, string_setting: str = "a", block_remove_temp_files: bool = False):
        super().__init__(MockAnalysisSettings(), locals())

        self.block_remove_temp_files = block_remove_temp_files

    def _create_analysis(self):
        self._analysis = SimpleNamespace(metadata=None, header_data=None, messages=[], Close=lambda: None)

    def run_analysis(self, *args, **kwargs) -> AnalysisData:
        if self.block_remove_temp_files:
            self._remove_config_file = False
            self._remove_text_output_file = False

        return MockAnalysisData()


MockOpticStudioSystem = type("OpticStudioSystem", tuple(), {})


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

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_analyses_correct_analysis_name(self, cls):
        assert cls.TYPE is not None
        assert hasattr(constants.Analysis.AnalysisIDM, cls.TYPE)

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_init_contains_all_settings(self, cls):
        init_signature = inspect.signature(cls.__init__)
        settings_fields = fields(cls().settings)

        assert all(field.name in init_signature.parameters for field in settings_fields)

    @pytest.mark.parametrize("cls", analysis_wrapper_classes)
    def test_analyses_default_values(self, cls):
        settings_defaults = self.get_settings_defaults(type(cls().settings))
        init_signature = inspect.signature(cls.__init__)

        for field_name, default_value in settings_defaults.items():
            assert field_name in init_signature.parameters
            assert init_signature.parameters[field_name].default == default_value

    @pytest.mark.parametrize(
        "temp_file_type,filename",
        [
            ("text_output_file", "test.txt"),
            ("text_output_file", None),
            ("config_file", "test.CFG"),
            ("config_file", None),
        ],
    )
    def test_create_text_output_file(self, temp_file_type, filename, tmp_path, monkeypatch):
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
    def test_text_output_file_wrong_filename(self, temp_file_type, tmp_path, filename, monkeypatch):
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
    def test_remove_text_output_file(self, temp_file_type, filename, tmp_path, monkeypatch):
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
