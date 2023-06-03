"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from typing import overload

from zospy.api._ZOSAPI.Analysis import ErrorType
from zospy.api._ZOSAPI.Tools import HPCRunState, ISystemTool

__all__ = (
    "BatchRayTraceDataEntry",
    "BatchRayTraceDataEntry",
    "BatchRayTraceDataHolder",
    "BatchRayTraceDataHolder",
    "IBatchRayTrace",
    "ILightningTrace",
    "INSCRayTrace",
    "IRayTraceDirectPolData",
    "IRayTraceDirectPolData",
    "IRayTraceDirectUnpolData",
    "IRayTraceDirectUnpolData",
    "IRayTraceNormPolData",
    "IRayTraceNormPolData",
    "IRayTraceNormUnpolData",
    "IRayTraceNormUnpolData",
    "IRayTraceNSCData",
    "IRayTraceNSCData",
    "IRayTraceNSCSourceData",
    "IRayTraceNSCSourceData",
    "IZRDReader",
    "IZRDReaderResults",
    "IZRDReaderResults",
    "LTEdgeSasmpling",
    "LTRaySampling",
    "NSCTraceOptions",
    "OPDMode",
    "RayPathDataEntry",
    "RayPathDataEntry",
    "RayPathDataHolder",
    "RayPathDataHolder",
    "RayStatus",
    "RaysType",
    "ZRDFormatType",
)

class BatchRayTraceDataEntry:
    pass

class BatchRayTraceDataHolder:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, data: list[BatchRayTraceDataEntry]): ...
    @overload
    def __init__(self, info: SerializationInfo, context: StreamingContext): ...
    def GetObjectData(self, info: SerializationInfo, context: StreamingContext) -> None: ...

class IBatchRayTrace(ISystemTool):
    def CreateDirectPol(
        self,
        MaxRays: int,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phax: float,
        phay: float,
        startSurface: int,
        toSurface: int,
    ) -> IRayTraceDirectPolData: ...
    def CreateDirectUnpol(
        self, MaxRays: int, rayType: RaysType, startSurface: int, toSurface: int
    ) -> IRayTraceDirectUnpolData: ...
    def CreateNormPol(
        self, MaxRays: int, rayType: RaysType, Ex: float, Ey: float, phaX: float, phaY: float, toSurface: int
    ) -> IRayTraceNormPolData: ...
    def CreateNormUnpol(self, MaxRays: int, rayType: RaysType, toSurface: int) -> IRayTraceNormUnpolData: ...
    def CreateNSC(self, MaxRays: int, maxSegments: int, coherenceLength: float) -> IRayTraceNSCData: ...
    def CreateNSCSourceData(self, maxSegments: int, coherenceLength: float) -> IRayTraceNSCSourceData: ...
    def GetDirectFieldCoordinates(
        self, waveNumber: int, rayType: RaysType, Hx: float, Hy: float, Px: float, Py: float
    ) -> tuple[bool, float, float, float, float, float, float]: ...
    def GetPhase(
        self, L: float, M: float, N: float, jx: float, jy: float, xPhaseDeg: float, yPhaseDeg: float, intensity: float
    ) -> tuple[float, float, float, float, float, float]: ...
    def SingleRayDirectPol(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        startSurface: int,
        toSurface: int,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> tuple[bool, int, int, float, float, float, float, float, float, float]: ...
    def SingleRayDirectPolFull(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        startSurface: int,
        toSurface: int,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> tuple[
        bool, int, int, float, float, float, float, float, float, float, float, float, float, float, float, float
    ]: ...
    def SingleRayDirectUnpol(
        self,
        rayType: RaysType,
        startSurface: int,
        toSurface: int,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> tuple[bool, int, int, float, float, float, float, float, float, float, float, float, float]: ...
    def SingleRayNormPol(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        toSurf: int,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> tuple[bool, int, float, float, float, float, float, float, float]: ...
    def SingleRayNormPolFull(
        self,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        toSurf: int,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> tuple[
        bool, int, float, float, float, float, float, float, float, float, float, float, float, float, float
    ]: ...
    def SingleRayNormUnpol(
        self, rayType: RaysType, toSurf: int, waveNumber: int, Hx: float, Hy: float, Px: float, Py: float, calcOPD: bool
    ) -> tuple[bool, int, int, float, float, float, float, float, float, float, float, float, float, float]: ...

class ILightningTrace(ISystemTool):
    @property
    def EdgeSampling(self) -> LTEdgeSasmpling: ...
    @property
    def RaySampling(self) -> LTRaySampling: ...
    @EdgeSampling.setter
    def EdgeSampling(self, value: LTEdgeSasmpling) -> None: ...
    @RaySampling.setter
    def RaySampling(self, value: LTRaySampling) -> None: ...

class INSCRayTrace(ISystemTool):
    def ClearDetectorObject(self, ObjectNumber: int) -> ErrorType: ...
    def ClearDetectors(self, DetectorNumber: int) -> ErrorType: ...
    def EstimateHPCTime(self) -> bool: ...
    @property
    def AutoUpdate(self) -> bool: ...
    @property
    def DeadRayErrors(self) -> float: ...
    @property
    def DeadRayThreshold(self) -> float: ...
    @property
    def Filter(self) -> str: ...
    @property
    def HasHPCUnsupportedDetectors(self) -> bool: ...
    @property
    def HPCEstimatedTimeS(self) -> float: ...
    @property
    def HPCHasTimeEstimate(self) -> bool: ...
    @property
    def HPCQueuePosition(self) -> int: ...
    @property
    def HPCRemainingTimeS(self) -> float: ...
    @property
    def HPCState(self) -> HPCRunState: ...
    @property
    def HPCTimeToStartS(self) -> float: ...
    @property
    def IgnoreErrors(self) -> bool: ...
    @property
    def IsHPCEnabled(self) -> bool: ...
    @property
    def NumberOfCores(self) -> int: ...
    @property
    def RayMultiplier(self) -> float: ...
    @property
    def SavePaths(self) -> bool: ...
    @property
    def SavePathsFile(self) -> str: ...
    @property
    def SaveRays(self) -> bool: ...
    @property
    def SaveRaysFile(self) -> str: ...
    @property
    def ScatterNSCRays(self) -> bool: ...
    @property
    def SplitNSCRays(self) -> bool: ...
    @property
    def UsePolarization(self) -> bool: ...
    @property
    def ZRDFormat(self) -> ZRDFormatType: ...
    def GetTotalRayEnergy(self) -> float: ...
    def ResetRandomSeed(self) -> None: ...
    @AutoUpdate.setter
    def AutoUpdate(self, value: bool) -> None: ...
    @Filter.setter
    def Filter(self, value: str) -> None: ...
    @IgnoreErrors.setter
    def IgnoreErrors(self, value: bool) -> None: ...
    @NumberOfCores.setter
    def NumberOfCores(self, value: int) -> None: ...
    @RayMultiplier.setter
    def RayMultiplier(self, value: float) -> None: ...
    @SavePaths.setter
    def SavePaths(self, value: bool) -> None: ...
    @SavePathsFile.setter
    def SavePathsFile(self, value: str) -> None: ...
    @SaveRays.setter
    def SaveRays(self, value: bool) -> None: ...
    @SaveRaysFile.setter
    def SaveRaysFile(self, value: str) -> None: ...
    @ScatterNSCRays.setter
    def ScatterNSCRays(self, value: bool) -> None: ...
    @SplitNSCRays.setter
    def SplitNSCRays(self, value: bool) -> None: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @ZRDFormat.setter
    def ZRDFormat(self, value: ZRDFormatType) -> None: ...
    def SetPartialRTMode(self, seed: int, group: int) -> None: ...
    def SetRandomSeed(self, seed: int) -> None: ...

class IRayTraceDirectPolData:
    def AddRay(self, waveNumber: int, X: float, Y: float, Z: float, L: float, M: float, N: float) -> bool: ...
    def ClearData(self) -> None: ...
    @property
    def HasResultData(self) -> bool: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def NumberOfRays(self) -> int: ...
    def ReadNextResult(self) -> tuple[bool, int, int, int, float, float, float, float, float, float, float]: ...
    def ReadNextResultFull(
        self,
    ) -> tuple[
        bool, int, int, int, float, float, float, float, float, float, float, float, float, float, float, float, float
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceDirectUnpolData:
    def AddRay(self, waveNumber: int, X: float, Y: float, Z: float, L: float, M: float, N: float) -> bool: ...
    def ClearData(self) -> None: ...
    @property
    def HasResultData(self) -> bool: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def NumberOfRays(self) -> int: ...
    def ReadNextResult(
        self,
    ) -> tuple[bool, int, int, int, float, float, float, float, float, float, float, float, float, float]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNormPolData:
    def AddRay(
        self,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> bool: ...
    def ClearData(self) -> None: ...
    @property
    def HasResultData(self) -> bool: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def NumberOfRays(self) -> int: ...
    def ReadNextResult(self) -> tuple[bool, int, int, float, float, float, float, float, float, float]: ...
    def ReadNextResultFull(
        self,
    ) -> tuple[
        bool, int, int, float, float, float, float, float, float, float, float, float, float, float, float, float
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNormUnpolData:
    def AddRay(self, waveNumber: int, Hx: float, Hy: float, Px: float, Py: float, calcOPD: OPDMode) -> bool: ...
    def ClearData(self) -> None: ...
    @property
    def HasResultData(self) -> bool: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def NumberOfRays(self) -> int: ...
    def ReadNextResult(
        self,
    ) -> tuple[bool, int, int, int, float, float, float, float, float, float, float, float, float, float, float]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNSCData:
    def AddRay(
        self,
        waveNumber: int,
        surf: int,
        mode: NSCTraceOptions,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
        InsideOf: int,
        exr: float,
        exi: float,
        eyr: float,
        eyi: float,
        ezr: float,
        ezi: float,
    ) -> bool: ...
    def ClearData(self) -> None: ...
    @property
    def HasResultData(self) -> bool: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def NumberOfRays(self) -> int: ...
    def ReadNextResult(self) -> tuple[bool, int, int, int, int]: ...
    def ReadNextSegment(
        self,
    ) -> tuple[
        bool,
        int,
        int,
        int,
        int,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNSCSourceData:
    @property
    def HasResultData(self) -> bool: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def ObjectNumber(self) -> int: ...
    @property
    def SurfaceNumber(self) -> int: ...
    @property
    def TraceOptions(self) -> NSCTraceOptions: ...
    @property
    def UseSingleSource(self) -> bool: ...
    @property
    def Wavelength(self) -> int: ...
    def ReadNextResult(self) -> tuple[bool, int, int, int, int]: ...
    def ReadNextSegment(
        self,
    ) -> tuple[
        bool,
        int,
        int,
        int,
        int,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ]: ...
    @MaxRays.setter
    def MaxRays(self, value: int) -> None: ...
    @ObjectNumber.setter
    def ObjectNumber(self, value: int) -> None: ...
    @SurfaceNumber.setter
    def SurfaceNumber(self, value: int) -> None: ...
    @TraceOptions.setter
    def TraceOptions(self, value: NSCTraceOptions) -> None: ...
    @UseSingleSource.setter
    def UseSingleSource(self, value: bool) -> None: ...
    @Wavelength.setter
    def Wavelength(self, value: int) -> None: ...
    def StartReadingResults(self) -> bool: ...
    def UseAnyWavelength(self) -> None: ...
    def UsePrimaryWavelength(self) -> None: ...

class IZRDReader(ISystemTool):
    @property
    def Filter(self) -> str: ...
    def GetResults(self) -> IZRDReaderResults: ...
    @Filter.setter
    def Filter(self, value: str) -> None: ...
    @ZRDFile.setter
    def ZRDFile(self, value: str) -> None: ...

class IZRDReaderResults:
    @property
    def IsValid(self) -> bool: ...
    def ReadNextResult(self) -> tuple[bool, int, int, float, int]: ...
    def ReadNextSegment(
        self,
    ) -> tuple[
        bool,
        int,
        int,
        int,
        int,
        int,
        RayStatus,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ]: ...
    def ReadNextSegmentFull(
        self,
    ) -> tuple[
        bool,
        int,
        int,
        int,
        int,
        int,
        RayStatus,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        int,
        int,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ]: ...

class LTEdgeSasmpling:
    S_1X_Low = 0
    S_4X = 1
    S_16X = 2
    S_64X = 3
    S_256X = 4

class LTRaySampling:
    S_1X_Low = 0
    S_4X = 1
    S_16X = 2
    S_64X = 3
    S_256X = 4
    S_1024X = 5

class NSCTraceOptions:
    # None = 0
    UsePolarization = 1
    UseSplitting = 2
    UsePolarizationSplitting = 3
    UseScattering = 4
    UsePolarizationScattering = 5
    UseSplittingScattering = 6
    UsePolarizationSplittingScattering = 7

class OPDMode:
    # None = 0
    Current = 1
    CurrentAndChief = 2

class RayPathDataEntry:
    pass

class RayPathDataHolder:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, offset: int, size: int): ...
    @overload
    def __init__(self, info: SerializationInfo, context: StreamingContext): ...
    def GetData(self, mmf: MemoryMappedFile, data: list[RayPathDataEntry]) -> tuple[bool, list[RayPathDataEntry]]: ...
    def GetObjectData(self, info: SerializationInfo, context: StreamingContext) -> None: ...
    def SetData(mmf: MemoryMappedFile, data: list[RayPathDataEntry], index: int) -> RayPathDataHolder: ...

class RayStatus:
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

class RaysType:
    Real = 0
    Paraxial = 1

class ZRDFormatType:
    UncompressedFullData = 0
    CompressedBasicData = 1
    CompressedFullData = 2
