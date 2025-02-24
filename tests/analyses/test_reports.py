from tests.helpers import assert_dataclass_equal
from zospy.analyses.reports import CardinalPoints, SurfaceData, SystemData


class TestSurfaceData:
    def test_can_run(self, simple_system):
        result = SurfaceData(surface=2).run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = SurfaceData(surface=2).run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    def test_surface_data_returns_correct_result(self, simple_system, expected_data):
        result = SurfaceData(surface=2).run(simple_system)

        assert_dataclass_equal(result.data, expected_data.data, ignore_fields=["date", "file"])

    def test_surface_data_matches_reference_data(self, simple_system, reference_data):
        result = SurfaceData(surface=2).run(simple_system)

        assert_dataclass_equal(result.data, reference_data.data, ignore_fields=["date", "file"])


class TestSystemData:
    def test_can_run(self, simple_system):
        result = SystemData().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = SystemData().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    def test_system_data_returns_correct_result(self, simple_system, expected_data):
        result = SystemData().run(simple_system)

        assert_dataclass_equal(result.data, expected_data.data)

    def test_system_data_matches_reference_data(self, simple_system, reference_data):
        result = SystemData().run(simple_system)

        assert_dataclass_equal(result.data, reference_data.data)


class TestCardinalPoints:
    def test_can_run(self, simple_system):
        result = CardinalPoints(surface_1=2, surface_2=3).run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = CardinalPoints(surface_1=2, surface_2=3).run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    def test_cardinal_points_returns_correct_result(self, simple_system, expected_data):
        result = CardinalPoints(surface_1=2, surface_2=3).run(simple_system)

        assert_dataclass_equal(result.data, expected_data.data)

    def test_cardinal_points_matches_reference_data(self, simple_system, reference_data):
        result = CardinalPoints(surface_1=2, surface_2=3).run(simple_system)

        assert_dataclass_equal(result.data, reference_data.data)
