# Using ZOS-API constants

All api constants are available through {py:mod}`zospy.constants <zospy.api.constants>`. 
Note that these are only available after initiating the ZOS-API connection, i.e. an instance of 
{py:class}`zospy.ZOS <zospy.zpcore.ZOS>` has been created (see [](01_connection.md)).

For example, the `Editors.LDE.SurfaceType` constant is available as `zospy.constants.Editors.LDE.SurfaceType`:

{emphasize-lines="3, 5"}
```python
import zospy as zp

zos = zp.ZOS() # <-- Constants are only available after creating a ZOS instance

print(zp.constants.Editors.LDE.SurfaceType.Standard)
```