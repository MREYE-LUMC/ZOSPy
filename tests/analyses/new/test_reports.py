from zospy.analyses.new.reports import SurfaceData, SystemData


class TestSurfaceData:
    def test_can_run(self, simple_system):
        result = SurfaceData().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = SurfaceData().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestSystemData:
    def test_can_run(self, simple_system):
        result = SystemData().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = SystemData().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
