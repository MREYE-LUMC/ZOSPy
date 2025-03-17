"""Old-style OpticStudio Analyses.

.. deprecated:: 2.0.0
    The `zospy.analyses.old` contains the deprecated analysis API. Migrate your analyses to the new format.

Analyses in OpticStudio are available through `zospy.analyses.old`.
These analyses are present for compatibility reasons. It is recommended to use the new analysis API.

Examples
--------
Run a Single Ray Trace analysis:

>>> from zospy.analyses.old.wavefront import zernike_standard_coefficients
>>> zernike_standard_coefficients(oss, sampling="32x32", maximum_term=15)

Open an analysis for which a wrapper function is not yet available:

>>> import zospy as zp
>>> analysis = zp.analyses.new_analysis(
...     oss, zp.constants.Analysis.AnalysisIDM.ImageSimulation
... )
"""

from warnings import warn

from zospy.analyses.old import (
    extendedscene,
    mtf,
    physicaloptics,
    polarization,
    psf,
    raysandspots,
    reports,
    surface,
    systemviewers,
    wavefront,
)
from zospy.analyses.old.base import OnComplete, new_analysis

__all__ = (
    "extendedscene",
    "mtf",
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

warn("The `zospy.analyses.old` module contains the deprecated analysis API. Migrate your analyses to the new format.", DeprecationWarning)
