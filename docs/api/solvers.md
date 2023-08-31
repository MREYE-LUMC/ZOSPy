# Solvers

ZOSPy provides easy access to various solvers offered by OpticStudio.
These are available in `zospy.solvers`.

## Examples

Make the radius of a surface variable:

```python
surface = oss.InsertNewSurfaceAt(1)

zp.solvers.variable(surface.RadiusCell)
```

Change the refractive index of a medium:

```python
surface = oss.InsertNewSurfaceAt(1)

zp.solvers.material_model(surface.MaterialCell, refractive_index=1.5)
```

## Documentation

```{eval-rst}
.. automodule:: zospy.solvers
   :members:
```