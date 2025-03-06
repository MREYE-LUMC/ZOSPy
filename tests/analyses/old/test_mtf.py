import numpy as np
import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.old.mtf import (
    fft_through_focus_mtf,
    fft_through_focus_mtf_fromcfg,
    huygens_mtf,
)

pytestmark = pytest.mark.old_analyses

_FFT_THROUGH_FOCUS_MTF_MTFTYPE_EXPECTED_RETURN = {
    # The expected return does not match constants.Analysis.Settings.Mtf.MtfTypes for fft_through_focus_mtf
    "Modulation": "5",
    "Real": "6",
    "Imaginary": "7",
    "Phase": "8",
    "SquareWave": "9",
}


class TestFFTThroughFocusMTF:
    def test_can_run_fft_through_focus_mtf(self, simple_system):
        result = fft_through_focus_mtf(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = fft_through_focus_mtf(simple_system)

        assert result.from_json(result.to_json())

    def test_can_run_fft_through_focus_mtf_fromcfg(self, simple_system, cfg_file):
        result = fft_through_focus_mtf_fromcfg(simple_system, str(cfg_file))

        assert result.Data is not None

    def test_fft_through_focus_mtf_fromcfg_loads_config_correctly(self, simple_system, cfg_file):
        result = fft_through_focus_mtf_fromcfg(simple_system, str(cfg_file))

        assert result.Settings.SampleSize == "S_128x128"
        assert result.Settings.DeltaFocus == 1.2
        assert result.Settings.Frequency == 3.0
        assert result.Settings.NumberOfSteps == 9
        # assert result.Settings.Type == "Imaginary"
        assert result.Settings.UsePolarization

    @pytest.mark.parametrize(
        "sampling,deltafocus,frequency,numberofsteps,mtftype",
        [("64x64", 0.1, 0, 5, "Modulation"), ("128x128", 0.3, 3, 10, "Imaginary")],
    )
    def test_fft_through_focus_mtf_returns_correct_result(
        self, simple_system, sampling, deltafocus, frequency, numberofsteps, mtftype, expected_data
    ):
        result = fft_through_focus_mtf(
            simple_system,
            sampling=sampling,
            deltafocus=deltafocus,
            frequency=frequency,
            numberofsteps=numberofsteps,
            mtftype=mtftype,
        )

        assert np.allclose(result.Data.astype(float), expected_data.Data.astype(float), rtol=1e-3)

    @pytest.mark.parametrize(
        "sampling,deltafocus,frequency,numberofsteps,mtftype",
        [("64x64", 0.1, 0, 5, "Modulation"), ("128x128", 0.3, 3, 10, "Imaginary")],
    )
    def test_fft_through_focus_mtf_matches_reference_data(
        self, simple_system, sampling, deltafocus, frequency, numberofsteps, mtftype, reference_data
    ):
        result = fft_through_focus_mtf(
            simple_system,
            sampling=sampling,
            deltafocus=deltafocus,
            frequency=frequency,
            numberofsteps=numberofsteps,
            mtftype=mtftype,
        )

        assert np.allclose(result.Data.astype(float), reference_data.Data.astype(float), rtol=1e-3)

    @pytest.mark.parametrize(
        "mtftype",
        ["Modulation", "Real", "Imaginary", "Phase", "SquareWave"],
    )
    def test_fft_through_focus_mtf_sets_mtftype_correctly(self, simple_system, mtftype):
        result = fft_through_focus_mtf(
            simple_system,
            mtftype=mtftype,
        )

        assert result.Settings["Type"] == _FFT_THROUGH_FOCUS_MTF_MTFTYPE_EXPECTED_RETURN[mtftype]


class TestHuygensMTF:
    def test_can_run_huygens_mtf(self, simple_system):
        result = huygens_mtf(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = huygens_mtf(simple_system)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,mtftype,maximum_frequency",
        [
            ("64x64", "64x64", 0.0, "Modulation", 150.0),
            ("32x32", "64x64", 1.0, "Modulation", 450.0),
            ("128x128", "128x128", 0.0, "Modulation", 314.5),
            ("32x32", "32x32", 0.0, "Modulation", 150.0),
        ],
    )
    def test_huygens_mtf_returns_correct_result(
        self, simple_system, pupil_sampling, image_sampling, image_delta, mtftype, maximum_frequency, expected_data
    ):
        result = huygens_mtf(
            simple_system,
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            mtftype=mtftype,
            maximum_frequency=maximum_frequency,
        )

        assert_frame_equal(result.Data.astype(float), expected_data.Data.astype(float))

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,mtftype,maximum_frequency",
        [
            ("64x64", "64x64", 0.0, "Modulation", 150.0),
            ("32x32", "64x64", 1.0, "Modulation", 450.0),
            ("128x128", "128x128", 0.0, "Modulation", 314.5),
            ("32x32", "32x32", 0.0, "Modulation", 150.0),
        ],
    )
    def test_huygens_mtf_matches_reference_data(
        self, simple_system, pupil_sampling, image_sampling, image_delta, mtftype, maximum_frequency, reference_data
    ):
        result = huygens_mtf(
            simple_system,
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            mtftype=mtftype,
            maximum_frequency=maximum_frequency,
        )

        assert_frame_equal(result.Data.astype(float), reference_data.Data.astype(float))
