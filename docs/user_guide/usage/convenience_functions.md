# Convenience functions

The {py:mod}`zospy.functions` module contains functions that are not directly related to the OpticStudio API, but provide 
useful functionality for working with OpticStudio. 
These functions are organized in submodules, such as {py:mod}`zospy.functions.lde` for functions related to the 
Lens Data Editor, and {py:mod}`zospy.functions.nce` for functions related to the Non-sequential Component Editor.

## Example

Use {py:func}`zospy.functions.lde.surface_change_type` to change the type of a surface:

```python
import zospy as zp

zos = zp.ZOS()
oss = zos.connect()

surface = oss.LDE.InsertNewSurfaceAt(1)
zp.functions.lde.surface_change_type(surface, zp.constants.Editors.LDE.SurfaceType.ZernikeStandardSag)
```
