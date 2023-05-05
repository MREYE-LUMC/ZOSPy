"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("ISAberrationTypes", "ISFlipTypes", "ISSamplings", "ISShowAsTypes")

class ISAberrationTypes(Enum):
    None_ = 0
    Geometric = 1
    Diffraction = 2

class ISFlipTypes(Enum):
    None_ = 0
    TopBottom = 1
    LeftRight = 2
    TopBottomLeftRight = 3

class ISSamplings(Enum):
    None_ = 0
    X2 = 1
    X4 = 2
    X8 = 3
    X16 = 4
    X32 = 5
    X64 = 6

class ISShowAsTypes(Enum):
    SimulatedImage = 0
    SourceBitmap = 1
    PSFGrid = 2
