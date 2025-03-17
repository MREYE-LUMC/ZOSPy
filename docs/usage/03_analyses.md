# Performing analyses

ZOSPy provides analysis wrappers for OpticStudio analyses in {py:mod}`zospy.analyses`.
These wrappers provide a consistent and more Pythonic interface to OpticStudio analyses.
Furthermore, they parse the output of the analyses into Python objects for easier access.
The available analyses are grouped in files that correspond to
the analysis groups in OpticStudio (e.g. {py:mod}`zospy.analyses.mtf`and {py:mod}`zospy.analyses.wavefront`).
An overview of the available analyses can be found in the [API reference](../api/zospy.analyses.rst).

## Analysis wrapper structure

Every analysis wrapper is a class which accepts the analysis settings as its arguments.
To run the analysis, the {py:meth}`run <zospy.analyses.base.BaseAnalysisWrapper.run>` method is called with the 
OpticStudioSystem `oss` as its argument.
This method also has an optional {py:type}`oncomplete <zospy.analyses.base.OnComplete>` argument, which specifies what to 
do after the analysis has finished.
Every analysis wrapper has a corresponding settings class as well, allowing to define the analysis settings separately
from creating the analysis object.
This is illustrated in the [examples below](#analysis-with-settings).

## Examples

Run an FFT through-focus MTF analysis with a sampling of 64x64 and a focus step of 0.1:

```python
import zospy as zp

zos = zp.ZOS()
oss = zos.connect()

...

mtf = zp.analyses.mtf.FFTThroughFocusMTF(sampling="64x64", delta_focus=0.1).run(oss, oncomplete="Close")
```

{#analysis-with-settings}
Create a settings object for a cardinal points analysis between surfaces 3 and 4, and run the analysis:

```python
import zospy as zp

zos = zp.ZOS()
oss = zos.connect()

...

cardinal_points_settings = zp.analyses.reports.CardinalPointsSettings(surface_1=3, surface_2=4)
cardinal_points = zp.analyses.reports.CardinalPoints.with_settings(cardinal_points_settings).run(oss)
```

## Accessing OpticStudio analyses directly

If you want to run an analysis that is not implemented in ZOSPy, you can access the OpticStudio analysis directly using
{py:func}`zp.analyses.new_analysis <zospy.analyses.base.new_analysis>`.
The analysis type has to be specified as a [ZOSPy constant](04_constants.md), for example:

```python
import zospy as zp

zos = zp.ZOS()
oss = zos.connect()

...

analysis = zp.analyses.new_analysis(oss, zp.constants.Analysis.AnalysisIDM.PathAnalysis, settings_first=True)

# Adjust the settings of the analysis
analysis.Settings.FirstRay = 1

# Run the analysis
analysis.ApplyAndWaitForCompletion()
```

If `settings_first=True`, the analysis is created without running it, allowing you to adjust the settings before running it.

:::{tip}
If you wrote code to access an OpticStudio analysis directly, consider [contributing](../contributing/developing_analyses.md) it to ZOSPy.
:::