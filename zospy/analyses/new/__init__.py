"""OpticStudio Analyses.

Analyses in OpticStudio are available through `zospy.analyses`.
This module provides basic classes and functions for interacting with
analyses (in `zospy.analyses.base`), as well as a procedural interface
to several analyses.

Examples
--------
Run a Single Ray Trace analysis:

>>> from zospy.analyses.new.wavefront import ZernikeStandardCoefficients
>>> ZernikeStandardCoefficients(sampling="32x32", maximum_term=15).run(oss)

Open an analysis for which a wrapper function is not yet available:

>>> import zospy as zp
>>> analysis = zp.analyses.new_analysis(
...     oss, zp.constants.Analysis.AnalysisIDM.ImageSimulation
... )
"""

from zospy.analyses.new import (
    mtf,
    physicaloptics,
    polarization,
    raysandspots,
    reports,
    surface,
    systemviewers,
    wavefront,
)

__all__ = (
    "mtf",
    "physicaloptics",
    "polarization",
    "raysandspots",
    "reports",
    "surface",
    "systemviewers",
    "wavefront",
)
