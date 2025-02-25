from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from datetime import datetime
from types import SimpleNamespace

import pytest

from zospy.analyses.base import AnalysisMetadata
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.systemviewers import CrossSection, NSC3DLayout, NSCShadedModel, ShadedModel, Viewer3D
from zospy.analyses.systemviewers.base import SystemViewerWrapper


def assert_systemviewer_result(result, minimal_version):
    """Makes sure systemviewer results is correctly asserted for different versions of OpticStudio."""
    if minimal_version >= "24.1.0":
        assert result.data is not None
    else:  # No result.data as layout exports are not supported
        assert result.data is None


class TestBase:
    @analysis_settings
    class MockSystemViewerSettings:
        number: int = 5

    class MockSystemViewer(SystemViewerWrapper[MockSystemViewerSettings]):
        def __init__(self, *, number: int = 5, settings: TestBase.MockSystemViewerSettings | None = None):
            super().__init__(locals())

        def _create_analysis(self, *, settings_first=True):  # noqa: ARG002
            self._analysis = SimpleNamespace(
                metadata=AnalysisMetadata(DateTime=datetime.now(), LensFile="", LensTitle="", FeatureDescription=""),
                header_data=None,
                messages=[],
                Close=lambda: None,
            )

        def _do_nothing(self):
            pass

        def configure_layout_tool(self):
            pass

        def run_analysis(self) -> None:
            return None

    @pytest.mark.parametrize(
        "filename,expectation",
        [
            ("test.bmp", does_not_raise()),
            ("test.jpeg", does_not_raise()),
            ("test.png", does_not_raise()),
            ("test.jpg", pytest.raises(ValueError, match="Image file must have one of the following extensions:")),
            ("test.tiff", pytest.raises(ValueError, match="Image file must have one of the following extensions:")),
        ],
    )
    def test_validate_path(self, filename, expectation, tmp_path):
        viewer = TestBase.MockSystemViewer()

        with expectation:
            result = viewer._validate_path(tmp_path / filename)  # noqa: SLF001
            assert result == str(tmp_path / filename)

    @pytest.mark.parametrize(
        "wavelength,expected,expectation",
        [
            (1, 1, does_not_raise()),
            (4, 4, does_not_raise()),
            (-1, -1, does_not_raise()),
            ("All", -1, does_not_raise()),
            ("a", None, pytest.raises(ValueError, match="wavelength must be an integer or 'All'")),
            (0.55, None, pytest.raises(TypeError, match="wavelength must be an integer or 'All'")),
            (
                -2,
                None,
                pytest.raises(ValueError, match="wavelength must be -1 or between 1 and the number of wavelengths"),
            ),
            (
                -0,
                None,
                pytest.raises(ValueError, match="wavelength must be -1 or between 1 and the number of wavelengths"),
            ),
            (
                5,
                None,
                pytest.raises(ValueError, match="wavelength must be -1 or between 1 and the number of wavelengths"),
            ),
        ],
    )
    def test_validate_wavelength(self, wavelength, expected, expectation, simple_system):
        while simple_system.SystemData.Wavelengths.NumberOfWavelengths < 4:
            simple_system.SystemData.Wavelengths.AddWavelength(0.555, 1)

        viewer = TestBase.MockSystemViewer()
        viewer.run(simple_system)

        with expectation:
            result = viewer._validate_wavelength(wavelength)  # noqa: SLF001
            assert result == expected

    @pytest.mark.parametrize(
        "field,expected,expectation",
        [
            (1, 1, does_not_raise()),
            (4, 4, does_not_raise()),
            (-1, -1, does_not_raise()),
            ("All", -1, does_not_raise()),
            ("a", None, pytest.raises(ValueError, match="field must be an integer or 'All'")),
            (0.55, None, pytest.raises(TypeError, match="field must be an integer or 'All'")),
            (
                -2,
                None,
                pytest.raises(ValueError, match="field must be -1 or between 1 and the number of fields"),
            ),
            (0, None, pytest.raises(ValueError, match="field must be -1 or between 1 and the number of fields")),
            (
                5,
                None,
                pytest.raises(ValueError, match="field must be -1 or between 1 and the number of fields"),
            ),
        ],
    )
    def test_validate_field(self, field, expected, expectation, simple_system):
        while simple_system.SystemData.Fields.NumberOfFields < 4:
            simple_system.SystemData.Fields.AddField(1, 1, 1)

        viewer = TestBase.MockSystemViewer()
        viewer.run(simple_system)

        with expectation:
            result = viewer._validate_field(field)  # noqa: SLF001
            assert result == expected

    @pytest.mark.parametrize(
        "start_surface,end_surface,expected,expectation",
        [
            (1, 2, 2, does_not_raise()),
            (1, -1, 4, does_not_raise()),
            (
                1,
                5,
                None,
                pytest.raises(
                    ValueError,
                    match="end_surface must be -1 or greater than start_surface and less than the number of surfaces",
                ),
            ),
            (
                3,
                1,
                None,
                pytest.raises(
                    ValueError,
                    match="end_surface must be -1 or greater than start_surface and less than the number of surfaces",
                ),
            ),
        ],
    )
    def test_validate_end_surface(self, start_surface, end_surface, expected, expectation, simple_system):
        viewer = TestBase.MockSystemViewer()
        viewer.run(simple_system)

        with expectation:
            result = viewer._validate_end_surface(start_surface, end_surface)  # noqa: SLF001
            assert result == expected

    @pytest.mark.skip_for_opticstudio_versions(">=24.1.0", "Settings are supported from OpticStudio 24R1")
    def test_warn_ignored_settings(self, simple_system):
        viewer = TestBase.MockSystemViewer(number=6)

        with pytest.warns(UserWarning, match="Some parameters were specified but ignored"):
            viewer.run(simple_system)


class TestCrossSection:
    def test_can_run(self, simple_system, optic_studio_version):
        result = CrossSection().run(simple_system)
        assert_systemviewer_result(result, optic_studio_version)

    def test_to_json(self, simple_system):
        result = CrossSection().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestViewer3D:
    def test_can_run(self, simple_system, optic_studio_version):
        result = Viewer3D().run(simple_system)
        assert_systemviewer_result(result, optic_studio_version)

    def test_to_json(self, simple_system):
        result = Viewer3D().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestShadedModel:
    def test_can_run(self, simple_system, optic_studio_version):
        result = ShadedModel().run(simple_system)
        assert_systemviewer_result(result, optic_studio_version)

    def test_to_json(self, simple_system):
        result = ShadedModel().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestNSC3DLayout:
    def test_can_run(self, nsc_simple_system, optic_studio_version):
        result = NSC3DLayout().run(nsc_simple_system)
        assert_systemviewer_result(result, optic_studio_version)

    def test_to_json(self, nsc_simple_system):
        result = NSC3DLayout().run(nsc_simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestNSCShadedModel:
    def test_can_run(self, nsc_simple_system, optic_studio_version):
        result = NSCShadedModel().run(nsc_simple_system)
        assert_systemviewer_result(result, optic_studio_version)

    def test_to_json(self, nsc_simple_system):
        result = NSCShadedModel().run(nsc_simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
