# Creating an optical system

The {py:class}`OpticStudioSystem <zospy.zpcore.OpticStudioSystem>` object `oss` that has been created in [](01_connection.md)
can be used to control the connected OpticStudio instance from Python.
This object exposes the ZOS-API namespaces as attributes.
Documenting these namespaces is not the intention of this documentation, because they are already well-documented in the
OpticStudio help files.

To create and modify a sequential optical system, the Lens Data Editor can be accessed through the 
{py:attr}`oss.LDE <zospy.zpcore.OpticStudioSystem.LDE>` attribute.

## Example

```python
import zospy as zp

# Connect to OpticStudio
zos = zp.ZOS()
oss = zos.connect()

# Create a new, empty system
oss.new()

# Insert a new surface at index 1 and adjust its radius and thickness
surface_1 = oss.LDE.InsertNewSurfaceAt(1)
surface_1.Radius = 10
surface_1.Thickness = 5

# Get the STOP surface and adjust its semi-diameter
surface_stop = oss.LDE.GetSurfaceAt(oss.LDE.StopSurface)
surface_stop.SemiDiameter = 2
```

## Using solvers

OpticStudio allows to dynamically set surface properties using solvers.
ZOSPy exposes these solvers through the {py:mod}`zospy.solvers` module.
The below example shows how to use the {py:func}`position <zospy.solvers.position>` solver to set the thickness of a surface,
and the {py:func}`material_model <zospy.solvers.material_model>` solver to set the refractive index of a material.

```python
import zospy as zp

# Connect to OpticStudio
zos = zp.ZOS()
oss = zos.connect()

surface = oss.LDE.GetSurfaceAt(2)
zp.solvers.position(surface.ThicknessCell, from_surface=oss.LDE.GetSurfaceAt(1), length=10)
zp.solvers.material_model(surface.MaterialCell, refractive_index=1.5)
```

## Contributing solvers

OpticStudio has many solvers, and not all of them are implemented in ZOSPy (yet).
If you want to use a solver that is not implemented, consider [contributing](../contributing/contributing.md) it to ZOSPy.
All solvers follow the same structure, and writing a new one is straightforward.
Here is an example for a solver that sets the power of an element:

```python
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
    
    # Create an OpticStudio solve data object
    solve_data = radius_cell.CreateSolveType(zp.constants.Editors.SolveType.ElementPower)._S_ElementPower

    # Apply the settings to the solve data
    solve_data.Power = power

    # Add the solve data to the Lens Data Editor cell
    radius_cell.SetSolveData(solve_data)

    return solve_data
```
