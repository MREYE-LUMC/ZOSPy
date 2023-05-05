"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

from . import QuickYield

__all__ = ("QuickYield", "QYCompensations", "QYCompensatorStrategy", "QYPrecisions")

class QYCompensations(Enum):
    Standard = 0
    High = 1
    VeryHigh = 2

class QYCompensatorStrategy(Enum):
    OptimizeAllDampedLeastSquares = 0
    ParaxialFocus = 1
    Ignore = 2
    OptimizeAllOrthogonalDescent = 3

class QYPrecisions(Enum):
    Standard = 0
    High = 1
    VeryHigh = 2
