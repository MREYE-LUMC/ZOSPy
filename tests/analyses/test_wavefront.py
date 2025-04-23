import pytest
from pandas.testing import assert_frame_equal

from tests.helpers import assert_dataclass_equal
from zospy.analyses.wavefront import WavefrontMap, ZernikeStandardCoefficients


class TestWavefrontMap:
    def test_can_run(self, simple_system):
        result = WavefrontMap().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = WavefrontMap().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "sampling,use_exit_pupil", [("64x64", True), ("64x64", False), ("128x128", True), ("128x128", False)]
    )
    def test_wavefront_map_returns_correct_result(self, simple_system, sampling, use_exit_pupil, expected_data):
        result = WavefrontMap(sampling=sampling, use_exit_pupil=use_exit_pupil).run(simple_system)

        assert_frame_equal(result.data, expected_data.data)


class TestZernikeStandardCoefficients:
    def test_can_run(self, simple_system):
        result = ZernikeStandardCoefficients().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = ZernikeStandardCoefficients().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_returns_correct_result(
        self, simple_system, sampling, maximum_term, expected_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(simple_system)

        assert_dataclass_equal(
            result.data,
            expected_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_decentered_returns_correct_result(
        self, decentered_system, sampling, maximum_term, expected_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(decentered_system)

        assert_dataclass_equal(
            result.data,
            expected_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_object_height_returns_correct_result(
        self, object_height_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(object_height_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_matches_reference_data(
        self, simple_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(simple_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_decentered_matches_reference_data(
        self, decentered_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(decentered_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_object_height_matches_reference_data(
        self, object_height_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(object_height_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )
