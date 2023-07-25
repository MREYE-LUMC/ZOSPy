import numpy as np
import pytest

import zospy.api.config as _config
from zospy.analyses.polarization import (
    _get_number_field,
    polarization_pupil_map,
    transmission,
)

_signs = ["", "+", "-"]
_int_numbers = ["1", "123"]
_float_numbers = [".1", ".123", "1.", "1.2", "1.23", "12.3"]
_decimal_separators = [",", "."]
_exps = ["", "e1", "e123", "e+1", "e+123", "e-1", "e-123", "E1", "E123", "E+1", "E+123", "E-1", "E-123"]


class TestGetNumberField:
    @pytest.mark.parametrize("sign", _signs)
    @pytest.mark.parametrize("number", _int_numbers)
    @pytest.mark.parametrize("exp", _exps)
    def test_get_number_field_returns_correct_result_for_integers(self, sign, number, exp):
        ...
        "number_string", [_sign + _number + _exp for _sign in _signs for _number in _int_numbers for _exp in _exps]
    )
    def test_get_number_field_returns_correct_result_for_integers(self, number_string):
        res = _get_number_field("Test", f"Test: {number_string}")

        assert res == number_string

    @pytest.mark.parametrize(
        "number_string, decimal_separator",
        [
            ((_sign + _number + _exp).replace(".", _decimal_separator), _decimal_separator)
            for _sign in _signs
            for _number in _float_numbers
            for _exp in _exps
            for _decimal_separator in _decimal_separators
        ],
    )
    def test_get_number_field_returns_correct_result_for_floats(self, number_string, decimal_separator):
        original_decimal_point = _config.DECIMAL_POINT  # store original decimal separator to revert later
        if decimal_separator is not None:
            _config.DECIMAL_POINT = decimal_separator  # adjust configured decimal point separator

        res = _get_number_field("Test", f"Test: {number_string}")

        _config.DECIMAL_POINT = original_decimal_point  # restore originally configured decimal point

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
            result = transmission(simple_system)

    def test_transmission_multiple_wavelengths_raises_notimplementederror(self, simple_system):
        simple_system.SystemData.Wavelengths.AddWavelength(0.314, 1.0)

        assert simple_system.SystemData.Wavelengths.NumberOfWavelengths == 2

        with pytest.raises(NotImplementedError):
            result = transmission(simple_system)
