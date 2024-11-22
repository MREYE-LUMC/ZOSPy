from zospy.analyses.new.raysandspots import SingleRayTrace


class TestSingleRayTrace:
    def test_can_run(self, simple_system):
        result = SingleRayTrace().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = SingleRayTrace().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
