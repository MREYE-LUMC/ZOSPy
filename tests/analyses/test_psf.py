import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.psf import HuygensPSF


class TestHuygensPSF:
    def test_can_run(self, simple_system):
        result = HuygensPSF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = HuygensPSF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,psf_type,normalize",
        [
            ("64x64", "64x64", 0.0, "Linear", False),
            ("32x32", "64x64", 1.0, "Linear", False),
            ("128x128", "128x128", 0.0, "Real", True),
            ("32x32", "32x32", 0.0, "Real", True),
        ],
    )
    def test_huygens_psf_returns_correct_result(
        self, simple_system, pupil_sampling, image_sampling, image_delta, psf_type, normalize, expected_data
    ):
        result = HuygensPSF(
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            psf_type=psf_type,
            normalize=normalize,
        ).run(simple_system)

        assert_frame_equal(result.data, expected_data.data)

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,psf_type,normalize",
        [
            ("64x64", "64x64", 0.0, "Linear", False),
            ("32x32", "64x64", 1.0, "Linear", False),
            ("128x128", "128x128", 0.0, "Real", True),
            ("32x32", "32x32", 0.0, "Real", True),
        ],
    )
    def test_huygens_psf_matches_reference_data(
        self, simple_system, pupil_sampling, image_sampling, image_delta, psf_type, normalize, reference_data
    ):
        result = HuygensPSF(
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            psf_type=psf_type,
            normalize=normalize,
        ).run(simple_system)

        assert_frame_equal(result.data, reference_data.data)

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,psf_type,normalize",
        [
            ("64x64", "64x64", 0.0, "Linear", False),
            ("32x32", "64x64", 1.0, "Linear", False),
            ("128x128", "128x128", 0.0, "Real", True),
            ("32x32", "32x32", 0.0, "Real", True),
        ],
    )
    def test_huygens_psf_asymmetric_returns_correct_result(
        self, decentered_system, pupil_sampling, image_sampling, image_delta, psf_type, normalize, expected_data
    ):
        result = HuygensPSF(
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            psf_type=psf_type,
            normalize=normalize,
        ).run(decentered_system)

        assert_frame_equal(result.data, expected_data.data)

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,psf_type,normalize",
        [
            ("64x64", "64x64", 0.0, "Linear", False),
            ("32x32", "64x64", 1.0, "Linear", False),
            ("128x128", "128x128", 0.0, "Real", True),
            ("32x32", "32x32", 0.0, "Real", True),
        ],
    )
    def test_huygens_psf_asymmetric_matches_reference_data(
        self, decentered_system, pupil_sampling, image_sampling, image_delta, psf_type, normalize, reference_data
    ):
        result = HuygensPSF(
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            psf_type=psf_type,
            normalize=normalize,
        ).run(decentered_system)

        assert_frame_equal(result.data, reference_data.data)
