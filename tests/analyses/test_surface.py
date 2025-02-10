from zospy.analyses.surface import Curvature


class TestCurvature:
    def test_can_run(self, simple_system):
        result = Curvature().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = Curvature().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
