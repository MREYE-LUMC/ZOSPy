"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = ("LTEdgeSasmpling", "LTRaySampling", "NSCTraceOptions", "OPDMode", "RayStatus", "RaysType", "ZRDFormatType")

class LTEdgeSasmpling:
    S_1X_Low: LTEdgeSasmpling = None
    S_4X: LTEdgeSasmpling = None
    S_16X: LTEdgeSasmpling = None
    S_64X: LTEdgeSasmpling = None
    S_256X: LTEdgeSasmpling = None

class LTRaySampling:
    S_1X_Low: LTRaySampling = None
    S_4X: LTRaySampling = None
    S_16X: LTRaySampling = None
    S_64X: LTRaySampling = None
    S_256X: LTRaySampling = None
    S_1024X: LTRaySampling = None

class NSCTraceOptions:
    None_: NSCTraceOptions = None
    UsePolarization: NSCTraceOptions = None
    UseSplitting: NSCTraceOptions = None
    UsePolarizationSplitting: NSCTraceOptions = None
    UseScattering: NSCTraceOptions = None
    UsePolarizationScattering: NSCTraceOptions = None
    UseSplittingScattering: NSCTraceOptions = None
    UsePolarizationSplittingScattering: NSCTraceOptions = None

class OPDMode:
    None_: OPDMode = None
    Current: OPDMode = None
    CurrentAndChief: OPDMode = None

class RayStatus:
    Parent: RayStatus = None
    Terminated: RayStatus = None
    Reflected: RayStatus = None
    Transmitted: RayStatus = None
    Scattered: RayStatus = None
    Diffracted: RayStatus = None
    GhostedFrom: RayStatus = None
    DiffractedFrom: RayStatus = None
    ScatteredFrom: RayStatus = None
    RayError: RayStatus = None
    BulkScattered: RayStatus = None
    WaveShifted: RayStatus = None
    TIR: RayStatus = None
    OrdinaryRay: RayStatus = None
    ExtraordinaryRay: RayStatus = None
    WaveShiftPL: RayStatus = None

class RaysType:
    Real: RaysType = None
    Paraxial: RaysType = None

class ZRDFormatType:
    UncompressedFullData: ZRDFormatType = None
    CompressedBasicData: ZRDFormatType = None
    CompressedFullData: ZRDFormatType = None
