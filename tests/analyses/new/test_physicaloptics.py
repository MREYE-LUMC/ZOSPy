from zospy.analyses.new.physicaloptics import PhysicalOpticsPropagation


class TestPhysicalOpticsPropagation:
    def test_can_run(self, simple_system):
        result = PhysicalOpticsPropagation().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = PhysicalOpticsPropagation().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
