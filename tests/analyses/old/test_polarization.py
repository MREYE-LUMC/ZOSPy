import numpy as np
import pytest

import zospy.api.config as _config
from zospy.analyses.old.polarization import polarization_pupil_map, transmission
from zospy.utils.zputils import _get_number_field

pytestmark = pytest.mark.old_analyses

XFAIL_REASON = "Intentionally skipped for this OpticStudio version. See https://zospy.readthedocs.io/compatibility."

_signs = ["", "+", "-"]
_int_numbers = ["1", "123"]
_float_numbers = [".1", ".123", "1.", "1.2", "1.23", "12.3"]
_decimal_separators = [",", "."]
_exponents = ["", "e1", "e123", "e+1", "e+123", "e-1", "e-123", "E1", "E123", "E+1", "E+123", "E-1", "E-123"]


class TestGetNumberField:
    @pytest.mark.parametrize("exp", _exponents)
    @pytest.mark.parametrize("number", _int_numbers)
    @pytest.mark.parametrize("sign", _signs)
    def test_parses_int(self, sign, number, exp):
        number_string = sign + number + exp
        res = _get_number_field("Test", f"Test: {number_string}")

        assert res == number_string

    @pytest.mark.parametrize("decimal_separator", _decimal_separators)
    @pytest.mark.parametrize("exp", _exponents)
    @pytest.mark.parametrize("number", _float_numbers)
    @pytest.mark.parametrize("sign", _signs)
    def test_parses_float(self, sign, number, exp, decimal_separator, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(_config, "DECIMAL_POINT", decimal_separator)

        number_string = (sign + number + exp).replace(".", decimal_separator)

        res = _get_number_field("Test", f"Test: {number_string}")

        assert res == number_string


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
            pytest.param(
                1,
                0,
                0,
                0,
                "Image",
                "11x11",
                marks=pytest.mark.xfail_for_opticstudio_versions(["20.3.2"], XFAIL_REASON),
            ),
            (1, 1, 0, 0, 2, "11x11"),
            (0, 1, 0, 0, "Image", "11x11"),
            pytest.param(
                1,
                1,
                45,
                90,
                "Image",
                "17x17",
                marks=pytest.mark.xfail_for_opticstudio_versions(["20.3.2", ">=24.1.3"], XFAIL_REASON),
            ),
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
            ("32x32", False, 0.001, 1, 0, 0),
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
            ("32x32", False, 0.001, 1, 0, 0),
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
            transmission(simple_system)

    def test_transmission_multiple_wavelengths_raises_notimplementederror(self, simple_system):
        simple_system.SystemData.Wavelengths.AddWavelength(0.314, 1.0)

        assert simple_system.SystemData.Wavelengths.NumberOfWavelengths == 2

        with pytest.raises(NotImplementedError):
            transmission(simple_system)
