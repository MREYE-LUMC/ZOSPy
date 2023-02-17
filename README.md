# ZOSPy

## About
Wrapper around the [Zemax OpticStudio](https://www.zemax.com/pages/opticstudio) API that provides a more pythonic and intuitive way to interact with the ZOS-API through python using a .NET connection. It also takes care of initiating the connection.

## Waranty and liability
The code is provided as is, without any warranty. It is solely intended for research purposes. No warranty is given and no rights can be derived from it, as is also stated in the [GNU General Public License Version 3](https://github.com/MREYE-LUMC/ZOSPy/blob/b26c2627d625f19545159dbf938847a9ebaf5a67/LICENSE.txt).

## Installing

ZOSPy is available on PyPi

```
pip install zospy
```

## Dependencies
### Python packages
- [Python for .NET](http://pythonnet.github.io/) (tested with version 2.5.2)
   > **Warning**: _(Oktober 2022)_
   Some functions of the ZOS-API do not work with the newest available version of Pythonnet (version 3.0.1). See https://github.com/MREYE-LUMC/ZOSPy/issues/9 for more information. Therefore, the required version of pythonnet has been set to version 2.5.2 as this seems to work fine. Upon running into similar errors, please check the installed pythonnet version. We are working on a solution for this problem.

- [pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)

### Software
- [Zemax OpticStudio](https://www.zemax.com/pages/opticstudio) (Tested with version 20.3.2)

## Referencing
When publishing results obtained with this package, please cite the paper in which the package was first used:<br>
van Vught L, Que I, Luyten GPM and Beenakker JWM.
_Effect of anatomical differences and intraocular lens design on Negative Dysphotopsia._
JCRS: Sep 06, 2022.
[doi: [10.1097/j.jcrs.0000000000001054](https://doi.org/10.1097/j.jcrs.0000000000001054) ] [[JCRS](https://journals.lww.com/jcrs/Abstract/9900/Effect_of_anatomical_differences_and_intraocular.107.aspx)]

If a direct reference of the package is also required, reference it using the following DOI:<br>
[![DOI](https://zenodo.org/badge/403590410.svg)](https://zenodo.org/badge/latestdoi/403590410)

## Basic usage
### Initiating connection
The connection as extension to running software OpticStudio is initiated as:

```python
import zospy as zp
zos = zp.ZOS()
zos.wakeup()
zos.connect_as_extension(0)
oss = zos.get_primary_system()
```
Make sure that the OpticStudio software is setup to be connected to as extension through the API. Alternatively, a standalone OpticStudio application can be launched by changing the last two lines to:

```python
zos.create_new_application()
oss = zos.get_primary_system()
```

### Performing analyses
Implemented analyses are are available though `zp.analyses`. The available analyses are grouped in files that correspond to the analysis groups in OpticStudio (e.g. `zp.analyses.mtf`and `zp.analyses.wavefront`). Every analysis requires the OptiStudioSystem `oss` as first parameter.

> **Note**:
> Up to version 0.6.0, some analyses where directly available through the OpticStudioSystem (`oss`) class. This has been changed as the namespace became cluttered.

#### Examples
```python
from zp.analyses.mtf import fft_through_focus_mtf
mtf = fft_through_focus_mtf(oss, sampling='64x64', deltafocus=0.1, oncomplete='Close')
```

```python
from zp.analyses.reports import cardinal_points
cp = cardinal_points(oss, surf1=3, surf2=4, oncomplete='Release')
```

A full description of the available function parameters is provided in the docstrings.


### Constants
After initiating the connection, all api constants are available through `zp.constants` (e.g. `zp.constants.Editors.LDE.SurfaceType`). Note that that are only available after `zos.wakeup() is called as defined under **Initiating connection**.


### Convenient functions
Some conventiant functions are available through `zp.functions`, e.g. to change a surface to a standard stuface:

```python
newsurf = oss.LDE.InsertNewSurfaceAt(0)
zp.functions.lde.surface_change_type(newsurf, 'Standard')
```

### Logging
Some basic logging is implemented through the standard [python logging module](https://docs.python.org/3/library/logging.html) (but still under development). The following implementation examples assume that `import logging` is executed.

1. To enable logging output from all ZOSPy and other modules using logging.basicConfig:
    ```python
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ```
2. To enable logging output from all ZOSPy and other modules using a root logger:
    ```python
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.addHandler(sh)
    ```
3. To enable logging output from only ZOSPy
    ```python
    logging.getLogger('zospy').addHandler(logging.StreamHandler())
    logging.getLogger('zospy').setLevel(logging.INFO)
    ```

## Contact
Feel free to contact us for any inquiries:
- L. van Vught ([email](mailto:l.van_vught@lumc.nl))
- J.W.M. Beenakker ([email](mailto:j.w.m.beenakker@lumc.nl))
