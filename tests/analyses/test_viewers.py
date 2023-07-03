from zospy.analyses.systemviewers import (
    cross_section,
    nsc_3d_layout,
    nsc_shaded_model,
    shaded_model,
    viewer_3d,
)


class TestViewers:
    def test_can_run_cross_section(self, simple_system):
        result = cross_section(simple_system, oncomplete="Sustain")
        analysistype = str(result.Analysis._analysis.AnalysisType)
        result.Analysis._analysis.Close()

        assert analysistype == "Draw2D"

    def test_can_run_viewer_3d(self, simple_system):
        result = viewer_3d(simple_system, oncomplete="Sustain")
        analysistype = str(result.Analysis._analysis.AnalysisType)
        result.Analysis._analysis.Close()

        assert analysistype == "Draw3D"

    def test_can_run_shaded_model(self, simple_system):
        result = shaded_model(simple_system, oncomplete="Sustain")
        analysistype = str(result.Analysis._analysis.AnalysisType)
        result.Analysis._analysis.Close()

        assert analysistype == "ShadedModel"

    def test_can_run_nsc_3d_layout(self, nsc_simple_system):
        result = nsc_3d_layout(nsc_simple_system, oncomplete="Sustain")
        analysistype = str(result.Analysis._analysis.AnalysisType)
        result.Analysis._analysis.Close()

        assert analysistype == "NSC3DLayout"

    def test_can_run_nsc_shaded_model(self, nsc_simple_system):
        result = nsc_shaded_model(nsc_simple_system, oncomplete="Sustain")
        analysistype = str(result.Analysis._analysis.AnalysisType)
        result.Analysis._analysis.Close()

        assert analysistype == "NSCShadedModel"
