"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

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

class DisplayAsTypes:
    Percent: DisplayAsTypes = None
    Absolute: DisplayAsTypes = None

class Distortions:
    F_TanTheta: Distortions = None
    F_Theta: Distortions = None
    Cal_F_Theta: Distortions = None
    Cal_F_TanTheta: Distortions = None
    SMIA_TV: Distortions = None

class FFA_AberrationTypes:
    Defocus: FFA_AberrationTypes = None
    PrimaryAstigmatism: FFA_AberrationTypes = None
    PrimaryComa: FFA_AberrationTypes = None
    SpecifiedTerm: FFA_AberrationTypes = None

class FFA_DecompositionTypes:
    ZernikeTerms: FFA_DecompositionTypes = None

class FFA_DisplayTypes:
    Absolute: FFA_DisplayTypes = None
    Relative: FFA_DisplayTypes = None
    Average: FFA_DisplayTypes = None

class FFA_FieldShapes:
    Rectangular: FFA_FieldShapes = None
    Elliptical: FFA_FieldShapes = None

class FFA_ShowAsTypes:
    GreyScale: FFA_ShowAsTypes = None
    GreyScaleInverted: FFA_ShowAsTypes = None
    FalseColor: FFA_ShowAsTypes = None
    FalseColorInverted: FFA_ShowAsTypes = None
    Icons: FFA_ShowAsTypes = None

class FieldScanDirections:
    Plus_Y: FieldScanDirections = None
    Plus_X: FieldScanDirections = None
    Minus_Y: FieldScanDirections = None
    Minus_X: FieldScanDirections = None

class RayTraceType:
    DirectionCosines: RayTraceType = None
    TangentAngle: RayTraceType = None
    YmUmYcUc: RayTraceType = None

class ZernikeCoefficientTypes:
    Fringe: ZernikeCoefficientTypes = None
    Standard: ZernikeCoefficientTypes = None
    Annular: ZernikeCoefficientTypes = None
