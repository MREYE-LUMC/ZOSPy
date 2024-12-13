from zospy.analyses.new.systemviewers import CrossSection, NSC3DLayout, NSCShadedModel, ShadedModel, Viewer3D


class TestCrossSection:
    def test_can_run(self, simple_system):
        result = CrossSection().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = CrossSection().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestViewer3D:
    def test_can_run(self, simple_system):
        result = Viewer3D().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = Viewer3D().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestShadedModel:
    def test_can_run(self, simple_system):
        result = ShadedModel().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = ShadedModel().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestNSC3DLayout:
    def test_can_run(self, nsc_simple_system):
        result = NSC3DLayout().run(nsc_simple_system)
        assert result.data is not None

    def test_to_json(self, nsc_simple_system):
        result = NSC3DLayout().run(nsc_simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()


class TestNSCShadedModel:
    def test_can_run(self, nsc_simple_system):
        result = NSCShadedModel().run(nsc_simple_system)
        assert result.data is not None

    def test_to_json(self, nsc_simple_system):
        result = NSCShadedModel().run(nsc_simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
