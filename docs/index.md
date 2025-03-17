# Welcome to ZOSPy's documentation!

[![PyPI - Version](https://img.shields.io/pypi/v/ZOSPy)](https://pypi.org/project/zospy)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FMREYE-LUMC%2FZOSPy%2Fmain%2Fpyproject.toml)
[![Conda Version](https://img.shields.io/conda/v/conda-forge/zospy)](https://anaconda.org/conda-forge/zospy)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/MREYE-LUMC/ZOSPy/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/zospy/badge/?version=latest)](https://zospy.readthedocs.io/en/latest/?badge=latest)
[![JOSS](https://joss.theoj.org/papers/10.21105/joss.05756/status.svg)][joss-paper]
[![Zenodo](https://zenodo.org/badge/403590410.svg)](https://zenodo.org/badge/latestdoi/403590410)

ZOSPy is a wrapper around the [Ansys OpticStudio][opticstudio] API that provides a more intuitive way to interact with the 
[ZOS-API][zos-api] through Python using a .NET connection, as described in [this Journal of Open Source Software paper][joss-paper].
It thereby allows you to do more optics modelling with less coding.

In addition to full access to all the OpticStudio functions through the ZOS-API, ZOSPy provides the following features:

- Wrapper functions for several OpticStudio analyses in `zospy.analyses`;
- Easy access to solvers in `zospy.solvers`;
- Easy access to all API constants in `zospy.constants`;
- Autocomplete for all ZOS-API endpoints and constants;
- Solves common problems related to Python.NET 3 and interaction with the ZOS-API. 

## Compatibility

ZOSPy officially supports Python {{ PYTHON_VERSIONS }}. It may work with older Python versions, but support is not provided for
these versions. Furthermore, a working installation of [Ansys Zemax OpticStudio](https://www.zemax.com/pages/opticstudio) is required.

See the below table for compatibility with different versions of Ansys Zemax OpticStudio.
More information on compatibility can be found in the [compatibility](compatibility.md) section.

```{include} compatibility_table.md
```

## Warranty and liability

The code is provided as is, without any warranty. It is solely intended for research purposes. No warranty is given and
no rights can be derived from it, as is also stated in the [MIT license](license.md).

(referencing)=
## Referencing

When publishing results obtained with this package, please cite [our paper][joss-paper] 
in the Journal of Open Source Software:  

> Vught, L. van, Haasjes, C. & Beenakker, J.W.M. (2024). 
> ZOSPy: Optical ray tracing in Python through OpticStudio. 
> Journal of Open Source Software, 9(96), 5756. 
> https://doi.org/10.21105/joss.05756

## Contact

Feel free to contact us via e-mail at [zospy@mreye.nl](mailto:zospy@mreye.nl) for any inquiries,
or visit [mreye.nl](https://mreye.nl) to discover our research.

```{toctree}
:maxdepth: 1
:caption: Getting started

installation
simple_example
faq
```

```{toctree}
:maxdepth: 1
:caption: Usage
:glob:

usage/*
compatibility
```

```{toctree}
:maxdepth: 1
:caption: Examples

examples/introduction
examples/Simple thick lens/Simple thick lens
examples/Escudero-Sanz eye model/Escudero-Sanz eye model
examples/Retinal illumination in pseudophakic eyes with and without Negative Dysphotopsia/retinal_illumination
examples/Ray trace Double Gauss/raytrace_double_gauss
examples/Polarization Prism/polarization_prism_example
examples/Modelling of a Shack-Hartmann Sensor for eye aberration evaluation/README
examples/Patient-specific mapping of fundus photographs to three-dimensional ocular imaging/README
```

```{toctree}
:maxdepth: 1
:caption: Advanced usage

advanced/logging
advanced/codecs
```

```{toctree}
:maxdepth: 2
:caption: Contributing

contributing/contributing
contributing/developing_analyses
contributing/unit_tests
```

```{eval-rst}
.. currentmodule:: zospy

.. autosummary::
   :toctree: api
   :caption: API reference
   :template: custom-module.rst
   :recursive:

   zospy.zpcore
   zospy.analyses
   zospy.api.constants
   zospy.api.codecs
   zospy.functions
   zospy.solvers
```

```{toctree}
:maxdepth: 1
:caption: About

license
changelog
contact
```

[opticstudio]: https://www.ansys.com/products/optics/ansys-zemax-opticstudio
[zos-api]: https://support.zemax.com/hc/en-us/articles/1500005578742-Basic-method-of-performing-system-analysis-in-ZOS-API
[joss-paper]: https://joss.theoj.org/papers/10.21105/joss.05756