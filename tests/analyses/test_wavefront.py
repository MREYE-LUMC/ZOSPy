from zospy.analyses.wavefront import WavefrontMap, ZernikeStandardCoefficients


class TestWavefrontMap:
    def test_can_run(self, simple_system):
        result = WavefrontMap().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = WavefrontMap().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestZernikeStandardCoefficients:
    def test_can_run(self, simple_system):
        result = ZernikeStandardCoefficients().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = ZernikeStandardCoefficients().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
