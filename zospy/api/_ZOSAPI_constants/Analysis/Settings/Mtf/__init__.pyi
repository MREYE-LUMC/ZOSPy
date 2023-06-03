"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("HuygensMtfTypes", "MtfDataTypes", "MtfTypes", "ShowAsTypes", "SurfaceMtfTypes")

class HuygensMtfTypes(Enum):
    Modulation = 0

class MtfDataTypes(Enum):
    Average = 0
    Tangential = 1
    Sagittal = 2

class MtfTypes(Enum):
    Modulation = 0
    Real = 1
    Imaginary = 2
    Phase = 3
    SquareWave = 4

class ShowAsTypes(Enum):
    GreyScale = 0
    GreyScaleInverted = 1
    FalseColor = 2
    FalseColorInverted = 3

class SurfaceMtfTypes(Enum):
    MTF_Incoherent = 0
    Real_Incoherent = 1
    Imaginary_Incoherent = 2
    MTF_Coherent = 3
    Real_Coherent = 4
    Imaginary_Coherent = 5
