# ZOSPy

[![PyPI - Version](https://img.shields.io/pypi/v/ZOSPy)](https://pypi.org/project/zospy)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FMREYE-LUMC%2FZOSPy%2Fmain%2Fpyproject.toml)
[![Conda Version](https://img.shields.io/conda/v/conda-forge/zospy)](https://anaconda.org/conda-forge/zospy)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/MREYE-LUMC/ZOSPy/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/zospy/badge/?version=latest)](https://zospy.readthedocs.io/en/latest/?badge=latest)

## About

Wrapper around the [Ansys Zemax OpticStudio](https://www.zemax.com/pages/opticstudio) API that provides a more pythonic and
intuitive way to interact with the [ZOS-API](https://www.zemax.com/blogs/free-tutorials/getting-started-with-zos-api)
through python using a .NET connection. It thereby allows you to do more
optics modelling with less coding.

In addition to full access to all the OpticStudio fucntions through the ZOS-API, ZOSPy provides the following features:

- Wrapper functions for several OpticStudio analyses in `zospy.analyses`;
- Easy access to solvers in `zospy.solvers`;
- Easy access to all API constants in `zospy.constants`;
- Autocomplete for all ZOS-API endpoints and constants;
- Solves common problems related to Python.NET 3 and interaction with the ZOS-API. 

## Waranty and liability

The code is provided as is, without any warranty. It is solely intended for research purposes. No warranty is given and
no rights can be derived from it, as is also stated in the [MIT license](LICENSE.txt).

## Installing

ZOSPy is available on PyPi

```
pip install zospy
```

And through conda:

```
conda install conda-forge::zospy
```

## Dependencies

ZOSPy officially supports Python 3.9 - 3.12. It may work with older Python versions, but support is not provided for
these versions.

### Python packages

- [Python for .NET](http://pythonnet.github.io/) 3.0.3
- [pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [SemVer](https://python-semver.readthedocs.io/en/latest/index.html) 3.0.2

### Software

- [Ansys Zemax OpticStudio](https://www.zemax.com/pages/opticstudio)

### Compatibility

ZOSPy is tested with the following versions of Python and Ansys Zemax OpticStudio:

| Zemax       | 20.3.2 | 23.1.0 | 23.2.1 | 24.1.0 |
|-------------|--------|--------|--------|--------|
| Python 3.9  | ⚠      | ✔      | ✔      | ✔      |
| Python 3.10 | ⚠      | ✔      | ✔      | ✔      |
| Python 3.11 | ⚠      | ✔      | ✔      | ✔      |
| Python 3.12 | ⚠      |        |        | ✔      |

✔: This version works without problems.
⚠: This version works, but the output of analyses can differ slightly from the used reference version (currently **OpticStudio 23 R1.01**).

## Referencing

When publishing results obtained with this package, please cite the paper in which the package was first used:<br>
van Vught L, Que I, Luyten GPM and Beenakker JWM.
_Effect of anatomical differences and intraocular lens design on Negative Dysphotopsia._
JCRS: Sep 06, 2022.
[doi: [10.1097/j.jcrs.0000000000001054](https://doi.org/10.1097/j.jcrs.0000000000001054) ] [[JCRS](https://journals.lww.com/jcrs/Abstract/9900/Effect_of_anatomical_differences_and_intraocular.107.aspx)]

If a direct reference of the package is also required, reference it using the following DOI:<br>
[![DOI](https://zenodo.org/badge/403590410.svg)](https://zenodo.org/badge/latestdoi/403590410)

## Contributing

Please read our [contribution guidelines](CONTRIBUTING.md) prior to opening a Pull Request.

## Basic usage

### Initiating connection

The connection as extension to running software OpticStudio is initiated as:

```python
import zospy as zp

zos = zp.ZOS()
oss = zos.connect("extension")
```

Make sure that the OpticStudio software is set up to be connected to as extension through the API. Alternatively, a
standalone OpticStudio application can be launched by changing the last line to:

```python
oss = zos.connect("standalone")
```

### Using solvers

Solvers for the Lens Data Editor are available through `zp.solvers`. Every solver requires a surface as its first
parameter.

#### Examples

```python
import zospy.solvers as solvers

surface = oss.LDE.GetSurfaceAt(2)
solvers.position(surface.ThicknessCell, from_surface=1, length=10)
```

### Performing analyses

Implemented analyses are available though `zp.analyses`. The available analyses are grouped in files that correspond to
the analysis groups in OpticStudio (e.g. `zp.analyses.mtf`and `zp.analyses.wavefront`). Every analysis requires the
OpticStudioSystem `oss` as first parameter.

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

After initiating the connection, all api constants are available through `zp.constants` (
e.g. `zp.constants.Editors.LDE.SurfaceType`). Note that these are only available after `zos.wakeup()` has been called,
as explained under **Initiating connection**.

### Convenience functions

Some convenience functions are available through `zp.functions`, e.g. to change a surface to a standard stuface:

```python
newsurf = oss.LDE.InsertNewSurfaceAt(0)
zp.functions.lde.surface_change_type(newsurf, 'Standard')
```

### Full example

This example creates a simple optical system consisting of a single lens.

```python
# Create a new, empty system
oss.new()

# Set aperture and wavelength
oss.SystemData.Aperture.ApertureType = zp.constants.SystemData.ZemaxApertureType.FloatByStopSize
oss.SystemData.Wavelengths.GetWavelength(1).Wavelength = 0.543  # in μm

# Set the object at infinity
surface_object = oss.LDE.GetSurfaceAt(0)
surface_object.Thickness = float("inf")

# Use a very small stop size, so the system is approximately paraxial
surface_stop = oss.LDE.GetSurfaceAt(1)
surface_stop.SemiDiameter = 0.1

# Add a lens with n = 1.5
lens_front = oss.LDE.InsertNewSurfaceAt(2)
lens_front.Comment = "lens front"
lens_front.Radius = 20
lens_front.Thickness = 1
zp.solvers.material_model(lens_front.MaterialCell, refractive_index=1.5)

lens_back = oss.LDE.InsertNewSurfaceAt(3)
lens_back.Comment = "lens back"
lens_back.Radius = -20
lens_back.Thickness = 19.792  # System is in focus
```

### Logging

Some basic logging is implemented through the
standard [python logging module](https://docs.python.org/3/library/logging.html) (but still under development). The
following implementation examples assume that `import logging` has been executed.

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

- C. Haasjes ([email](mailto:c.haasjes@lumc.nl))
- J.W.M. Beenakker ([email](mailto:j.w.m.beenakker@lumc.nl))
- L. van Vught ([email](mailto:l.van_vught@lumc.nl))