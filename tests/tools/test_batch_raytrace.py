from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import zospy as zp
from zospy.tools import BatchRayTraceNormUnpol

if TYPE_CHECKING:
    from zospy.zpcore import OpticStudioSystem


RAY_COORDINATES = [(0, 0), (0.5, 0.5), (-0.5, 0.5), (1, 1), (-1, -1)]
PUPIL_COORDINATES = [(0, 0), (0, 0), (-1, -1), (0.5, 0.5), (0, 0)]
EXPECTED_DATA = """
rayNumber,ErrorCode,vignetteCode,X,Y,Z,L,M,N,l2,m2,n2,opd,intensity
1,0,0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,-1.0,21.292,1.0
2,0,0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,-1.0,21.292,1.0
3,0,0,0.0061213962871815575,0.0061213962871815575,0.0,0.04982748996703953,0.04982748996703953,0.997514131472416,0.0,0.0,-1.0,21.29250706701466,1.0
4,0,0,-1.180861838340208e-05,-1.180861838340208e-05,0.0,-0.024821950654654583,-0.024821950654654583,0.9993836808410451,0.0,0.0,-1.0,21.292012741140418,1.0
5,0,0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,-1.0,21.292,1.0
"""


def test_batch_ray_trace_norm_unpol(simple_system: OpticStudioSystem):
    tool = BatchRayTraceNormUnpol(
        hx=[c[0] for c in RAY_COORDINATES],
        hy=[c[1] for c in RAY_COORDINATES],
        px=[c[0] for c in PUPIL_COORDINATES],
        py=[c[1] for c in PUPIL_COORDINATES],
    )

    result = tool.run(simple_system)

    # Compare the actual result with the expected data
    assert_frame_equal(result.data, pd.read_csv(StringIO(EXPECTED_DATA)))


@pytest.mark.parametrize(
    "surface, expected_coordinate",
    [
        (1, (0.0, 0.5, 0.0)),  # Stop surface
        (2, (0.0, 0.50124164265831, 0.006282066217268977)),  # Lens front surface
        (3, (0.0, 0.6209696175613508, -0.009642406048217225)),  # Lens back surface
        (4, (0.0, 3.944854065030327, 0.0)),  # Image surface
        ("Image", (0.0, 3.944854065030327, 0.0)),  # Image surface
    ],
)
def test_batch_ray_trace_norm_unpol_surface(
    decentered_system: OpticStudioSystem,
    surface: int | Literal["Image"],
    expected_coordinate: tuple[float, float, float],
):
    tool = BatchRayTraceNormUnpol(
        hx=[0.0],
        hy=[0.5],
        px=[0.0],
        py=[0.5],
        surface=surface,
    )

    result = tool.run(decentered_system)

    # Check that the coordinates of the first ray match the expected values
    assert np.allclose(result.data.loc[0, ["X", "Y", "Z"]].values, expected_coordinate)


@pytest.mark.parametrize(
    "wavelength, expected_coordinate",
    [
        (1, (0.0, 3.9220149310491603, 0)),  # Wavelength 1
        (2, (0.0, 3.926593029532985, 0)),  # Wavelength 2
    ],
)
def test_batch_ray_trace_norm_unpol_wavelength(
    decentered_system: OpticStudioSystem, wavelength: int, expected_coordinate: tuple[float, float, float]
):
    decentered_system.SystemData.Wavelengths.AddWavelength(0.6328, 1.0)  # Add a second wavelength to the system
    zp.solvers.fixed(
        decentered_system.LDE.GetSurfaceAt(2).MaterialCell
    )  # Use a material that has a different refractive index at the second wavelength
    decentered_system.LDE.GetSurfaceAt(2).Material = "BK7"

    tool = BatchRayTraceNormUnpol(
        hx=[0.0],
        hy=[0.5],
        px=[0.0],
        py=[0.5],
        wavelength=wavelength,
    )

    result = tool.run(decentered_system)

    # Check that the coordinates of the first ray match the expected values for the specified wavelength
    assert np.allclose(result.data.loc[0, ["X", "Y", "Z"]].values, expected_coordinate)
