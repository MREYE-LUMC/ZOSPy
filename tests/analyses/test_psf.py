from pandas.testing import assert_frame_equal

from zospy.analyses.psf import HuygensPSF


class TestHuygensPSF:
    def test_can_run(self, simple_system):
        result = HuygensPSF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = HuygensPSF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    def test_huygens_psf_returns_correct_result(self, simple_system, expected_data):
        result = HuygensPSF().run(simple_system)

        assert_frame_equal(result.data, expected_data.data)

    def test_huygens_psf_matches_reference_data(self, simple_system, reference_data):
        result = HuygensPSF().run(simple_system)

        assert_frame_equal(result.data, reference_data.data)

    def test_huygens_psf_asymmetric_returns_correct_result(self, decentered_system, expected_data):
        result = HuygensPSF().run(decentered_system)

        assert_frame_equal(result.data, expected_data.data)

    def test_huygens_psf_asymmetric_matches_reference_data(self, decentered_system, reference_data):
        result = HuygensPSF().run(decentered_system)

        assert_frame_equal(result.data, reference_data.data)
