import numpy as np
import pytest

from zospy.analyses.surface import curvature


class TestCurvature:
    def test_can_run_curvature(self, simple_system):
        result = curvature(simple_system, surface=2)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = curvature(simple_system, surface=2)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize(
        "sampling,data,remove,surface,showas,contourformat,bfs_criterion,bfs_reversedirection",
        [
            ("65x65", "TangentialCurvature", None, 2, "Surface", "", "MinimumVolume", False),
            ("129x129", "SagitalCurvature", None, 2, "Contour", "", "MinimumVolume", False),
            ("129x129", "SagitalCurvature", "BaseROC", 2, "Contour", "0.1", "MinimumVolume", False),
            ("33x33", "X_Curvature", "BestFitSphere", 3, "Contour", "", "MinimumRMS", False),
            ("33x33", "X_Curvature", "BestFitSphere", 3, "Contour", "", "MinimumVolume", False),
            ("33x33", "X_Curvature", "BestFitSphere", 3, "Contour", "0.2", "MinimumVolume", True),
        ],
    )
    def test_curvature_returns_correct_result(
        self,
        simple_system,
        sampling,
        data,
        remove,
        surface,
        showas,
        contourformat,
        bfs_criterion,
        bfs_reversedirection,
        expected_data,
    ):
        result = curvature(
            simple_system,
            sampling=sampling,
            data=data,
            remove=remove,
            surface=surface,
            showas=showas,
            contourformat=contourformat,
            bfs_criterion=bfs_criterion,
            bfs_reversedirection=bfs_reversedirection,
        )

        assert np.allclose(result.Data, expected_data.Data, equal_nan=True)

    @pytest.mark.parametrize(
        "sampling,data,remove,surface,showas,contourformat,bfs_criterion,bfs_reversedirection",
        [
            ("65x65", "TangentialCurvature", None, 2, "Surface", "", "MinimumVolume", False),
            ("129x129", "SagitalCurvature", None, 2, "Contour", "", "MinimumVolume", False),
            ("129x129", "SagitalCurvature", "BaseROC", 2, "Contour", "0.1", "MinimumVolume", False),
            ("33x33", "X_Curvature", "BestFitSphere", 3, "Contour", "", "MinimumRMS", False),
            ("33x33", "X_Curvature", "BestFitSphere", 3, "Contour", "", "MinimumVolume", False),
            ("33x33", "X_Curvature", "BestFitSphere", 3, "Contour", "0.2", "MinimumVolume", True),
        ],
    )
    def test_curvature_matches_reference_data(
        self,
        simple_system,
        sampling,
        data,
        remove,
        surface,
        showas,
        contourformat,
        bfs_criterion,
        bfs_reversedirection,
        reference_data,
    ):
        result = curvature(
            simple_system,
            sampling=sampling,
            data=data,
            remove=remove,
            surface=surface,
            showas=showas,
            contourformat=contourformat,
            bfs_criterion=bfs_criterion,
            bfs_reversedirection=bfs_reversedirection,
        )

        assert np.allclose(result.Data, reference_data.Data, equal_nan=True)
