import numpy as np
import pytest

from zospy.analyses.wavefront import zernike_standard_coefficients


class TestZernikeStandardCoefficients:
    def test_can_run_zernike_standard_coefficients(self, simple_system):
        result = zernike_standard_coefficients(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = zernike_standard_coefficients(simple_system)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_returns_correct_result(
        self, simple_system, sampling, maximum_term, expected_data
    ):
        result = zernike_standard_coefficients(simple_system, sampling=sampling, maximum_term=maximum_term)

        assert np.allclose(
            result.Data.Coefficients.Value.astype(float), expected_data.Data.Coefficients.Value.astype(float), atol=1e-8
        )
        assert np.isclose(
            result.Data.GeneralData.loc["StrehlRatio(Est)", "Value"],
            expected_data.Data.GeneralData.loc["StrehlRatio(Est)", "Value"],
        )
        assert all(result.Data.Coefficients.Function == expected_data.Data.Coefficients.Function)

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_matches_reference_data(
        self, simple_system, sampling, maximum_term, reference_data
    ):
        result = zernike_standard_coefficients(simple_system, sampling=sampling, maximum_term=maximum_term)

        assert np.allclose(
            result.Data.Coefficients.Value.astype(float),
            reference_data.Data.Coefficients.Value.astype(float),
            atol=1e-8,
        )
        assert np.isclose(
            result.Data.GeneralData.loc["StrehlRatio(Est)", "Value"],
            reference_data.Data.GeneralData.loc["StrehlRatio(Est)", "Value"],
        )
        assert all(result.Data.Coefficients.Function == reference_data.Data.Coefficients.Function)
