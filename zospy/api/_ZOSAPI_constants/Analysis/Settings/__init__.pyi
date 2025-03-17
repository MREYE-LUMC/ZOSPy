"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations
from . import Aberrations, EncircledEnergy, ExtendedScene, Fans, Mtf, NSCSurface, Psf, RMS, Spot, Wavefront

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

class AxisType:
    X: AxisType = None
    Y: AxisType = None
    Z: AxisType = None

class DetectorViewerScaleTypes:
    Linear: DetectorViewerScaleTypes = None
    Log_Minus_5: DetectorViewerScaleTypes = None
    Normalized: DetectorViewerScaleTypes = None
    Log_Minus_10: DetectorViewerScaleTypes = None
    Log_Minus_15: DetectorViewerScaleTypes = None

class DisplayOption:
    AllRays: DisplayOption = None
    FailedRays: DisplayOption = None
    PassedRays: DisplayOption = None

class HuygensPsfTypes:
    Linear: HuygensPsfTypes = None
    Log_Minus_1: HuygensPsfTypes = None
    Log_Minus_2: HuygensPsfTypes = None
    Log_Minus_3: HuygensPsfTypes = None
    Log_Minus_4: HuygensPsfTypes = None
    Log_Minus_5: HuygensPsfTypes = None
    Real: HuygensPsfTypes = None
    Imaginary: HuygensPsfTypes = None
    Phase: HuygensPsfTypes = None

class Parity:
    Even: Parity = None
    Odd: Parity = None

class Polarizations:
    None_: Polarizations = None
    Ex: Polarizations = None
    Ey: Polarizations = None
    Ez: Polarizations = None

class PsfSpread:
    Line: PsfSpread = None
    Edge: PsfSpread = None

class PsfTypes:
    X_Linear: PsfTypes = None
    Y_Linear: PsfTypes = None
    X_Logarithmic: PsfTypes = None
    Y_Logarithmic: PsfTypes = None
    X_Phase: PsfTypes = None
    Y_Phase: PsfTypes = None
    X_RealPart: PsfTypes = None
    Y_RealPart: PsfTypes = None
    X_ImaginaryPart: PsfTypes = None
    Y_ImaginaryPart: PsfTypes = None

class ReferenceGia:
    ChiefRay: ReferenceGia = None
    Vertex: ReferenceGia = None
    PrimaryChief: ReferenceGia = None
    Centroid: ReferenceGia = None

class Rotations:
    Rotate_0: Rotations = None
    Rotate_90: Rotations = None
    Rotate_180: Rotations = None
    Rotate_270: Rotations = None

class ScanTypes:
    Plus_Y: ScanTypes = None
    Plus_X: ScanTypes = None
    Minus_Y: ScanTypes = None
    Minus_X: ScanTypes = None

class SourceGia:
    Uniform: SourceGia = None
    Lambertian: SourceGia = None

class STAREffectsOptions:
    On: STAREffectsOptions = None
    Difference: STAREffectsOptions = None
