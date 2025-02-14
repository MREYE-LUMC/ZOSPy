import numpy as np

from tests.helpers import assert_dataclass_equal
from zospy.analyses.raysandspots import RayFan, SingleRayTrace
import pytest

class TestSingleRayTrace:
    def test_can_run(self, simple_system):
        result = SingleRayTrace().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = SingleRayTrace().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

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
        result = SingleRayTrace(
            hx=hx,
            hy=hy,
            px=px,
            py=py,
            raytrace_type=raytrace_type,
            global_coordinates=global_coordinates,
        ).run(simple_system)

        assert_dataclass_equal(result.data, expected_data.data, ignore_fields=["real_ray_trace_data", "paraxial_ray_trace_data"])
        assert np.allclose(
            result.data.real_ray_trace_data.select_dtypes(float),
            expected_data.data.real_ray_trace_data.select_dtypes(float),
            equal_nan=True,
        )
        assert np.allclose(
            result.data.paraxial_ray_trace_data.select_dtypes(float),
            expected_data.data.paraxial_ray_trace_data.select_dtypes(float),
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
        result = SingleRayTrace(
            hx=hx,
            hy=hy,
            px=px,
            py=py,
            raytrace_type=raytrace_type,
            global_coordinates=global_coordinates,
        ).run(simple_system)

        assert_dataclass_equal(result.data, reference_data.data, ignore_fields=["real_ray_trace_data", "paraxial_ray_trace_data"])
        assert np.allclose(
            result.data.real_ray_trace_data.select_dtypes(float),
            reference_data.data.real_ray_trace_data.select_dtypes(float),
            equal_nan=True,
        )
        assert np.allclose(
            result.data.paraxial_ray_trace_data.select_dtypes(float),
            reference_data.data.paraxial_ray_trace_data.select_dtypes(float),
            equal_nan=True,
        )


class TestRayFan:
    def test_can_run(self, simple_system):
        result = RayFan().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = RayFan().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

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
        result = RayFan(
            plot_scale=plot_scale,
            number_of_rays=number_of_rays,
            tangential=tangential,
            sagittal=sagittal,
        ).run(simple_system)

        assert_dataclass_equal(result.data, expected_data.data)

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
        result = RayFan(
            plot_scale=plot_scale,
            number_of_rays=number_of_rays,
            tangential=tangential,
            sagittal=sagittal,
        ).run(simple_system)

        assert_dataclass_equal(result.data, reference_data.data)
