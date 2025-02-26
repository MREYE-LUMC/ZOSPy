import pytest
from pandas.testing import assert_frame_equal

from tests.helpers import assert_dataclass_equal
from zospy.analyses.raysandspots import RayFan, SingleRayTrace


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

        assert_dataclass_equal(result.data, expected_data.data)

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

        assert_dataclass_equal(
            result.data, reference_data.data, ignore_fields=["real_ray_trace_data", "paraxial_ray_trace_data"]
        )


class TestRayFan:
    def test_can_run(self, simple_system):
        result = RayFan().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = RayFan().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "fieldx,fieldy", [(0, 0), (5.5, 0), (0, 5.5), (5.5, 5.5), (-5.5, 0), (0, -5.5), (-5.5, -5.5)]
    )
    def test_field_parsing(self, fieldx, fieldy, simple_system):
        field1 = simple_system.SystemData.Fields.GetField(1)
        field1.X = fieldx
        field1.Y = fieldy
        result = RayFan().run(simple_system)

        assert result.data.tangential[0].field_coordinate.value[0] == fieldx
        assert result.data.tangential[0].field_coordinate.value[1] == fieldy
        assert result.data.sagittal[0].field_coordinate.value[0] == fieldx
        assert result.data.sagittal[0].field_coordinate.value[1] == fieldy

    @pytest.mark.parametrize("fields", [[(5.5, -5.5)], [(0, 0), (0.0, 5.5), (5.5, 0.0), (5.5, -5.5)]])
    def test_to_dataframe(self, fields, simple_system):
        field1 = simple_system.SystemData.Fields.GetField(1)
        field1.X = fields[0][0]
        field1.Y = fields[0][1]

        for f in fields[1:]:
            simple_system.SystemData.Fields.AddField(f[0], f[1], 1.0)

        result = RayFan().run(simple_system)

        df = result.data.to_dataframe()

        for r in result.data.tangential:
            for wl in r.data.columns:
                assert_frame_equal(
                    df.loc[
                        (df["Direction"] == "Tangential")
                        & (df["Field Number"] == r.field_number)
                        & (df["FieldX"] == r.field_coordinate.value[0])
                        & (df["FieldY"] == r.field_coordinate.value[1])
                        & (df["Wavelength"] == wl),
                        ["Pupil", "Aberration"],
                    ].set_index("Pupil"),
                    r.data[wl].to_frame("Aberration"),
                )

        for r in result.data.sagittal:
            for wl in r.data.columns:
                assert_frame_equal(
                    df.loc[
                        (df["Direction"] == "Sagittal")
                        & (df["Field Number"] == r.field_number)
                        & (df["FieldX"] == r.field_coordinate.value[0])
                        & (df["FieldY"] == r.field_coordinate.value[1])
                        & (df["Wavelength"] == wl),
                        ["Pupil", "Aberration"],
                    ].set_index("Pupil"),
                    r.data[wl].to_frame("Aberration"),
                )

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
