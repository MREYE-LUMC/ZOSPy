import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.old.psf import huygens_psf

pytestmark = pytest.mark.old_analyses


class TestHuygensPSF:
    def test_can_run_huygens_psf(self, simple_system):
        result = huygens_psf(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = huygens_psf(simple_system)

        assert result.from_json(result.to_json())

    def test_huygens_psf_returns_correct_result(self, simple_system, expected_data):
        result = huygens_psf(simple_system)

        assert_frame_equal(result.Data.astype(float), expected_data.Data.astype(float))

    def test_huygens_psf_matches_reference_data(self, simple_system, reference_data):
        result = huygens_psf(simple_system)

        assert_frame_equal(result.Data.astype(float), reference_data.Data.astype(float))

    def test_huygens_psf_asymmetric_returns_correct_result(self, decentered_system, expected_data):
        result = huygens_psf(decentered_system)

        assert_frame_equal(result.Data.astype(float), expected_data.Data.astype(float))

    def test_huygens_psf_asymmetric_matches_reference_data(self, decentered_system, reference_data):
        result = huygens_psf(decentered_system)

        assert_frame_equal(result.Data.astype(float), reference_data.Data.astype(float))
