import pytest

import zospy as zp
from zospy import solvers
from zospy.api.config import DECIMAL_POINT


def test_element_power(simple_system):
    lens_back = simple_system.LDE.GetSurfaceAt(3)

    solvers.element_power(lens_back.RadiusCell, power=40)

    assert lens_back.RadiusCell.GetSolveData().Type == zp.constants.Editors.SolveType.ElementPower
    assert lens_back.Radius != -20


def test_fixed(simple_system):
    lens_back = simple_system.LDE.GetSurfaceAt(3)

    solvers.fixed(lens_back.RadiusCell)

    assert lens_back.RadiusCell.GetSolveData().Type == zp.constants.Editors.SolveType.Fixed


def test_material_model(simple_system):
    lens_front = simple_system.LDE.GetSurfaceAt(2)

    solvers.material_model(lens_front.MaterialCell, refractive_index=2.0, abbe_number=1, partial_dispersion=0)

    assert lens_front.MaterialCell.GetSolveData().Type == zp.constants.Editors.SolveType.MaterialModel
    assert lens_front.Material == f"2{DECIMAL_POINT}00,1,0"


@pytest.mark.parametrize("from_column,scale,offset", [(None, 1, 0), ("Radius", 2, 1)])
def test_surface_pickup(simple_system, from_column, scale, offset):
    lens_front = simple_system.LDE.GetSurfaceAt(2)
    lens_back = simple_system.LDE.GetSurfaceAt(3)

    solvers.surface_pickup(lens_back.ThicknessCell, lens_front, from_column, scale, offset)

    assert lens_back.ThicknessCell.GetSolveData().Type == zp.constants.Editors.SolveType.SurfacePickup

    if from_column is None:
        assert lens_back.Thickness == lens_front.Thickness
    else:
        assert (
            lens_back.Thickness
            == lens_front.GetSurfaceCell(getattr(zp.constants.Editors.LDE.SurfaceColumn, from_column)).DoubleValue
            * scale
            + offset
        )


def test_pickup_chief_ray(coordinate_break_system):
    coordinate_break = coordinate_break_system.LDE.GetSurfaceAt(4)

    solvers.pickup_chief_ray(coordinate_break.SurfaceData.Decenter_X_Cell)

    assert (
        coordinate_break.SurfaceData.Decenter_X_Cell.GetSolveData().Type
        == zp.constants.Editors.SolveType.PickupChiefRay
    )
    assert coordinate_break.SurfaceData.Decenter_X <= 1e-3


def test_position(simple_system):
    length = 50

    stop = simple_system.LDE.GetSurfaceAt(2)
    lens_back = simple_system.LDE.GetSurfaceAt(3)

    solvers.position(lens_back.ThicknessCell, from_surface=stop, length=length)

    assert lens_back.ThicknessCell.GetSolveData().Type == zp.constants.Editors.SolveType.Position
    assert sum(simple_system.LDE.GetSurfaceAt(i).Thickness for i in range(1, 4)) == length


def test_variable(simple_system):
    lens_back = simple_system.LDE.GetSurfaceAt(3)

    solvers.variable(lens_back.RadiusCell)

    assert lens_back.RadiusCell.GetSolveData().Type == zp.constants.Editors.SolveType.Variable
