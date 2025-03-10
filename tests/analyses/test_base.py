from __future__ import annotations

import inspect
import json
from contextlib import nullcontext as does_not_raise
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
from zospy.analyses.base import (
    AnalysisData,
    AnalysisMetadata,
    AnalysisResult,
    AnalysisSettings,
    BaseAnalysisWrapper,
    _validated_setter,
    new_analysis,
)
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import ValidatedDataFrame
from zospy.analyses.reports.surface_data import SurfaceDataSettings
from zospy.analyses.systemviewers.base import SystemViewerWrapper


def all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])


analysis_wrapper_classes = all_subclasses(BaseAnalysisWrapper)
analysis_wrapper_classes.remove(SystemViewerWrapper)


class TestValidatedSetter:
    class MockSettings:
        int_setting: int = 1
        string_setting: str = "a"

    def test_get_existing(self):
        settings = _validated_setter(self.MockSettings())

        assert settings.int_setting == self.MockSettings.int_setting

    def test_get_non_existing(self):
        settings = _validated_setter(self.MockSettings())

        with pytest.raises(AttributeError):
            assert settings.non_existing  # type: ignore

    def test_set_existing(self):
        settings = _validated_setter(self.MockSettings())

        settings.int_setting = 2

        assert settings.int_setting == 2

    def test_set_non_existing(self):
        settings = _validated_setter(self.MockSettings())

        with pytest.raises(AttributeError, match="'MockSettings' object has no attribute 'non_existing'"):
            settings.non_existing = 2  # type: ignore


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
        assert all(p.kind.name == "KEYWORD_ONLY" for _, p in inspect.signature(cls).parameters.items())

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
        analysis = MockAnalysis.with_settings(settings)

        assert analysis.settings.int_setting == 2
        assert analysis.settings.string_setting == "b"

    def test_settings_object_is_copied(self):
        settings = MockAnalysisSettings(int_setting=2, string_setting="b")
        analysis = MockAnalysis.with_settings(settings)

        assert analysis.settings is not settings
        assert analysis.settings == settings

    def test_update_settings_object(self):
        analysis = MockAnalysis(int_setting=1, string_setting="a")

        analysis.update_settings(settings=MockAnalysisSettings(int_setting=2, string_setting="b"))

        assert analysis.settings.int_setting == 2
        assert analysis.settings.string_setting == "b"

    def test_update_settings_dictionary(self):
        analysis = MockAnalysis(int_setting=1, string_setting="a")

        analysis.update_settings(settings_kws={"int_setting": 2, "string_setting": "b"})

        assert analysis.settings.int_setting == 2
        assert analysis.settings.string_setting == "b"

    def test_update_settings_object_and_dictionary(self):
        analysis = MockAnalysis(int_setting=1, string_setting="a")

        analysis.update_settings(
            settings=MockAnalysisSettings(int_setting=2, string_setting="a"), settings_kws={"string_setting": "b"}
        )

        assert analysis.settings.int_setting == 2
        assert analysis.settings.string_setting == "b"

    def test_update_settings_no_dataclass_raises_type_error(self):
        with pytest.raises(TypeError, match="settings should be a dataclass"):
            MockAnalysis().update_settings(settings=123)

    @pytest.mark.parametrize(
        "field_specification",
        [
            "All",
            0,
            1,
            2,
            3,
        ],
    )
    def test_get_field(self, simple_system, field_specification):
        for x in (-5, 5):
            simple_system.SystemData.Fields.AddField(x, 0, 1.0)

        analysis = new_analysis(simple_system, constants.Analysis.AnalysisIDM.RayFan, settings_first=True)

        if field_specification in ("All", 0):
            analysis.Settings.Field.UseAllFields()
        else:
            analysis.Settings.Field.SetFieldNumber(field_specification)

        assert analysis.get_field() == ("All" if field_specification == 0 else field_specification)

    @pytest.mark.parametrize(
        "analysis_type,field_specification,expectation",
        [
            ("RayFan", "All", does_not_raise()),
            ("RayFan", 0, does_not_raise()),
            ("RayFan", 1, does_not_raise()),
            ("RayFan", 2, does_not_raise()),
            ("RayFan", 3, does_not_raise()),
            ("RayFan", 1.0, pytest.raises(ValueError, match=r"^Field value should be")),
            ("RayFan", 1.5, pytest.raises(ValueError, match=r"^Field value should be")),
            ("RayFan", "Invalid", pytest.raises(ValueError, match=r"^Field value should be")),
            ("RayFan", None, pytest.raises(ValueError, match=r"^Field value should be")),
            ("WavefrontMap", "All", pytest.raises(ValueError, match=r"^Could not set field value to")),
            ("WavefrontMap", 1, does_not_raise()),
        ],
    )
    def test_set_field(self, simple_system, analysis_type, field_specification, expectation):
        for x in (-5, 5):
            simple_system.SystemData.Fields.AddField(x, 0, 1.0)

        analysis = new_analysis(
            simple_system, getattr(constants.Analysis.AnalysisIDM, analysis_type), settings_first=True
        )

        with expectation:
            analysis.set_field(field_specification)
            assert analysis.Settings.Field.GetFieldNumber() == (
                0 if field_specification == "All" else field_specification
            )

    @pytest.mark.parametrize(
        "wavelength_specification",
        [
            "All",
            0,
            1,
            2,
            3,
        ],
    )
    def test_get_wavelength(self, simple_system, wavelength_specification):
        # Use FdC_Visible to have three wavelengths
        simple_system.SystemData.Wavelengths.SelectWavelengthPreset(constants.SystemData.WavelengthPreset.FdC_Visible)

        analysis = new_analysis(simple_system, constants.Analysis.AnalysisIDM.RayFan, settings_first=True)

        if wavelength_specification in ("All", 0):
            analysis.Settings.Wavelength.UseAllWavelengths()
        else:
            analysis.Settings.Wavelength.SetWavelengthNumber(wavelength_specification)

        assert analysis.get_wavelength() == ("All" if wavelength_specification == 0 else wavelength_specification)

    @pytest.mark.parametrize(
        "analysis_type,wavelength_specification,expectation",
        [
            ("RayFan", "All", does_not_raise()),
            ("RayFan", 0, does_not_raise()),
            ("RayFan", 1, does_not_raise()),
            ("RayFan", 2, does_not_raise()),
            ("RayFan", 3, does_not_raise()),
            ("RayFan", 1.0, pytest.raises(ValueError, match=r"^Wavelength value should be")),
            ("RayFan", 1.5, pytest.raises(ValueError, match=r"^Wavelength value should be")),
            ("RayFan", "Invalid", pytest.raises(ValueError, match=r"^Wavelength value should be")),
            ("RayFan", None, pytest.raises(ValueError, match=r"^Wavelength value should be")),
            ("WavefrontMap", "All", pytest.raises(ValueError, match=r"^Could not set wavelength value to")),
            ("WavefrontMap", 1, does_not_raise()),
        ],
    )
    def test_set_wavelength(self, simple_system, analysis_type, wavelength_specification, expectation):
        simple_system.SystemData.Wavelengths.SelectWavelengthPreset(constants.SystemData.WavelengthPreset.FdC_Visible)

        analysis = new_analysis(
            simple_system, getattr(constants.Analysis.AnalysisIDM, analysis_type), settings_first=True
        )

        with expectation:
            analysis.set_wavelength(wavelength_specification)

            assert analysis.Settings.Wavelength.GetWavelengthNumber() == (
                0 if wavelength_specification == "All" else wavelength_specification
            )

    @pytest.mark.parametrize(
        "analysis_type,surface_specification,expectation",
        [
            ("SurfaceCurvature", 0, does_not_raise()),
            ("SurfaceCurvature", 1, does_not_raise()),
            ("SurfaceCurvature", 2, does_not_raise()),
            ("SurfaceCurvature", "Image", pytest.raises(ValueError, match=r"^Could not set surface value to")),
            ("SurfaceCurvature", "Objective", pytest.raises(ValueError, match=r"^Could not set surface value to")),
            ("SurfaceCurvature", 1.5, pytest.raises(ValueError, match=r"^Surface value should be")),
            ("SurfaceCurvature", "Invalid", pytest.raises(ValueError, match=r"^Surface value should be")),
            ("SurfaceCurvature", None, pytest.raises(ValueError, match=r"^Surface value should be")),
            ("WavefrontMap", 1, does_not_raise()),
            ("WavefrontMap", "Image", does_not_raise()),
            ("WavefrontMap", "Objective", pytest.raises(ValueError, match=r"^Could not set surface value to")),
            # TODO Implement test for Objective that should pass when such a test becomes possible
        ],
    )
    def test_set_surface(self, simple_system, analysis_type, surface_specification, expectation):
        analysis = new_analysis(
            simple_system, getattr(constants.Analysis.AnalysisIDM, analysis_type), settings_first=True
        )

        with expectation:
            analysis.set_surface(surface_specification)
            assert analysis.Settings.Surface.GetSurfaceNumber() == (
                0 if surface_specification == "Image" else surface_specification
            )

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
            "data_type": "zospy_class",
            "name": "MockAnalysisSettings",
            "module": "tests.analyses.test_base",
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
