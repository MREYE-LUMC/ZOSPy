import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.old.surface import curvature

pytestmark = pytest.mark.old_analyses


class TestCurvature:
    SKIP_SAGITTAL_CURVATURE = "SagitalCurvature is renamed to SagittalCurvature in OpticStudio 24.1.2 and higher"

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
            pytest.param(
                "129x129",
                "SagitalCurvature",
                None,
                2,
                "Contour",
                "",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions(">=24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
            pytest.param(
                "129x129",
                "SagitalCurvature",
                "BaseROC",
                2,
                "Contour",
                "0.1",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions(">=24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
            pytest.param(
                "129x129",
                "SagittalCurvature",
                None,
                2,
                "Contour",
                "",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions("<24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
            pytest.param(
                "129x129",
                "SagittalCurvature",
                "BaseROC",
                2,
                "Contour",
                "0.1",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions("<24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
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

        assert_frame_equal(result.Data, expected_data.Data)

    @pytest.mark.parametrize(
        "sampling,data,remove,surface,showas,contourformat,bfs_criterion,bfs_reversedirection",
        [
            ("65x65", "TangentialCurvature", None, 2, "Surface", "", "MinimumVolume", False),
            pytest.param(
                "129x129",
                "SagitalCurvature",
                None,
                2,
                "Contour",
                "",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions(">=24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
            pytest.param(
                "129x129",
                "SagitalCurvature",
                "BaseROC",
                2,
                "Contour",
                "0.1",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions(">=24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
            pytest.param(
                "129x129",
                "SagittalCurvature",
                None,
                2,
                "Contour",
                "",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions("<24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
            pytest.param(
                "129x129",
                "SagittalCurvature",
                "BaseROC",
                2,
                "Contour",
                "0.1",
                "MinimumVolume",
                False,
                marks=pytest.mark.skip_for_opticstudio_versions("<24.1.2", SKIP_SAGITTAL_CURVATURE),
            ),
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

        assert_frame_equal(result.Data, reference_data.Data)
