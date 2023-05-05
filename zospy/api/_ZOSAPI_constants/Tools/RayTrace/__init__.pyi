"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("LTEdgeSasmpling", "LTRaySampling", "NSCTraceOptions", "OPDMode", "RayStatus", "RaysType", "ZRDFormatType")

class LTEdgeSasmpling(Enum):
    S_1X_Low = 0
    S_4X = 1
    S_16X = 2
    S_64X = 3
    S_256X = 4

class LTRaySampling(Enum):
    S_1X_Low = 0
    S_4X = 1
    S_16X = 2
    S_64X = 3
    S_256X = 4
    S_1024X = 5

class NSCTraceOptions(Enum):
    None_ = 0
    UsePolarization = 1
    UseSplitting = 2
    UsePolarizationSplitting = 3
    UseScattering = 4
    UsePolarizationScattering = 5
    UseSplittingScattering = 6
    UsePolarizationSplittingScattering = 7

class OPDMode(Enum):
    None_ = 0
    Current = 1
    CurrentAndChief = 2

class RayStatus(Enum):
    Parent = 0
    Terminated = 1
    Reflected = 2
    Transmitted = 4
    Scattered = 8
    Diffracted = 16
    GhostedFrom = 32
    DiffractedFrom = 64
    ScatteredFrom = 128
    RayError = 256
    BulkScattered = 512
    WaveShifted = 1024
    OrdinaryRay = 65536
    ExtraordinaryRay = 131072
    WaveShiftPL = 262144

class RaysType(Enum):
    Real = 0
    Paraxial = 1

class ZRDFormatType(Enum):
    UncompressedFullData = 0
    CompressedBasicData = 1
    CompressedFullData = 2
