"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("OptimizationAlgorithm", "OptimizationCycles", "OptimizationSaveCount")

class OptimizationAlgorithm(Enum):
    DampedLeastSquares = 0
    OrthogonalDescent = 1

class OptimizationCycles(Enum):
    Automatic = 0
    Fixed_1_Cycle = 1
    Fixed_5_Cycles = 2
    Fixed_10_Cycles = 3
    Fixed_50_Cycles = 4
    Infinite = 5

class OptimizationSaveCount(Enum):
    Save_10 = 0
    Save_20 = 1
    Save_30 = 2
    Save_40 = 3
    Save_50 = 4
    Save_60 = 5
    Save_70 = 6
    Save_80 = 7
    Save_90 = 8
    Save_100 = 9
