import numpy as np
import pytest

import zospy as zp
from zospy.analyses.polarization import polarization_pupil_map, transmission


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
