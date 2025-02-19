import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.surface import Curvature


class TestCurvature:
    def test_can_run(self, simple_system):
        result = Curvature().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = Curvature(surface=2).run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    SKIP_SAGITTAL_CURVATURE = "SagitalCurvature is renamed to SagittalCurvature in OpticStudio 24.1.2 and higher"

    @pytest.mark.parametrize(
        "sampling,data,remove,surface,show_as,contour_format,bfs_criterion,bfs_reverse_direction",
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
        show_as,
        contour_format,
        bfs_criterion,
        bfs_reverse_direction,
        expected_data,
    ):
        result = Curvature(
            sampling=sampling,
            data=data,
            remove=remove,
            surface=surface,
            show_as=show_as,
            contour_format=contour_format,
            bfs_criterion=bfs_criterion,
            bfs_reverse_direction=bfs_reverse_direction,
        ).run(simple_system)

        assert_frame_equal(result.data.data, expected_data.data.data)
