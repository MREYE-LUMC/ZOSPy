"""Helper functions that are used in the raytracing and analysis notebooks.

- `get_nodal_points`: Calculate the object and image nodal points of an optical system using OpticStudio.
- `get_ray_input_angle`: Calculate the input angle of a ray with respect to the optical axis.
- `get_ray_output_angle`: Calculate the output angle of a ray with respect to the optical axis and a reference point.
- `InputOutputAngles`: NamedTuple to store the input and output angles of a ray.
- `get_retina_locations`: Get the retina locations for a given row in the input-output angles DataFrame.
- `euclidean_distance`: Convert two series of tuples to NumPy arrays and calculate the element-wise euclidean distance.
- `find_ellipse_intersection`: Find the intersection between a straight line (light ray) and an ellipse.
- `ellipse_arc_length`: Calculate the arc length of an ellipse between two points.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, NamedTuple

import numpy as np
import pandas as pd
import sympy
from scipy.integrate import quad
from sympy.geometry import Ellipse, Line2D, Point2D, intersection

import zospy as zp

if TYPE_CHECKING:
    from zospy.analyses.base import AnalysisResult
    from zospy.analyses.raysandspots.single_ray_trace import SingleRayTraceResult, SingleRayTraceSettings
    from zospy.zpcore import OpticStudioSystem


def _ignore_fields(oss: OpticStudioSystem, index: int | list[int], ignore=True):
    if isinstance(index, int):
        index = [index]

    for i in index:
        oss.SystemData.Fields.GetField(i).Ignore = ignore


def get_nodal_points(oss: OpticStudioSystem) -> tuple[float, float]:
    """Calculate the object and image nodal points of an optical system using OpticStudio."""
    surface_1_to_iris = sum(oss.LDE.GetSurfaceAt(i).Thickness for i in range(1, oss.LDE.StopSurface))
    surface_2_to_iris = sum(
        oss.LDE.GetSurfaceAt(i).Thickness for i in range(oss.LDE.StopSurface, oss.LDE.NumberOfSurfaces - 1)
    )

    # Only use the chief ray
    _ignore_fields(oss, range(2, oss.SystemData.Fields.NumberOfFields + 1), True)

    cardinal_points_result = zp.analyses.reports.CardinalPoints(
        surface_1=1, surface_2=oss.LDE.NumberOfSurfaces - 1
    ).run(oss)

    object_nodal_point = cardinal_points_result.data.cardinal_points.nodal_planes.object - surface_1_to_iris
    image_nodal_point = cardinal_points_result.data.cardinal_points.nodal_planes.image + surface_2_to_iris

    # Enable rays again
    _ignore_fields(oss, range(2, oss.SystemData.Fields.NumberOfFields + 1), False)

    return object_nodal_point, image_nodal_point


def get_ray_input_angle(
    df: pd.DataFrame,
    reference_surface: int = 2,
    reference_point: tuple[float, float] | None = None,
    coordinate="Y-coordinate",
):
    """Calculate the input angle of a ray with respect to the optical axis."""
    x0, y0 = (
        df.loc[reference_surface - 1, "Z-coordinate"],
        df.loc[reference_surface - 1, coordinate],
    )

    if reference_point is None:
        x1, y1 = (
            df.loc[reference_surface, "Z-coordinate"],
            df.loc[reference_surface, coordinate],
        )
    else:
        x1, y1 = reference_point

    return np.rad2deg(np.arctan2(y1 - y0, x1 - x0))


def get_ray_output_angle(
    df: pd.DataFrame,
    reference_point: tuple[float, float] = (0, 0),
    coordinate="Y-coordinate",
):
    """Calculate the output angle of a ray with respect to the optical axis and a reference point."""
    x0, y0 = reference_point
    x1, y1 = df.loc[len(df) - 1, "Z-coordinate"], df.loc[len(df) - 1, coordinate]

    return np.rad2deg(np.arctan2(y1 - y0, x1 - x0))


class InputOutputAngles(NamedTuple):
    input_angle_field: float
    input_angle_cornea: float
    input_angle_pupil: float
    output_angle_pupil: float
    output_angle_np2: float
    output_angle_retina_center: float | None = None
    output_angle_navarro_np2: float | None = None
    location_np2: float | None = None
    location_retina_center: float | None = None
    patient: int | str | None = None

    @classmethod
    def from_ray_trace_result(
        cls,
        ray_trace_result: AnalysisResult[SingleRayTraceResult, SingleRayTraceSettings],
        field_angle: float,
        np2: float,
        np2_navarro: float | None = None,
        retina_center: float | None = None,
        patient: int | None = None,
        coordinate="Y-coordinate",
    ) -> InputOutputAngles:
        real_ray_trace_data = ray_trace_result.data.real_ray_trace_data

        return cls(
            input_angle_field=field_angle,
            input_angle_cornea=get_ray_input_angle(real_ray_trace_data, reference_surface=2, coordinate=coordinate),
            input_angle_pupil=get_ray_input_angle(real_ray_trace_data, reference_surface=4, coordinate=coordinate),
            output_angle_pupil=get_ray_output_angle(real_ray_trace_data, reference_point=(0, 0), coordinate=coordinate),
            output_angle_np2=get_ray_output_angle(real_ray_trace_data, reference_point=(np2, 0), coordinate=coordinate),
            output_angle_retina_center=(
                get_ray_output_angle(
                    real_ray_trace_data,
                    reference_point=(retina_center, 0),
                    coordinate=coordinate,
                )
                if retina_center is not None
                else None
            ),
            output_angle_navarro_np2=(
                get_ray_output_angle(
                    real_ray_trace_data,
                    reference_point=(np2_navarro, 0),
                    coordinate=coordinate,
                )
                if np2_navarro is not None
                else None
            ),
            location_np2=np2,
            location_retina_center=retina_center or None,
            patient=patient,
        )


def get_retina_locations(row: pd.Series, ray_trace_data: pd.DataFrame):
    """Get the retina locations for a given row in the input-output angles DataFrame."""
    retina_ray_trace_result = ray_trace_data.query("InputAngle == @row.input_angle_field and Comment == 'Retina'")

    if len(retina_ray_trace_result) != 1 and row.input_angle_field != 0:
        raise RuntimeError(f"Got more than one result for {row.input_angle_field=}")

    return tuple(retina_ray_trace_result.iloc[0][["Z-coordinate", "Y-coordinate"]])


def euclidean_distance(column_1: pd.Series, column_2: pd.Series):
    column_1_array = np.vstack(column_1)
    column_2_array = np.vstack(column_2)

    distance = np.linalg.norm(column_2_array - column_1_array, axis=1)
    sign = np.where(column_2_array[:, 0] > column_1_array[:, 0], -1, 1)

    return sign * distance


def _build_ellipse_intersection_function() -> Callable[[float, float, float, float, float], tuple[float, float]]:
    line_x_0, angle, r_x, r_y, ellipse_x_0 = sympy.symbols("line_x_0 angle r_x r_y ellipse_x_0")

    ellipse = Ellipse(center=Point2D(ellipse_x_0, 0), hradius=r_x, vradius=r_y)

    line = Line2D(p1=Point2D(line_x_0, 0), slope=sympy.tan(angle))

    ellipse_line_intersection = intersection(ellipse, line)

    return sympy.lambdify(
        [line_x_0, angle, r_x, r_y, ellipse_x_0],
        tuple(i.coordinates for i in ellipse_line_intersection),
        modules=["numpy"],
    )


sympy_ellipse_intersection = _build_ellipse_intersection_function()


def find_ellipse_intersection(
    reference_point: float,
    angle: float,
    r_x: float,
    r_y: float,
    ellipse_center_x: float,
) -> tuple[float, float]:
    """Find the intersection between a straight line and an ellipse.

    The ellipse has horizontal (axial) radius `r_x` and vertical (radial) radius `r_y`.
    The line intersects the horizontal axis at `distance_to_center` from the ellipse center
    and has an angle `angle` with the horizontal axis.

    Parameters
    ----------
    reference_point : float
        Point of intersection between the line and the horizontal axis.
    angle : float
        Angle of the line with the horizontal axis, in radians.
    r_x : float
        Horizontal radius of the ellipse.
    r_y : float
        Vertical radius of the ellipse.
    ellipse_center_x : float
        Horizontal location of the ellipse center.

    Returns
    -------
    tuple[float, float]
        Coordinate (x, y) of the intersection between the line and the ellipse.
    """
    # Angle of 0 is an edge case that needs to be handled separately
    if angle <= 1e-3:
        return ellipse_center_x + r_x, 0

    all_intersections = sympy_ellipse_intersection(reference_point, angle, r_x, r_y, ellipse_center_x)

    if len(all_intersections) == 2:
        if (
            # x of the 1st intersection is larger than x of the 2nd intersection
            all_intersections[0][0] > all_intersections[1][0]
            # y of the first intersection is positive
            and all_intersections[0][1] >= 0
        ):
            return all_intersections[0]

        return all_intersections[1]

    if len(all_intersections) == 1:
        return all_intersections[0]

    if len(all_intersections) == 0:
        return np.nan, np.nan

    raise ValueError("More than 2 intersections found 🤔")


def _upper_ellipse(x: float, r_x: float, r_y: float) -> float:
    return r_y * np.sqrt(1 - x**2 / r_x**2)


def _upper_ellipse_arc(x: float, r_x: float, r_y: float) -> float:
    return np.sqrt(1 + r_y**2 * x**2 / (r_x**4 - r_x**2 * x**2))


def ellipse_arc_length(x1: float, x2: float, r_x: float, r_y: float, atol: float = 1e-3) -> float:
    arc_length, error = quad(lambda x: _upper_ellipse_arc(x, r_x, r_y), x1, x2)

    if error > atol:
        raise RuntimeError(f"Absolute integration error is larger than {atol}")

    return arc_length
