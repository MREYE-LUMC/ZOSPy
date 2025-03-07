import numpy as np
import pytest

from zospy.analyses.old.raysandspots import ray_fan, single_ray_trace
from zospy.api.config import DECIMAL_POINT

pytestmark = pytest.mark.old_analyses


class TestSingleRayTrace:
    def test_can_run_single_ray_trace(self, simple_system):
        result = single_ray_trace(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = single_ray_trace(simple_system)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize(
        "hx,hy,px,py,raytrace_type,global_coordinates",
        [
            (1, 1, 0, 0, "DirectionCosines", False),
            (0, 0, 1, 1, "DirectionCosines", True),
            (1, 1, 0, 0, "TangentAngle", True),
        ],
    )
    def test_single_ray_trace_returns_correct_result(
        self, simple_system, hx, hy, px, py, raytrace_type, global_coordinates, expected_data
    ):
        result = single_ray_trace(
            simple_system,
            hx=hx,
            hy=hy,
            px=px,
            py=py,
            raytrace_type=raytrace_type,
            global_coordinates=global_coordinates,
        )

        assert np.allclose(
            result.Data.ParaxialRayTraceData.select_dtypes(float),
            expected_data.Data.ParaxialRayTraceData.select_dtypes(float),
            equal_nan=True,
        )
        assert np.allclose(
            result.Data.RealRayTraceData.select_dtypes(float),
            expected_data.Data.RealRayTraceData.select_dtypes(float),
            equal_nan=True,
        )

    @pytest.mark.parametrize(
        "hx,hy,px,py,raytrace_type,global_coordinates",
        [
            (1, 1, 0, 0, "DirectionCosines", False),
            (0, 0, 1, 1, "DirectionCosines", True),
            (1, 1, 0, 0, "TangentAngle", True),
        ],
    )
    def test_single_ray_trace_matches_reference_data(
        self, simple_system, hx, hy, px, py, raytrace_type, global_coordinates, reference_data
    ):
        result = single_ray_trace(
            simple_system,
            hx=hx,
            hy=hy,
            px=px,
            py=py,
            raytrace_type=raytrace_type,
            global_coordinates=global_coordinates,
        )

        assert np.allclose(
            result.Data.ParaxialRayTraceData.select_dtypes(float),
            reference_data.Data.ParaxialRayTraceData.select_dtypes(float),
            equal_nan=True,
        )
        assert np.allclose(
            result.Data.RealRayTraceData.select_dtypes(float),
            reference_data.Data.RealRayTraceData.select_dtypes(float),
            equal_nan=True,
        )


class TestRayFan:
    def test_can_run_ray_fan(self, simple_system):
        result = ray_fan(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = ray_fan(simple_system)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize(
        "plot_scale,number_of_rays,tangential,sagittal",
        [
            (0, 20, "Aberration_Y", "Aberration_X"),
            (1, 40, "Aberration_Y", "Aberration_X"),
            (0, 20, "Aberration_X", "Aberration_Y"),
        ],
    )
    def test_ray_fan_returns_correct_result(
        self, simple_system, plot_scale, number_of_rays, tangential, sagittal, expected_data
    ):
        result = ray_fan(
            simple_system,
            plot_scale=plot_scale,
            number_of_rays=number_of_rays,
            tangential=tangential,
            sagittal=sagittal,
        )

        assert np.allclose(
            result.Data[f"Tangential fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
            expected_data.Data[f"Tangential fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
        )
        assert np.allclose(
            result.Data[f"Sagittal fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
            expected_data.Data[f"Sagittal fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
        )

    @pytest.mark.parametrize(
        "plot_scale,number_of_rays,tangential,sagittal",
        [
            (0, 20, "Aberration_Y", "Aberration_X"),
            (1, 40, "Aberration_Y", "Aberration_X"),
            (0, 20, "Aberration_X", "Aberration_Y"),
        ],
    )
    def test_ray_fan_matches_reference_data(
        self, simple_system, plot_scale, number_of_rays, tangential, sagittal, reference_data
    ):
        result = ray_fan(
            simple_system,
            plot_scale=plot_scale,
            number_of_rays=number_of_rays,
            tangential=tangential,
            sagittal=sagittal,
        )

        assert np.allclose(
            result.Data[f"Tangential fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
            reference_data.Data[f"Tangential fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
        )
        assert np.allclose(
            result.Data[f"Sagittal fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
            reference_data.Data[f"Sagittal fan, field number 1 = 0{DECIMAL_POINT}0000 (deg)"],
        )
