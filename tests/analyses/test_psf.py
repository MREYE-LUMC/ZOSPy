import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.psf import FFTPSF, HuygensPSF


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


class TestFFTPSF:
    def test_can_run(self, simple_system):
        result = FFTPSF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = FFTPSF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    fft_psf_parametrize = pytest.mark.parametrize(
        "sampling,display,rotation,psf_type,use_polarization,image_delta,normalize,surface",
        [
            ("32x32", "32x32", 0, "Linear", False, 0.0, False, "Image"),
            ("64x64", "32x32", 90, "Log", True, 0.0, False, "Image"),
            ("64x64", "64x64", 180, "Phase", True, 0.5, True, "Image"),
            ("128x128", "32x32", 270, "Real", False, 0.0, True, "Image"),
            ("32x32", "32x32", 0, "Imaginary", False, 1.0, False, 3),
        ],
    )

    @fft_psf_parametrize
    def test_fft_psf_returns_correct_result(
        self,
        simple_system,
        sampling,
        display,
        rotation,
        psf_type,
        use_polarization,
        image_delta,
        normalize,
        surface,
        expected_data,
    ):
        result = FFTPSF(
            sampling=sampling,
            display=display,
            rotation=rotation,
            psf_type=psf_type,
            use_polarization=use_polarization,
            image_delta=image_delta,
            normalize=normalize,
            surface=surface,
        ).run(simple_system)

        assert_frame_equal(result.data, expected_data.data)

    @fft_psf_parametrize
    def test_fft_psf_matches_reference_data(
        self,
        simple_system,
        sampling,
        display,
        rotation,
        psf_type,
        use_polarization,
        image_delta,
        normalize,
        surface,
        reference_data,
    ):
        result = FFTPSF(
            sampling=sampling,
            display=display,
            rotation=rotation,
            psf_type=psf_type,
            use_polarization=use_polarization,
            image_delta=image_delta,
            normalize=normalize,
            surface=surface,
        ).run(simple_system)

        assert_frame_equal(result.data, reference_data.data)

    # Larger sampling sizes needed for accurate results in decentered system
    fft_psf_decentered_parametrize = pytest.mark.parametrize(
        "sampling,display,rotation,psf_type,use_polarization,image_delta,normalize,surface",
        [
            ("128x128", "32x32", 0, "Linear", False, 0.0, False, "Image"),
            ("128x128", "128x128", 90, "Log", True, 0.0, False, "Image"),
            ("256x256", "64x64", 180, "Phase", True, 0.5, True, "Image"),
            ("128x128", "32x32", 270, "Real", False, 0.0, True, "Image"),
            ("1024x1024", "512x512", 0, "Imaginary", False, 1.0, False, 3),
        ],
    )

    @fft_psf_decentered_parametrize
    def test_fft_psf_asymmetric_returns_correct_result(
        self,
        decentered_system,
        sampling,
        display,
        rotation,
        psf_type,
        use_polarization,
        image_delta,
        normalize,
        surface,
        expected_data,
    ):
        result = FFTPSF(
            sampling=sampling,
            display=display,
            rotation=rotation,
            psf_type=psf_type,
            use_polarization=use_polarization,
            image_delta=image_delta,
            normalize=normalize,
            surface=surface,
        ).run(decentered_system)

        assert_frame_equal(result.data, expected_data.data)

    @fft_psf_decentered_parametrize
    def test_fft_psf_asymmetric_matches_reference_data(
        self,
        decentered_system,
        sampling,
        display,
        rotation,
        psf_type,
        use_polarization,
        image_delta,
        normalize,
        surface,
        reference_data,
    ):
        result = FFTPSF(
            sampling=sampling,
            display=display,
            rotation=rotation,
            psf_type=psf_type,
            use_polarization=use_polarization,
            image_delta=image_delta,
            normalize=normalize,
            surface=surface,
        ).run(decentered_system)

        assert_frame_equal(result.data, reference_data.data)
