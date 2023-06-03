"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = (
    "POPBeamTypes",
    "POPDataTypes",
    "POPFiberPositions",
    "POPFiberTypes",
    "POPProjectionTypes",
    "POPScaleTypes",
    "POPShowAsTypes",
    "POPZoomTypes",
)

class POPBeamTypes(Enum):
    GaussianWaist = 0
    GaussianAngle = 1
    GaussianSizeAngle = 2
    TopHat = 3
    File = 4
    DLL = 5
    Multimode = 6
    AstigmaticGaussian = 7

class POPDataTypes(Enum):
    Irradiance = 0
    EXIrradiance = 1
    EYIrradiance = 2
    Phase = 3
    EXPhase = 4
    EYPhase = 5
    TransferMagnitude = 6
    TransferPhase = 7

class POPFiberPositions(Enum):
    ChiefRay = 0
    SurfaceVertex = 1

class POPFiberTypes(Enum):
    GaussianWaist = 0
    GaussianAngle = 1
    GaussianSizeAngle = 2
    TopHat = 3
    File = 4
    DLL = 5
    AstigmaticGaussian = 6

class POPProjectionTypes(Enum):
    AlongBeam = 0
    AlongNormal = 1
    AlongLocalZ = 2

class POPScaleTypes(Enum):
    Linear = 0
    Log_Minus_5 = 1
    Log_Minus_10 = 2
    Log_Minus_15 = 3

class POPShowAsTypes(Enum):
    Surface = 0
    Contour = 1
    GrayScale = 2
    InverseGrayScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    CrossX = 6
    CrossY = 7
    Encircled = 8
    Ensquared = 9
    EnslittedX = 10
    EnslittedY = 11

class POPZoomTypes(Enum):
    NoZoom = 0
    X2 = 1
    X4 = 2
    X8 = 3
    X16 = 4
