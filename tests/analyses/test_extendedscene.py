from zospy.analyses.extendedscene import GeometricImageAnalysis


class TestPolarizationTransmission:
    def test_can_run(self, simple_system):
        result = GeometricImageAnalysis().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = GeometricImageAnalysis().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
