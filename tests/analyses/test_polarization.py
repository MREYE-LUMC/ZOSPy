import numpy as np
import pytest

import zospy as zp
from zospy.analyses.polarization import polarization_pupil_map, transmission

BK7_WAVELENGTH = 0.546706
BK7_REFRACTIVE_INDEX = 1.51872


@pytest.fixture
def fabry_perot_system(empty_system: zp.zpcore.OpticStudioSystem):
    """Test system for polarization analyses.

    This system is based on the Fabry-Perot example from Zemax OpticStudio.
    Surface 1 and 2 use hardcoded refractive indices instead of BK7 glass in order
    to ensure consistency between different OpticStudio versions.
    """

    oss = empty_system

    oss.SystemData.Aperture.ApertureType = zp.constants.SystemData.ZemaxApertureType.EntrancePupilDiameter
    oss.SystemData.Aperture.ApertureValue = 5.0
    oss.SystemData.Aperture.FastSemiDiameters = True

    # Set wavelength to 546.706 nm
    oss.SystemData.Wavelengths.GetWavelength(1).Wavelength = BK7_WAVELENGTH

    surface_object = oss.LDE.GetSurfaceAt(0)
    surface_object.SemiDiameter = np.inf

    surface_stop = oss.LDE.GetSurfaceAt(1)
    surface_stop.Thickness = 2.0
    zp.solvers.material_model(surface_stop.MaterialCell, refractive_index=BK7_REFRACTIVE_INDEX)
    surface_stop.SemiDiameter = 3.0

    surface_coating = oss.LDE.InsertNewSurfaceAt(2)
    surface_coating.Thickness = 2.0
    zp.solvers.material_model(surface_coating.MaterialCell, refractive_index=BK7_REFRACTIVE_INDEX)
    surface_coating.Coating = "FP"
    surface_coating.SemiDiameter = 3.0

    surface_aperture = oss.LDE.InsertNewSurfaceAt(3)
    surface_aperture.Thickness = 5.0
    surface_aperture.SemiDiameter = 3.0

    surface_paraxial = oss.LDE.InsertNewSurfaceAt(4)
    zp.functions.lde.surface_change_type(surface_paraxial, zp.constants.Editors.LDE.SurfaceType.Paraxial)
    surface_paraxial.Thickness = 19.0

    # Focal length
    surface_paraxial.GetCellAt(12).DoubleValue = 20.0

    # OPD Mode
    surface_paraxial.GetCellAt(13).IntegerValue = 1

    surface_image = oss.LDE.GetSurfaceAt(5)

    return oss


class TestPolarizationPupilMap:
    def test_can_run_polarization_pupil_map(self, polarized_system):
        result = polarization_pupil_map(polarized_system)

        assert result.Data is not None

    @pytest.mark.parametrize(
        "jx,jy,x_phase,y_phase,surface,sampling",
        [
            (1, 0, 0, 0, "Image", "11x11"),
            (1, 1, 0, 0, 2, "11x11"),
            (0, 1, 0, 0, "Image", "11x11"),
            (1, 1, 45, 90, "Image", "17x17"),
        ],
    )
    def test_polarization_pupil_map_returns_correct_result(
        self, polarized_system, jx, jy, x_phase, y_phase, surface, sampling, expected_data
    ):
        result = polarization_pupil_map(polarized_system, jx, jy, x_phase, y_phase, surface=surface, sampling=sampling)

        assert result.Data.Transmission == expected_data.Data.Transmission
        assert np.allclose(result.Data.Table, expected_data.Data.Table)

    @pytest.mark.parametrize(
        "jx,jy,x_phase,y_phase,surface,sampling",
        [
            (1, 0, 0, 0, "Image", "11x11"),
            (1, 1, 0, 0, 2, "11x11"),
            (0, 1, 0, 0, "Image", "11x11"),
            (1, 1, 45, 90, "Image", "17x17"),
        ],
    )
    def test_polarization_pupil_map_matches_reference_data(
        self, polarized_system, jx, jy, x_phase, y_phase, surface, sampling, reference_data
    ):
        result = polarization_pupil_map(polarized_system, jx, jy, x_phase, y_phase, surface=surface, sampling=sampling)

        assert result.Data.Transmission == reference_data.Data.Transmission
        assert np.allclose(result.Data.Table, reference_data.Data.Table)


class TestTransmission:
    def test_can_run_transmission(self, polarized_system):
        result = transmission(polarized_system)

        assert result.Data is not None

    @pytest.mark.parametrize(
        "sampling,unpolarized,jx,jy,x_phase,y_phase",
        [
            ("32x32", False, 1, 0, 0, 0),
            ("32x32", False, 0, 1, 0, 0),
            ("32x32", False, 1, 1, 0, 0),
            ("64x64", False, 1, 1, 45, 90),
            ("64x64", True, 1, 0, 0, 0),
        ],
    )
    def test_transmission_returns_correct_result(
        self, polarized_system, sampling, unpolarized, jx, jy, x_phase, y_phase, expected_data
    ):
        result = transmission(polarized_system, sampling, unpolarized, jx, jy, x_phase, y_phase)

        assert result.Data.FieldPos == expected_data.Data.FieldPos
        assert result.Data.Wavelength == expected_data.Data.Wavelength
        assert result.Data.TotalTransmission == expected_data.Data.TotalTransmission
        assert np.allclose(result.Data.Table, expected_data.Data.Table)

    @pytest.mark.parametrize(
        "sampling,unpolarized,jx,jy,x_phase,y_phase",
        [
            ("32x32", False, 1, 0, 0, 0),
            ("32x32", False, 0, 1, 0, 0),
            ("32x32", False, 1, 1, 0, 0),
            ("64x64", False, 1, 1, 45, 90),
            ("64x64", True, 1, 0, 0, 0),
        ],
    )
    def test_transmission_matches_reference_data(
        self, polarized_system, sampling, unpolarized, jx, jy, x_phase, y_phase, reference_data
    ):
        result = transmission(polarized_system, sampling, unpolarized, jx, jy, x_phase, y_phase)

        assert result.Data.FieldPos == reference_data.Data.FieldPos
        assert result.Data.Wavelength == reference_data.Data.Wavelength
        assert result.Data.TotalTransmission == reference_data.Data.TotalTransmission
        assert np.allclose(result.Data.Table, reference_data.Data.Table)

    def test_transmission_multiple_fields_raises_notimplementederror(self, simple_system):
        simple_system.SystemData.Fields.AddField(1, 1, 1.0)

        assert simple_system.SystemData.Fields.NumberOfFields == 2

        with pytest.raises(NotImplementedError):
            result = transmission(simple_system)

    def test_transmission_multiple_wavelengths_raises_notimplementederror(self, simple_system):
        simple_system.SystemData.Wavelengths.AddWavelength(0.314, 1.0)

        assert simple_system.SystemData.Wavelengths.NumberOfWavelengths == 2

        with pytest.raises(NotImplementedError):
            result = transmission(simple_system)
