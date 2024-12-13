"""OpticStudio Analyses.

Analyses in OpticStudio are available through `zospy.analyses`.
This module provides basic classes and functions for interacting with
analyses (in `zospy.analyses.base`), as well as a procedural interface
to several analyses.

Examples
--------
Run a Single Ray Trace analysis:

>>> from zospy.analyses.wavefront import zernike_standard_coefficients
>>> zernike_standard_coefficients(oss, sampling="32x32", maximum_term=15)

Open an analysis for which a wrapper function is not yet available:

>>> import zospy as zp
>>> analysis = zp.analyses.new_analysis(oss, zp.constants.Analysis.AnalysisIDM.ImageSimulation)
"""

from zospy.analyses import (
    extendedscene,
    mtf,
    new,
    physicaloptics,
    polarization,
    psf,
    raysandspots,
    reports,
    surface,
    systemviewers,
    wavefront,
)
from zospy.analyses.base import OnComplete, new_analysis

__all__ = (
    "extendedscene",
    "mtf",
    "new",
    "physicaloptics",
    "psf",
    "reports",
    "raysandspots",
    "polarization",
    "surface",
    "systemviewers",
    "wavefront",
    "new_analysis",
    "OnComplete",
)
