"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from typing import overload

from zospy.api.stubs._ZOSAPI.Tools.RayTrace import (
    BatchRayTraceDataEntry,
    IRayTraceDirectPolData,
    IRayTraceDirectUnpolData,
    IRayTraceNormPolData,
    IRayTraceNormUnpolData,
    IRayTraceNSCData,
    IRayTraceNSCSourceData,
    IZRDReaderResults,
    LTEdgeSasmpling,
    LTRaySampling,
    NSCTraceOptions,
    OPDMode,
    RayPathDataEntry,
    RayPathDataHolder,
    RayStatus,
    RaysType,
    ZRDFormatType,
)
from zospy.api.stubs._ZOSAPI.Tools import HPCRunState, ISystemTool
from zospy.api.stubs._ZOSAPI.Analysis import ErrorType

from zospy.api.stubs._ZOSAPI_constants.Tools.RayTrace import (
    LTEdgeSasmpling,
    LTRaySampling,
    NSCTraceOptions,
    OPDMode,
    RayStatus,
    RaysType,
    ZRDFormatType,
)

__all__ = (
    "BatchRayTraceDataEntry",
    "BatchRayTraceDataHolder",
    "IBatchRayTrace",
    "ILightningTrace",
    "INSCRayTrace",
    "IRayTraceDirectPolData",
    "IRayTraceDirectUnpolData",
    "IRayTraceNormPolData",
    "IRayTraceNormUnpolData",
    "IRayTraceNSCData",
    "IRayTraceNSCSourceData",
    "IZRDReader",
    "IZRDReaderResults",
    "LTEdgeSasmpling",
    "LTRaySampling",
    "NSCTraceOptions",
    "OPDMode",
    "RayPathDataEntry",
    "RayPathDataHolder",
    "RayStatus",
    "RaysType",
    "ZRDFormatType",
)

class BatchRayTraceDataEntry: ...

class BatchRayTraceDataHolder:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, data: list[BatchRayTraceDataEntry]): ...
    @overload
    def __init__(self, info: object, context: object): ...
    def GetObjectData(self, info: object, context: object) -> None: ...

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
        self,
        MaxRays: int,
        rayType: RaysType,
        Ex: float,
        Ey: float,
        phaX: float,
        phaY: float,
        toSurface: int,
    ) -> IRayTraceNormPolData: ...
    def CreateNormUnpol(
        self, MaxRays: int, rayType: RaysType, toSurface: int
    ) -> IRayTraceNormUnpolData: ...
    def CreateNSC(
        self, MaxRays: int, maxSegments: int, coherenceLength: float
    ) -> IRayTraceNSCData: ...
    def CreateNSCSourceData(
        self, maxSegments: int, coherenceLength: float
    ) -> IRayTraceNSCSourceData: ...
    def GetDirectFieldCoordinates(
        self,
        waveNumber: int,
        rayType: RaysType,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
    ) -> tuple[bool, float, float, float, float, float, float]: ...
    def GetPhase(
        self,
        L: float,
        M: float,
        N: float,
        jx: float,
        jy: float,
        xPhaseDeg: float,
        yPhaseDeg: float,
        intensity: float,
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
        bool,
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
    ) -> tuple[
        bool,
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
    ]: ...
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
        bool,
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
    ]: ...
    def SingleRayNormUnpol(
        self,
        rayType: RaysType,
        toSurf: int,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        calcOPD: bool,
    ) -> tuple[
        bool,
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
    ]: ...

class ILightningTrace(ISystemTool):
    @property
    def RaySampling(self) -> LTRaySampling: ...
    @RaySampling.setter
    def RaySampling(self, value: LTRaySampling) -> None: ...
    @property
    def EdgeSampling(self) -> LTEdgeSasmpling: ...
    @EdgeSampling.setter
    def EdgeSampling(self, value: LTEdgeSasmpling) -> None: ...

class INSCRayTrace(ISystemTool):
    @property
    def AutoUpdate(self) -> bool: ...
    @AutoUpdate.setter
    def AutoUpdate(self, value: bool) -> None: ...
    @property
    def NumberOfCores(self) -> int: ...
    @NumberOfCores.setter
    def NumberOfCores(self, value: int) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def IgnoreErrors(self) -> bool: ...
    @IgnoreErrors.setter
    def IgnoreErrors(self, value: bool) -> None: ...
    @property
    def SplitNSCRays(self) -> bool: ...
    @SplitNSCRays.setter
    def SplitNSCRays(self, value: bool) -> None: ...
    @property
    def ScatterNSCRays(self) -> bool: ...
    @ScatterNSCRays.setter
    def ScatterNSCRays(self, value: bool) -> None: ...
    @property
    def SaveRays(self) -> bool: ...
    @SaveRays.setter
    def SaveRays(self, value: bool) -> None: ...
    @property
    def SaveRaysFile(self) -> str: ...
    @SaveRaysFile.setter
    def SaveRaysFile(self, value: str) -> None: ...
    @property
    def SavePaths(self) -> bool: ...
    @SavePaths.setter
    def SavePaths(self, value: bool) -> None: ...
    @property
    def SavePathsFile(self) -> str: ...
    @SavePathsFile.setter
    def SavePathsFile(self, value: str) -> None: ...
    @property
    def ZRDFormat(self) -> ZRDFormatType: ...
    @ZRDFormat.setter
    def ZRDFormat(self, value: ZRDFormatType) -> None: ...
    @property
    def Filter(self) -> str: ...
    @Filter.setter
    def Filter(self, value: str) -> None: ...
    @property
    def DeadRayErrors(self) -> float: ...
    @property
    def DeadRayThreshold(self) -> float: ...
    @property
    def IsHPCEnabled(self) -> bool: ...
    @property
    def HPCEstimatedTimeS(self) -> float: ...
    @property
    def HPCRemainingTimeS(self) -> float: ...
    @property
    def HPCTimeToStartS(self) -> float: ...
    @property
    def HPCQueuePosition(self) -> int: ...
    @property
    def HPCState(self) -> HPCRunState: ...
    @property
    def HPCHasTimeEstimate(self) -> bool: ...
    @property
    def RayMultiplier(self) -> float: ...
    @RayMultiplier.setter
    def RayMultiplier(self, value: float) -> None: ...
    @property
    def HasHPCUnsupportedDetectors(self) -> bool: ...
    def ClearDetectorObject(self, ObjectNumber: int) -> ErrorType: ...
    def ClearDetectors(self, DetectorNumber: int) -> ErrorType: ...
    def EstimateHPCTime(self) -> bool: ...
    def GetTotalRayEnergy(self) -> float: ...
    def ResetRandomSeed(self) -> None: ...
    def SetPartialRTMode(self, seed: int, group: int) -> None: ...
    def SetRandomSeed(self, seed: int) -> None: ...

class IRayTraceDirectPolData:
    @property
    def NumberOfRays(self) -> int: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def HasResultData(self) -> bool: ...
    def AddRay(
        self,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> bool: ...
    def ClearData(self) -> None: ...
    def ReadNextResult(
        self,
    ) -> tuple[
        bool, int, int, int, float, float, float, float, float, float, float
    ]: ...
    def ReadNextResultFull(
        self,
    ) -> tuple[
        bool,
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
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceDirectUnpolData:
    @property
    def NumberOfRays(self) -> int: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def HasResultData(self) -> bool: ...
    def AddRay(
        self,
        waveNumber: int,
        X: float,
        Y: float,
        Z: float,
        L: float,
        M: float,
        N: float,
    ) -> bool: ...
    def ClearData(self) -> None: ...
    def ReadNextResult(
        self,
    ) -> tuple[
        bool,
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
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNormPolData:
    @property
    def NumberOfRays(self) -> int: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def HasResultData(self) -> bool: ...
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
    def ReadNextResult(
        self,
    ) -> tuple[bool, int, int, float, float, float, float, float, float, float]: ...
    def ReadNextResultFull(
        self,
    ) -> tuple[
        bool,
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
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNormUnpolData:
    @property
    def NumberOfRays(self) -> int: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def HasResultData(self) -> bool: ...
    def AddRay(
        self,
        waveNumber: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        calcOPD: OPDMode,
    ) -> bool: ...
    def ClearData(self) -> None: ...
    def ReadNextResult(
        self,
    ) -> tuple[
        bool,
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
    ]: ...
    def StartReadingResults(self) -> bool: ...

class IRayTraceNSCData:
    @property
    def NumberOfRays(self) -> int: ...
    @property
    def MaxRays(self) -> int: ...
    @property
    def HasResultData(self) -> bool: ...
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
    def UseSingleSource(self) -> bool: ...
    @UseSingleSource.setter
    def UseSingleSource(self, value: bool) -> None: ...
    @property
    def SurfaceNumber(self) -> int: ...
    @SurfaceNumber.setter
    def SurfaceNumber(self, value: int) -> None: ...
    @property
    def ObjectNumber(self) -> int: ...
    @ObjectNumber.setter
    def ObjectNumber(self, value: int) -> None: ...
    @property
    def MaxRays(self) -> int: ...
    @MaxRays.setter
    def MaxRays(self, value: int) -> None: ...
    @property
    def TraceOptions(self) -> NSCTraceOptions: ...
    @TraceOptions.setter
    def TraceOptions(self, value: NSCTraceOptions) -> None: ...
    @property
    def Wavelength(self) -> int: ...
    @Wavelength.setter
    def Wavelength(self, value: int) -> None: ...
    @property
    def HasResultData(self) -> bool: ...
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
    def UseAnyWavelength(self) -> None: ...
    def UsePrimaryWavelength(self) -> None: ...

class IZRDReader(ISystemTool):
    @property
    def ZRDFile(self) -> None: ...
    @ZRDFile.setter
    def ZRDFile(self, value: str) -> None: ...
    @property
    def Filter(self) -> str: ...
    @Filter.setter
    def Filter(self, value: str) -> None: ...
    def GetResults(self) -> IZRDReaderResults: ...

class IZRDReaderResults:
    @property
    def IsValid(self) -> bool: ...
    @property
    def RayNumber(self) -> int: ...
    @property
    def WaveIndex(self) -> int: ...
    @property
    def WlUM(self) -> float: ...
    @property
    def NumSegments(self) -> int: ...
    @property
    def SegTerminated(self) -> bool: ...
    @property
    def SegReflected(self) -> bool: ...
    @property
    def SegTransmitted(self) -> bool: ...
    @property
    def SegScattered(self) -> bool: ...
    @property
    def SegDiffracted(self) -> bool: ...
    @property
    def SegBulkScattered(self) -> bool: ...
    @property
    def SegmentTIR(self) -> bool: ...
    @property
    def ParentGhost(self) -> bool: ...
    @property
    def ParentDiffracted(self) -> bool: ...
    @property
    def ParentScattered(self) -> bool: ...
    @property
    def RayError(self) -> bool: ...
    @property
    def SegmentLevel(self) -> int: ...
    @property
    def SegmentParent(self) -> int: ...
    @property
    def HitObject(self) -> int: ...
    @property
    def HitFace(self) -> int: ...
    @property
    def InsideOf(self) -> int: ...
    @property
    def X(self) -> float: ...
    @property
    def Y(self) -> float: ...
    @property
    def Z(self) -> float: ...
    @property
    def L(self) -> float: ...
    @property
    def M(self) -> float: ...
    @property
    def N(self) -> float: ...
    @property
    def EXR(self) -> float: ...
    @property
    def EXI(self) -> float: ...
    @property
    def EYR(self) -> float: ...
    @property
    def EYI(self) -> float: ...
    @property
    def EZR(self) -> float: ...
    @property
    def EZI(self) -> float: ...
    @property
    def Intensity(self) -> float: ...
    @property
    def PathLength(self) -> float: ...
    @property
    def OpticalPathW(self) -> float: ...
    @property
    def OpticalPathLU(self) -> float: ...
    @property
    def XYBin(self) -> float: ...
    @property
    def LMBin(self) -> float: ...
    @property
    def XNorm(self) -> float: ...
    @property
    def YNorm(self) -> float: ...
    @property
    def ZNorm(self) -> float: ...
    @property
    def Index(self) -> float: ...
    @property
    def StartingPhase(self) -> float: ...
    @property
    def PhaseOf(self) -> float: ...
    @property
    def PhaseAt(self) -> float: ...
    @property
    def HasOrderX(self) -> bool: ...
    @property
    def HasOrderY(self) -> bool: ...
    @property
    def OrderX(self) -> int: ...
    @property
    def OrderY(self) -> int: ...
    def ReadNextRay(self) -> bool: ...
    def ReadNextRaySegment(self) -> bool: ...
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

# LTEdgeSasmpling is imported as constant

# LTRaySampling is imported as constant

# NSCTraceOptions is imported as constant

# OPDMode is imported as constant

class RayPathDataEntry: ...

class RayPathDataHolder:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, offset: int, size: int): ...
    @overload
    def __init__(self, info: object, context: object): ...
    def GetData(
        self, mmf: object, data: list[RayPathDataEntry]
    ) -> tuple[bool, list[RayPathDataEntry]]: ...
    def GetObjectData(self, info: object, context: object) -> None: ...
    def SetData(
        mmf: object, data: list[RayPathDataEntry], index: int
    ) -> RayPathDataHolder: ...

# RayStatus is imported as constant

# RaysType is imported as constant

# ZRDFormatType is imported as constant
