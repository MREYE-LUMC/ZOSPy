"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = (
    "DisplayAsTypes",
    "Distortions",
    "FFA_AberrationTypes",
    "FFA_DecompositionTypes",
    "FFA_DisplayTypes",
    "FFA_FieldShapes",
    "FFA_ShowAsTypes",
    "FieldScanDirections",
    "RayTraceType",
    "ZernikeCoefficientTypes",
)

class DisplayAsTypes(Enum):
    Percent = 0
    Absolute = 1

class Distortions(Enum):
    F_TanTheta = 0
    F_Theta = 1
    Cal_F_Theta = 2
    Cal_F_TanTheta = 3
    SMIA_TV = 4

class FFA_AberrationTypes(Enum):
    Defocus = 0
    PrimaryAstigmatism = 1
    PrimaryComa = 2
    SpecifiedTerm = 3

class FFA_DecompositionTypes(Enum):
    ZernikeTerms = 0

class FFA_DisplayTypes(Enum):
    Absolute = 0
    Relative = 1
    Average = 2

class FFA_FieldShapes(Enum):
    Rectangular = 0
    Elliptical = 1

class FFA_ShowAsTypes(Enum):
    GreyScale = 0
    GreyScaleInverted = 1
    FalseColor = 2
    FalseColorInverted = 3
    Icons = 4

class FieldScanDirections(Enum):
    Plus_Y = 0
    Plus_X = 1
    Minus_Y = 2
    Minus_X = 3

class RayTraceType(Enum):
    DirectionCosines = 0
    TangentAngle = 1
    YmUmYcUc = 2

class ZernikeCoefficientTypes(Enum):
    Fringe = 0
    Standard = 1
    Annular = 2
