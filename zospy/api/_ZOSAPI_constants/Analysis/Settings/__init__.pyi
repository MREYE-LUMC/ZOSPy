"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

from . import (
    RMS,
    Aberrations,
    EncircledEnergy,
    ExtendedScene,
    Fans,
    Mtf,
    NSCSurface,
    Psf,
    Spot,
    Wavefront,
)

__all__ = (
    "Aberrations",
    "EncircledEnergy",
    "ExtendedScene",
    "Fans",
    "Mtf",
    "NSCSurface",
    "Psf",
    "RMS",
    "Spot",
    "Wavefront",
    "AxisType",
    "DetectorViewerScaleTypes",
    "DisplayOption",
    "HuygensPsfTypes",
    "Parity",
    "Polarizations",
    "PsfSpread",
    "PsfTypes",
    "ReferenceGia",
    "Rotations",
    "ScanTypes",
    "SourceGia",
    "STAREffectsOptions",
)

class AxisType(Enum):
    X = 0
    Y = 1
    Z = 2

class DetectorViewerScaleTypes(Enum):
    Linear = 0
    Log_Minus_5 = 1
    Normalized = 1
    Log_Minus_10 = 2
    Log_Minus_15 = 3

class DisplayOption(Enum):
    AllRays = 0
    FailedRays = 1
    PassedRays = 2

class HuygensPsfTypes(Enum):
    Linear = 0
    Log_Minus_1 = 1
    Log_Minus_2 = 2
    Log_Minus_3 = 3
    Log_Minus_4 = 4
    Log_Minus_5 = 5
    Real = 6
    Imaginary = 7
    Phase = 8

class Parity(Enum):
    Even = 0
    Odd = 1

class Polarizations(Enum):
    None_ = 0
    Ex = 1
    Ey = 2
    Ez = 3

class PsfSpread(Enum):
    Line = 0
    Edge = 1

class PsfTypes(Enum):
    X_Linear = 0
    Y_Linear = 1
    X_Logarithmic = 2
    Y_Logarithmic = 3
    X_Phase = 4
    Y_Phase = 5
    X_RealPart = 6
    Y_RealPart = 7
    X_ImaginaryPart = 8
    Y_ImaginaryPart = 9

class ReferenceGia(Enum):
    ChiefRay = 0
    Vertex = 1
    PrimaryChief = 2
    Centroid = 3

class Rotations(Enum):
    Rotate_0 = 0
    Rotate_90 = 1
    Rotate_180 = 2
    Rotate_270 = 3

class ScanTypes(Enum):
    Plus_Y = 0
    Plus_X = 1
    Minus_Y = 2
    Minus_X = 3

class SourceGia(Enum):
    Uniform = 0
    Lambertian = 1

class STAREffectsOptions(Enum):
    On = 0
    Difference = 1
