from zospy.analyses.new.mtf import FFTThroughFocusMTF, HuygensMTF


class TestFFTThroughFocusMTF:
    def test_can_run(self, simple_system):
        result = FFTThroughFocusMTF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = FFTThroughFocusMTF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestHuygensMTF:
    def test_can_run(self, simple_system):
        result = HuygensMTF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = HuygensMTF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()