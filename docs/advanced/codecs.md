# Custom object conversion between the ZOS-API and ZOSPy

ZOSPy connects to the ZOS-API using [Python.NET][pythonnet].
Python.NET converts .NET objects to Python objects and vice versa, and it allows to customize this conversion 
behaviour using [codecs].
ZOSPy defines these codecs in {py:class}`zospy.api.codecs` and loads them before loading the ZOS-API libraries in 
{py:class}`zospy.api.apisupport`.

## {py:class}`OpticStudioInterfaceEncoder <zospy.api.codecs.OpticStudioInterfaceEncoder>`

This encoder automatically downcasts generic interfaces to specific implementations.
The ZOS-API often defines a generic interface which is implemented by many other, more specific interfaces.

:::{dropdown} Example
:color: info
:icon: light-bulb

The `ZOSAPI.Analysis.Settings.IAS_` interface specifies the properties and methods that should be 
implemented by the settings object of all analyses.
Many analyses have settings that are specific to that analysis, and these settings are specified by a separate 
interface.
For example, the Huygens PSF settings are specified by the `ZOSAPI.Analysis.Settings.Psf.IAS_HuygensPsf` interface,
which also inherits from `ZOSAPI.Analysis.Settings.IAS_`.
:::

Starting with Python.NET 3, this leads to problems when the API returns objects implementing the generic interface, 
but you need to access a method or property of the specific interface.
The solution to this problem is "downcasting" the generic interface to the specific interface.
Python.NET uses the `__implementation__` attribute for this.
More information can be found on the [OpticStudio community forum][opticstudio-forum].

::::{dropdown} Example
:color: info
:icon: light-bulb

:::{warning}
This example does not work out of the box, because 
{py:class}`zospy.api.codecs.OpticStudioInterfaceEncoder` solves this problem.
You need to modify ZOSPy's source code to get this example working.
:::

If you create a Huygens PSF analysis using the "raw" ZOS-API, you cannot access its analysis specific settings:

```python
import zospy as zp

zos = zp.ZOS()
oss = zos.connect(mode="standalone")

huygens_psf = oss.Analyses.New_Analysis_SettingsFirst(zp.constants.Analysis.AnalysisIDM.HuygensPsf)
huygens_psf_settings = huygens_psf.GetSettings()

print(huygens_psf_settings.Normalize) # AttributeError: 'IAS_' object has no attribute 'Normalize'
```

By downcasting using the `__implementation__` attribute, the Huygens PSF settings can be accessed:

```python
print(huygens_psf_settings.__implementation__.Normalize) # False
```
::::

Manually accessing `__implementation__` is unintuitive, and decreases code readability.
The `OpticStudioInterfaceEncoder` solves this problem by automatically casting from the interface to the implementation
class.

### Interfaces that are automatically downcast

Interfaces need to be registered before they will be converted by `OpticStudioInterfaceEncoder`.
These interfaces are downcast by default:

- `ZOSAPI.Analysis.Settings.IAS_`
  - Access via `zp.analyses.new_analysis(<analysis type>).Settings`
  - Interface for analysis settings. **PLEASE NOTE:** `zospy.analyses` already performed downcasting before codecs were implemented.
- `ZOSAPI.Editors.LDE.ISurface`
  - `oss.LDE.GetSurfaceAt(<index>).SurfaceData`
  - Surface data, which provides access to surface-specific settings (e.g. tilts and decenters of a Coordinate Break)
- `ZOSAPI.Editors.LDE.ISurfaceApertureType`
  - Access via `oss.LDE.GetSurfaceAt(<index>).ApertureData.CurrentTypeSettings`
  - Interface for surface aperture settings
- `ZOSAPI.Editors.LDE.ISurfaceScatteringType`
  - Access via `oss.LDE.GetSurfaceAt(<index>).ScatteringData.CurrentTypeSettings`
  - Interface for surface scattering settings
- `ZOSAPI.Editors.NCE.IObject`
  - `oss.NCE.GetObjectAt(<index>).ObjectData`
  - Object data, which provides access to object-specific settings
- `ZOSAPI.Tools.ISystemTool`
  - `oss.Tools.CurrentTool`
  - Interface for tool settings

### Interfaces that are not automatically downcast

The interfaces listed below provide "convenience properties" to access the specific interfaces.
They are therefore not handled by `OpticStudioInterfaceEncoder`.
Consult the OpticStudio documentation for more information. 

- `ZOSAPI.Editors.ISolveData`
- `ZOSAPI.Editors.NCE.ISourceColorSettings`
- `ZOSAPI.Editors.NCE.IObjectScatteringSettings`
- `ZOSAPI.Editors.NCE.IVolumePhysicsModelSettings`
- `ZOSAPI.Editors.NCE.IIndexModelSettings`

:::{dropdown} Example
:color: info
:icon: light-bulb

The 'Pickup' solver, which implements the `ZOSAPI.Editors.ISolveSurfacePickup` interface, can be accessed in this way:

```python
# ThicknessCell is only an example, you can use any cell that supports the Pickup solver
oss.LDE.GetSurfaceAt(<index>).ThicknessCell.GetSolveData()._S_SurfacePickup
```
:::

### Registering additional interfaces for automatic downcasting

You can register additional interfaces using 
{py:class}`zospy.api.codecs.OpticStudioInterfaceEncoder.register_interfaces`.
If you think you found an interface that should be converted by default, please file an issue or create a Pull Request.

[pythonnet]: https://pythonnet.github.io/
[codecs]: https://pythonnet.github.io/pythonnet/codecs.html
[opticstudio-forum]: https://community.zemax.com/zos-api-12/pythonnet-3-x-is-fixed-3945
