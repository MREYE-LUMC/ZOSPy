"""OpticStudio Solvers.

`zospy.solvers` provides easy access to various solvers offered by OpticStudio.
Solvers have the general structure `solver_function(cell, *args)`, with `cell` the EditorCell of the solver,
followed by the parameters for the solver.

Examples
--------
Make the radius of a surface variable:

>>> surface = oss.InsertNewSurfaceAt(1)
>>> zp.solvers.variable(surface.RadiusCell)

Change the refractive index of a medium:

>>> surface = oss.InsertNewSurfaceAt(1)
>>> zp.solvers.material_model(surface.MaterialCell, refractive_index=1.5)
"""
from __future__ import annotations

from zospy.api import _ZOSAPI, constants


def _get_surface_index(surface: _ZOSAPI.Editors.IEditorRow | int) -> int:
    if isinstance(surface, int):
        return surface
    elif surface.GetType().BaseType.FullName == "ZemaxUI.ZOSAPI.Editors.ZOSAPI_EditorRowBase":
        return surface.RowIndex
    else:
        raise ValueError(f"from_surface should be an int or a Surface, got {surface}")


def element_power(radius_cell: _ZOSAPI.Editors.IEditorCell, power: float) -> _ZOSAPI.Editors.ISolveElementPower:
    """Solver for element power.

    Adjusts the value of `radius_cell` to create an element with the specified `power`. This solver should be set on
    the last surface of the element.

    Parameters
    ----------
    radius_cell : ZOSAPI.Editors.IEditorCell
        Radius cell of the last element surface
    power : float
        Element power in diopters

    Returns
    -------
    solve_data : ZOSAPI.Editors.ISolveElementPower
        The solve data for the element power
    """
    solve_data = radius_cell.CreateSolveType(constants.Editors.SolveType.ElementPower)._S_ElementPower

    # The ZOS-API accepts powers in diopters instead of diopters / 1000
    solve_data.Power = power

    radius_cell.SetSolveData(solve_data)

    return solve_data


def fixed(cell: _ZOSAPI.Editors.IEditorCell) -> _ZOSAPI.Editors.ISolveFixed:
    """Sets the cell solve type to Fixed.

    Parameters
    ----------
    cell: ZOSAPI.Editors.IEditorCell

    Returns
    -------
    The solve data object for `cell`.
    """
    solve_data = cell.CreateSolveType(constants.Editors.SolveType.Fixed)._S_Fixed
    cell.SetSolveData(solve_data)

    return solve_data


def material_model(
    material_cell: _ZOSAPI.Editors.IEditorCell,
    refractive_index: float = 1,
    abbe_number: float = 0,
    partial_dispersion: float = 0,
) -> _ZOSAPI.Editors.ISolveMaterialModel:
    """Solver for material model.

    Sets the material type of a specific LDE surface to model. This solver only works on material cells.

    Parameters
    ----------
    material_cell: ZOSAPI.Editors.IEditorCell
        MaterialCell of the LDE surface row or NCE object row that requires the modification
    refractive_index: float
        Refractive index of the material
    abbe_number: float
        Abbe number of the material
    partial_dispersion: float
        Partial dispersion term at d-light

    Returns
    -------
    The SolveData object for the material model.
    """
    solve_data = material_cell.CreateSolveType(constants.Editors.SolveType.MaterialModel)._S_MaterialModel
    solve_data.IndexNd = refractive_index
    solve_data.AbbeVd = abbe_number
    solve_data.dPgF = partial_dispersion

    material_cell.SetSolveData(solve_data)

    return solve_data


def surface_pickup(
    cell: _ZOSAPI.Editors.IEditorCell,
    from_surface: _ZOSAPI.Editors.IEditorRow | int,
    from_column: _ZOSAPI.Editors.LDE.SurfaceColumn = None,
    scale: float = 1,
    offset: float = 0,
) -> _ZOSAPI.Editors.ISolveSurfacePickup:
    """Picks up the value of `cell` from another surface.

    Parameters
    ----------
    cell: ZOSAPI.Editors.IEditorCell
        Cell for which the value should be set
    from_surface: ZOSAPI.Editors.IEditorRow
        Index of the surface or surface from which the value is picked up
    from_column: float
        Column from which the value is picked up
    scale: float
        Factor by which the picked up value is scaled. This value is only set if the cell supports a scale
        factor. Defaults to 1.
    offset: float
        Offset which is added to the picked up value. This value is only set if the cell supports an offset.
        Defaults to 0.

    Returns
    -------
        The SolveData object for the surface pickup.
    """
    solve_data = cell.CreateSolveType(constants.Editors.SolveType.SurfacePickup)._S_SurfacePickup

    solve_data.Surface = _get_surface_index(from_surface)

    if solve_data.SupportsScale:
        solve_data.ScaleFactor = scale

    if solve_data.SupportsOffset:
        solve_data.Offset = offset

    if from_column is not None:
        solve_data.Column = from_column

    cell.SetSolveData(solve_data)

    return solve_data


def position(
    thickness_cell: _ZOSAPI.Editors.IEditorCell,
    from_surface: _ZOSAPI.Editors.LDE.ILDERow | _ZOSAPI.Editors.NCE.INCERow,
    length: float,
) -> _ZOSAPI.Editors.ISolvePosition:
    """Solver for position.

    Solves the position of `surface` relative to `from_surface`. This solver works only on thickness cells.

    Parameters
    ----------
    thickness_cell: ZOSAPI.Editors.IEditorCell
        Surface for which the position should be set
    from_surface: ZOSAPI.Editors.IEditorRow | int
        Index of the surface or surface from which the position is measured
    length: float
        Distance between `from_surface` and `surface`.

    Returns
    -------
        The SolveData object for the position.
    """
    solve_data = thickness_cell.CreateSolveType(constants.Editors.SolveType.Position)._S_Position

    if isinstance(from_surface, int):
        solve_data.FromSurface = from_surface
    elif type(from_surface).__name__ in ("ILDERow", "INCERow"):
        solve_data.FromSurface = from_surface.RowIndex
    else:
        raise ValueError(f"from_surface should be an int or a Surface, got {from_surface}")

    solve_data.Length = length

    thickness_cell.SetSolveData(solve_data)

    return solve_data


def variable(cell: _ZOSAPI.Editors.IEditorCell) -> _ZOSAPI.Editors.ISolveVariable:
    """Sets the cell solve type to Variable.

    Parameters
    ----------
    cell: ZOSAPI.Editors.IEditorCell

    Returns
    -------
    The solve data object for `cell`.
    """
    solve_data = cell.CreateSolveType(constants.Editors.SolveType.Variable)._S_Variable
    cell.SetSolveData(solve_data)

    return solve_data
