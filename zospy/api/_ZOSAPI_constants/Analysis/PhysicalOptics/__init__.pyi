"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

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

class POPBeamTypes:
    GaussianWaist: POPBeamTypes = None
    GaussianAngle: POPBeamTypes = None
    GaussianSizeAngle: POPBeamTypes = None
    TopHat: POPBeamTypes = None
    File: POPBeamTypes = None
    DLL: POPBeamTypes = None
    Multimode: POPBeamTypes = None
    AstigmaticGaussian: POPBeamTypes = None

class POPDataTypes:
    Irradiance: POPDataTypes = None
    EXIrradiance: POPDataTypes = None
    EYIrradiance: POPDataTypes = None
    Phase: POPDataTypes = None
    EXPhase: POPDataTypes = None
    EYPhase: POPDataTypes = None
    TransferMagnitude: POPDataTypes = None
    TransferPhase: POPDataTypes = None

class POPFiberPositions:
    ChiefRay: POPFiberPositions = None
    SurfaceVertex: POPFiberPositions = None

class POPFiberTypes:
    GaussianWaist: POPFiberTypes = None
    GaussianAngle: POPFiberTypes = None
    GaussianSizeAngle: POPFiberTypes = None
    TopHat: POPFiberTypes = None
    File: POPFiberTypes = None
    DLL: POPFiberTypes = None
    AstigmaticGaussian: POPFiberTypes = None

class POPProjectionTypes:
    AlongBeam: POPProjectionTypes = None
    AlongNormal: POPProjectionTypes = None
    AlongLocalZ: POPProjectionTypes = None

class POPScaleTypes:
    Linear: POPScaleTypes = None
    Log_Minus_5: POPScaleTypes = None
    Log_Minus_10: POPScaleTypes = None
    Log_Minus_15: POPScaleTypes = None

class POPShowAsTypes:
    Surface: POPShowAsTypes = None
    Contour: POPShowAsTypes = None
    GrayScale: POPShowAsTypes = None
    InverseGrayScale: POPShowAsTypes = None
    FalseColor: POPShowAsTypes = None
    InverseFalseColor: POPShowAsTypes = None
    CrossX: POPShowAsTypes = None
    CrossY: POPShowAsTypes = None
    Encircled: POPShowAsTypes = None
    Ensquared: POPShowAsTypes = None
    EnslittedX: POPShowAsTypes = None
    EnslittedY: POPShowAsTypes = None

class POPZoomTypes:
    NoZoom: POPZoomTypes = None
    X2: POPZoomTypes = None
    X4: POPZoomTypes = None
    X8: POPZoomTypes = None
    X16: POPZoomTypes = None
