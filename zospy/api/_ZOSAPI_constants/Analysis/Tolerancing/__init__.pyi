"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations
from . import QuickYield

__all__ = ("QuickYield", "QYCompensations", "QYCompensatorStrategy", "QYPrecisions", "ShowAsISO")

class QYCompensations:
    Standard: QYCompensations = None
    High: QYCompensations = None
    VeryHigh: QYCompensations = None

class QYCompensatorStrategy:
    OptimizeAllDampedLeastSquares: QYCompensatorStrategy = None
    ParaxialFocus: QYCompensatorStrategy = None
    Ignore: QYCompensatorStrategy = None
    OptimizeAllOrthogonalDescent: QYCompensatorStrategy = None

class QYPrecisions:
    Standard: QYPrecisions = None
    High: QYPrecisions = None
    VeryHigh: QYPrecisions = None

class ShowAsISO:
    Surface: ShowAsISO = None
    Singlet: ShowAsISO = None
    Doublet: ShowAsISO = None
