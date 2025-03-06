import numpy as np
import pytest

from zospy.analyses.old.wavefront import wavefront_map, zernike_standard_coefficients

pytestmark = pytest.mark.old_analyses


class TestWavefrontMap:
    def test_can_run_wavefront_map(self, simple_system):
        result = wavefront_map(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = wavefront_map(simple_system)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize(
        "sampling,use_exit_pupil", [("64x64", True), ("64x64", False), ("128x128", True), ("128x128", False)]
    )
    def test_wavefront_map_returns_correct_result(self, simple_system, sampling, use_exit_pupil, expected_data):
        result = wavefront_map(simple_system, sampling=sampling, use_exit_pupil=use_exit_pupil)

        assert np.allclose(result.Data.to_numpy(dtype=float), expected_data.Data.to_numpy(dtype=float), equal_nan=True)

    @pytest.mark.parametrize(
        "sampling,use_exit_pupil", [("64x64", True), ("64x64", False), ("128x128", True), ("128x128", False)]
    )
    def test_wavefront_map_matches_reference_data(self, simple_system, sampling, use_exit_pupil, reference_data):
        result = wavefront_map(simple_system, sampling=sampling, use_exit_pupil=use_exit_pupil)

        assert np.allclose(result.Data.to_numpy(dtype=float), reference_data.Data.to_numpy(dtype=float), equal_nan=True)


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
