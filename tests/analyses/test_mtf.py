import numpy as np
import pytest

from zospy.analyses.mtf import fft_through_focus_mtf, fft_through_focus_mtf_fromcfg


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
