"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from typing import overload

from zospy.api._ZOSAPI.Tools import ISystemTool
from zospy.api._ZOSAPI.Tools.General import RayPatternType

__all__ = (
    "BackgroundOptions",
    "BrightnessOptions",
    "CameraViewpointOptions",
    "ColorRaysByCrossSectionOptions",
    "ColorRaysByNSCOptions",
    "ColorRaysByOptions",
    "DetectorDisplayModeOptions",
    "DetectorPixelColorOptions",
    "DrawSectionOptions",
    "I3DViewerExport",
    "ICrossSectionExport",
    "IImageExportData",
    "IImagePixel",
    "INSC3DLayoutExport",
    "INSCShadedModelExport",
    "IShadedModelExport",
    "LineThicknessOptions",
    "NumberSegmentsOptions",
    "OpacityOptions",
    "RayTraceOptions",
    "RealPupilOptions",
)

class BackgroundOptions:
    White = 0
    Black = 1
    Red = 2
    Green = 3
    Blue = 4
    DarkGreen = 5
    DarkBlue = 6
    Color01 = 7
    Color02 = 8
    Color03 = 9
    Color04 = 10
    Color05 = 11
    Color06 = 12
    Color07 = 13
    Color08 = 14
    Color09 = 15
    Color10 = 16
    Color11 = 17
    Color12 = 18
    Color13 = 19
    Color14 = 20
    Color15 = 21
    Color16 = 22
    Color17 = 23
    Color18 = 24
    Color19 = 25
    Color20 = 26
    Color21 = 27
    Color22 = 28
    Color23 = 29
    Color24 = 30
    Gradient01 = 31
    Gradient02 = 32
    Gradient03 = 33
    Gradient04 = 34
    Gradient05 = 35
    Gradient06 = 36
    Gradient07 = 37
    Gradient08 = 38
    Gradient09 = 39
    Gradient10 = 40
    GradientUser = 41

class BrightnessOptions:
    P100 = 0
    P90 = 1
    P80 = 2
    P70 = 3
    P60 = 4
    P50 = 5
    P40 = 6
    P30 = 7
    P20 = 8
    P10 = 9

class CameraViewpointOptions:
    Isometric = 0
    XY = 1
    YZ = 2
    XZ = 3

class ColorRaysByCrossSectionOptions:
    Fields = 0
    Waves = 1
    Wavelength = 2

class ColorRaysByNSCOptions:
    SourceNumber = 0
    WaveNumber = 1
    ConfigNumber = 2
    Wavelength = 3
    SegmentNumber = 4

class ColorRaysByOptions:
    Fields = 0
    Waves = 1
    Config = 2
    Wavelength = 3

class DetectorDisplayModeOptions:
    Consider = 0
    GreyScaleFlux = 1
    InverseGreyScaleFlux = 2
    FalseColorFlux = 3
    InverseFalseColorFlux = 4
    GreyScaleIrradiance = 5
    InverseGreyScaleIrradiance = 6
    FalseColorIrradiance = 7
    InverseFalseColorIrradiance = 8

class DetectorPixelColorOptions:
    DoNotColorIndividualPoints = 0
    ByRaysOnLayout = 1
    ByLastAnalysis = 2

class DrawSectionOptions:
    P100 = 0
    P75 = 1
    P50 = 2
    P25 = 3

class I3DViewerExport(ISystemTool):
    @property
    def SaveImageAsFile(self) -> bool: ...
    @SaveImageAsFile.setter
    def SaveImageAsFile(self, value: bool) -> None: ...
    @property
    def OutputFileName(self) -> str: ...
    @OutputFileName.setter
    def OutputFileName(self, value: str) -> None: ...
    @property
    def IsValidFileName(self) -> bool: ...
    @property
    def OutputPixelWidth(self) -> int: ...
    @OutputPixelWidth.setter
    def OutputPixelWidth(self, value: int) -> None: ...
    @property
    def OutputPixelHeight(self) -> int: ...
    @OutputPixelHeight.setter
    def OutputPixelHeight(self, value: int) -> None: ...
    @property
    def StartSurface(self) -> int: ...
    @StartSurface.setter
    def StartSurface(self, value: int) -> None: ...
    @property
    def EndSurface(self) -> int: ...
    @EndSurface.setter
    def EndSurface(self, value: int) -> None: ...
    @property
    def NumberOfRays(self) -> int: ...
    @NumberOfRays.setter
    def NumberOfRays(self, value: int) -> None: ...
    @property
    def Wavelength(self) -> int: ...
    @Wavelength.setter
    def Wavelength(self, value: int) -> None: ...
    @property
    def Field(self) -> int: ...
    @Field.setter
    def Field(self, value: int) -> None: ...
    @property
    def RayPattern(self) -> RayPatternType: ...
    @RayPattern.setter
    def RayPattern(self, value: RayPatternType) -> None: ...
    @property
    def ColorRaysBy(self) -> ColorRaysByOptions: ...
    @ColorRaysBy.setter
    def ColorRaysBy(self, value: ColorRaysByOptions) -> None: ...
    @property
    def DeleteVignetted(self) -> bool: ...
    @DeleteVignetted.setter
    def DeleteVignetted(self, value: bool) -> None: ...
    @property
    def HideLensFaces(self) -> bool: ...
    @HideLensFaces.setter
    def HideLensFaces(self, value: bool) -> None: ...
    @property
    def HideLensEdges(self) -> bool: ...
    @HideLensEdges.setter
    def HideLensEdges(self, value: bool) -> None: ...
    @property
    def HideXBars(self) -> bool: ...
    @HideXBars.setter
    def HideXBars(self, value: bool) -> None: ...
    @property
    def DrawParaxialPupils(self) -> bool: ...
    @DrawParaxialPupils.setter
    def DrawParaxialPupils(self, value: bool) -> None: ...
    @property
    def FletchRays(self) -> bool: ...
    @FletchRays.setter
    def FletchRays(self, value: bool) -> None: ...
    @property
    def SplitNSCRays(self) -> bool: ...
    @SplitNSCRays.setter
    def SplitNSCRays(self, value: bool) -> None: ...
    @property
    def ScatterNSCRays(self) -> bool: ...
    @ScatterNSCRays.setter
    def ScatterNSCRays(self, value: bool) -> None: ...
    @property
    def DrawRealEntrancePupils(self) -> RealPupilOptions: ...
    @DrawRealEntrancePupils.setter
    def DrawRealEntrancePupils(self, value: RealPupilOptions) -> None: ...
    @property
    def DrawRealExitPupils(self) -> RealPupilOptions: ...
    @DrawRealExitPupils.setter
    def DrawRealExitPupils(self, value: RealPupilOptions) -> None: ...
    @property
    def SurfaceLineThickness(self) -> LineThicknessOptions: ...
    @SurfaceLineThickness.setter
    def SurfaceLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def RaysLineThickness(self) -> LineThicknessOptions: ...
    @RaysLineThickness.setter
    def RaysLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def ConfigurationAll(self) -> bool: ...
    @ConfigurationAll.setter
    def ConfigurationAll(self, value: bool) -> None: ...
    @property
    def ConfigurationCurrent(self) -> bool: ...
    @ConfigurationCurrent.setter
    def ConfigurationCurrent(self, value: bool) -> None: ...
    @property
    def ConfigurationOffsetX(self) -> float: ...
    @ConfigurationOffsetX.setter
    def ConfigurationOffsetX(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetY(self) -> float: ...
    @ConfigurationOffsetY.setter
    def ConfigurationOffsetY(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetZ(self) -> float: ...
    @ConfigurationOffsetZ.setter
    def ConfigurationOffsetZ(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleX(self) -> float: ...
    @CameraViewpointAngleX.setter
    def CameraViewpointAngleX(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleY(self) -> float: ...
    @CameraViewpointAngleY.setter
    def CameraViewpointAngleY(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleZ(self) -> float: ...
    @CameraViewpointAngleZ.setter
    def CameraViewpointAngleZ(self, value: float) -> None: ...
    @property
    def ImageExportData(self) -> IImageExportData: ...
    def SetCameraViewpoint(self, cameraViewpoint: CameraViewpointOptions) -> None: ...
    def SetConfigurationEnabled(self, config: int, enabled: bool) -> None: ...

class ICrossSectionExport(ISystemTool):
    @property
    def SaveImageAsFile(self) -> bool: ...
    @SaveImageAsFile.setter
    def SaveImageAsFile(self, value: bool) -> None: ...
    @property
    def OutputFileName(self) -> str: ...
    @OutputFileName.setter
    def OutputFileName(self, value: str) -> None: ...
    @property
    def IsValidFileName(self) -> bool: ...
    @property
    def OutputPixelWidth(self) -> int: ...
    @OutputPixelWidth.setter
    def OutputPixelWidth(self, value: int) -> None: ...
    @property
    def OutputPixelHeight(self) -> int: ...
    @OutputPixelHeight.setter
    def OutputPixelHeight(self, value: int) -> None: ...
    @property
    def StartSurface(self) -> int: ...
    @StartSurface.setter
    def StartSurface(self, value: int) -> None: ...
    @property
    def EndSurface(self) -> int: ...
    @EndSurface.setter
    def EndSurface(self, value: int) -> None: ...
    @property
    def NumberOfRays(self) -> int: ...
    @NumberOfRays.setter
    def NumberOfRays(self, value: int) -> None: ...
    @property
    def YStretch(self) -> float: ...
    @YStretch.setter
    def YStretch(self, value: float) -> None: ...
    @property
    def Wavelength(self) -> int: ...
    @Wavelength.setter
    def Wavelength(self, value: int) -> None: ...
    @property
    def Field(self) -> int: ...
    @Field.setter
    def Field(self, value: int) -> None: ...
    @property
    def ColorRaysBy(self) -> ColorRaysByCrossSectionOptions: ...
    @ColorRaysBy.setter
    def ColorRaysBy(self, value: ColorRaysByCrossSectionOptions) -> None: ...
    @property
    def UpperPupil(self) -> float: ...
    @UpperPupil.setter
    def UpperPupil(self, value: float) -> None: ...
    @property
    def LowerPupil(self) -> float: ...
    @LowerPupil.setter
    def LowerPupil(self, value: float) -> None: ...
    @property
    def FletchRays(self) -> bool: ...
    @FletchRays.setter
    def FletchRays(self, value: bool) -> None: ...
    @property
    def DeleteVignetted(self) -> bool: ...
    @DeleteVignetted.setter
    def DeleteVignetted(self, value: bool) -> None: ...
    @property
    def MarginalAndChiefRayOnly(self) -> bool: ...
    @MarginalAndChiefRayOnly.setter
    def MarginalAndChiefRayOnly(self, value: bool) -> None: ...
    @property
    def SurfaceLineThickness(self) -> LineThicknessOptions: ...
    @SurfaceLineThickness.setter
    def SurfaceLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def RaysLineThickness(self) -> LineThicknessOptions: ...
    @RaysLineThickness.setter
    def RaysLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def Configuration(self) -> int: ...
    @Configuration.setter
    def Configuration(self, value: int) -> None: ...
    @property
    def ImageExportData(self) -> IImageExportData: ...
    def SetFieldsAll(self) -> None: ...
    def SetWavelengthsAll(self) -> None: ...

class IImageExportData:
    @property
    def Width(self) -> int: ...
    @property
    def Height(self) -> int: ...
    @property
    def Values(self) -> list[list[IImagePixel]]: ...
    def FillValues(self, fullSize: int) -> tuple[list[int], list[int], list[int]]: ...
    @overload
    def GetImagePixel(self, index: int) -> IImagePixel: ...
    @overload
    def GetImagePixel(self, x: int, y: int) -> IImagePixel: ...

class IImagePixel:
    @property
    def R(self) -> int: ...
    @property
    def G(self) -> int: ...
    @property
    def B(self) -> int: ...

class INSC3DLayoutExport(ISystemTool):
    @property
    def SaveImageAsFile(self) -> bool: ...
    @SaveImageAsFile.setter
    def SaveImageAsFile(self, value: bool) -> None: ...
    @property
    def OutputFileName(self) -> str: ...
    @OutputFileName.setter
    def OutputFileName(self, value: str) -> None: ...
    @property
    def IsValidFileName(self) -> bool: ...
    @property
    def OutputPixelWidth(self) -> int: ...
    @OutputPixelWidth.setter
    def OutputPixelWidth(self, value: int) -> None: ...
    @property
    def OutputPixelHeight(self) -> int: ...
    @OutputPixelHeight.setter
    def OutputPixelHeight(self, value: int) -> None: ...
    @property
    def RayDatabase(self) -> str: ...
    @RayDatabase.setter
    def RayDatabase(self, value: str) -> None: ...
    @property
    def Filter(self) -> str: ...
    @Filter.setter
    def Filter(self, value: str) -> None: ...
    @property
    def RayTrace(self) -> RayTraceOptions: ...
    @RayTrace.setter
    def RayTrace(self, value: RayTraceOptions) -> None: ...
    @property
    def ColorRaysBy(self) -> ColorRaysByNSCOptions: ...
    @ColorRaysBy.setter
    def ColorRaysBy(self, value: ColorRaysByNSCOptions) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def FletchRays(self) -> bool: ...
    @FletchRays.setter
    def FletchRays(self, value: bool) -> None: ...
    @property
    def SplitNSCRays(self) -> bool: ...
    @SplitNSCRays.setter
    def SplitNSCRays(self, value: bool) -> None: ...
    @property
    def ScatterNSCRays(self) -> bool: ...
    @ScatterNSCRays.setter
    def ScatterNSCRays(self, value: bool) -> None: ...
    @property
    def SurfaceLineThickness(self) -> LineThicknessOptions: ...
    @SurfaceLineThickness.setter
    def SurfaceLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def RaysLineThickness(self) -> LineThicknessOptions: ...
    @RaysLineThickness.setter
    def RaysLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def ConfigurationAll(self) -> bool: ...
    @ConfigurationAll.setter
    def ConfigurationAll(self, value: bool) -> None: ...
    @property
    def ConfigurationCurrent(self) -> bool: ...
    @ConfigurationCurrent.setter
    def ConfigurationCurrent(self, value: bool) -> None: ...
    @property
    def ConfigurationOffsetX(self) -> float: ...
    @ConfigurationOffsetX.setter
    def ConfigurationOffsetX(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetY(self) -> float: ...
    @ConfigurationOffsetY.setter
    def ConfigurationOffsetY(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetZ(self) -> float: ...
    @ConfigurationOffsetZ.setter
    def ConfigurationOffsetZ(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleX(self) -> float: ...
    @CameraViewpointAngleX.setter
    def CameraViewpointAngleX(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleY(self) -> float: ...
    @CameraViewpointAngleY.setter
    def CameraViewpointAngleY(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleZ(self) -> float: ...
    @CameraViewpointAngleZ.setter
    def CameraViewpointAngleZ(self, value: float) -> None: ...
    @property
    def ImageExportData(self) -> IImageExportData: ...
    def SetCameraViewpoint(self, cameraViewpoint: CameraViewpointOptions) -> None: ...
    def SetConfigurationEnabled(self, config: int, enabled: bool) -> None: ...

class INSCShadedModelExport(ISystemTool):
    @property
    def SaveImageAsFile(self) -> bool: ...
    @SaveImageAsFile.setter
    def SaveImageAsFile(self, value: bool) -> None: ...
    @property
    def OutputFileName(self) -> str: ...
    @OutputFileName.setter
    def OutputFileName(self, value: str) -> None: ...
    @property
    def IsValidFileName(self) -> bool: ...
    @property
    def OutputPixelWidth(self) -> int: ...
    @OutputPixelWidth.setter
    def OutputPixelWidth(self, value: int) -> None: ...
    @property
    def OutputPixelHeight(self) -> int: ...
    @OutputPixelHeight.setter
    def OutputPixelHeight(self, value: int) -> None: ...
    @property
    def RayDatabase(self) -> str: ...
    @RayDatabase.setter
    def RayDatabase(self, value: str) -> None: ...
    @property
    def Filter(self) -> str: ...
    @Filter.setter
    def Filter(self, value: str) -> None: ...
    @property
    def RayTrace(self) -> RayTraceOptions: ...
    @RayTrace.setter
    def RayTrace(self, value: RayTraceOptions) -> None: ...
    @property
    def ColorRaysBy(self) -> ColorRaysByNSCOptions: ...
    @ColorRaysBy.setter
    def ColorRaysBy(self, value: ColorRaysByNSCOptions) -> None: ...
    @property
    def DetectorPixelColorMode(self) -> DetectorPixelColorOptions: ...
    @DetectorPixelColorMode.setter
    def DetectorPixelColorMode(self, value: DetectorPixelColorOptions) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def FletchRays(self) -> bool: ...
    @FletchRays.setter
    def FletchRays(self, value: bool) -> None: ...
    @property
    def SplitNSCRays(self) -> bool: ...
    @SplitNSCRays.setter
    def SplitNSCRays(self, value: bool) -> None: ...
    @property
    def ScatterNSCRays(self) -> bool: ...
    @ScatterNSCRays.setter
    def ScatterNSCRays(self, value: bool) -> None: ...
    @property
    def SurfaceLineThickness(self) -> LineThicknessOptions: ...
    @SurfaceLineThickness.setter
    def SurfaceLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def RaysLineThickness(self) -> LineThicknessOptions: ...
    @RaysLineThickness.setter
    def RaysLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def ConfigurationAll(self) -> bool: ...
    @ConfigurationAll.setter
    def ConfigurationAll(self, value: bool) -> None: ...
    @property
    def ConfigurationCurrent(self) -> bool: ...
    @ConfigurationCurrent.setter
    def ConfigurationCurrent(self, value: bool) -> None: ...
    @property
    def ConfigurationOffsetX(self) -> float: ...
    @ConfigurationOffsetX.setter
    def ConfigurationOffsetX(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetY(self) -> float: ...
    @ConfigurationOffsetY.setter
    def ConfigurationOffsetY(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetZ(self) -> float: ...
    @ConfigurationOffsetZ.setter
    def ConfigurationOffsetZ(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleX(self) -> float: ...
    @CameraViewpointAngleX.setter
    def CameraViewpointAngleX(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleY(self) -> float: ...
    @CameraViewpointAngleY.setter
    def CameraViewpointAngleY(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleZ(self) -> float: ...
    @CameraViewpointAngleZ.setter
    def CameraViewpointAngleZ(self, value: float) -> None: ...
    @property
    def ImageExportData(self) -> IImageExportData: ...
    @property
    def DetectorDisplayMode(self) -> DetectorDisplayModeOptions: ...
    @DetectorDisplayMode.setter
    def DetectorDisplayMode(self, value: DetectorDisplayModeOptions) -> None: ...
    @property
    def Opacity(self) -> OpacityOptions: ...
    @Opacity.setter
    def Opacity(self, value: OpacityOptions) -> None: ...
    @property
    def Background(self) -> BackgroundOptions: ...
    @Background.setter
    def Background(self, value: BackgroundOptions) -> None: ...
    @property
    def Brightness(self) -> BrightnessOptions: ...
    @Brightness.setter
    def Brightness(self, value: BrightnessOptions) -> None: ...
    def SetCameraViewpoint(self, cameraViewpoint: CameraViewpointOptions) -> None: ...
    def SetConfigurationEnabled(self, config: int, enabled: bool) -> None: ...

class IShadedModelExport(ISystemTool):
    @property
    def SaveImageAsFile(self) -> bool: ...
    @SaveImageAsFile.setter
    def SaveImageAsFile(self, value: bool) -> None: ...
    @property
    def OutputFileName(self) -> str: ...
    @OutputFileName.setter
    def OutputFileName(self, value: str) -> None: ...
    @property
    def IsValidFileName(self) -> bool: ...
    @property
    def OutputPixelWidth(self) -> int: ...
    @OutputPixelWidth.setter
    def OutputPixelWidth(self, value: int) -> None: ...
    @property
    def OutputPixelHeight(self) -> int: ...
    @OutputPixelHeight.setter
    def OutputPixelHeight(self, value: int) -> None: ...
    @property
    def StartSurface(self) -> int: ...
    @StartSurface.setter
    def StartSurface(self, value: int) -> None: ...
    @property
    def EndSurface(self) -> int: ...
    @EndSurface.setter
    def EndSurface(self, value: int) -> None: ...
    @property
    def NumberOfRays(self) -> int: ...
    @NumberOfRays.setter
    def NumberOfRays(self, value: int) -> None: ...
    @property
    def ColorRaysBy(self) -> ColorRaysByOptions: ...
    @ColorRaysBy.setter
    def ColorRaysBy(self, value: ColorRaysByOptions) -> None: ...
    @property
    def RayPattern(self) -> RayPatternType: ...
    @RayPattern.setter
    def RayPattern(self, value: RayPatternType) -> None: ...
    @property
    def Wavelength(self) -> int: ...
    @Wavelength.setter
    def Wavelength(self, value: int) -> None: ...
    @property
    def Field(self) -> int: ...
    @Field.setter
    def Field(self, value: int) -> None: ...
    @property
    def Opacity(self) -> OpacityOptions: ...
    @Opacity.setter
    def Opacity(self, value: OpacityOptions) -> None: ...
    @property
    def Background(self) -> BackgroundOptions: ...
    @Background.setter
    def Background(self, value: BackgroundOptions) -> None: ...
    @property
    def Brightness(self) -> BrightnessOptions: ...
    @Brightness.setter
    def Brightness(self, value: BrightnessOptions) -> None: ...
    @property
    def AngularSegments(self) -> NumberSegmentsOptions: ...
    @AngularSegments.setter
    def AngularSegments(self, value: NumberSegmentsOptions) -> None: ...
    @property
    def RadialSegments(self) -> NumberSegmentsOptions: ...
    @RadialSegments.setter
    def RadialSegments(self, value: NumberSegmentsOptions) -> None: ...
    @property
    def FletchRays(self) -> bool: ...
    @FletchRays.setter
    def FletchRays(self, value: bool) -> None: ...
    @property
    def DeleteVignetted(self) -> bool: ...
    @DeleteVignetted.setter
    def DeleteVignetted(self, value: bool) -> None: ...
    @property
    def SplitNSCRays(self) -> bool: ...
    @SplitNSCRays.setter
    def SplitNSCRays(self, value: bool) -> None: ...
    @property
    def ScatterNSCRays(self) -> bool: ...
    @ScatterNSCRays.setter
    def ScatterNSCRays(self, value: bool) -> None: ...
    @property
    def SurfaceLineThickness(self) -> LineThicknessOptions: ...
    @SurfaceLineThickness.setter
    def SurfaceLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def RaysLineThickness(self) -> LineThicknessOptions: ...
    @RaysLineThickness.setter
    def RaysLineThickness(self, value: LineThicknessOptions) -> None: ...
    @property
    def ImageExportData(self) -> IImageExportData: ...
    @property
    def ConfigurationAll(self) -> bool: ...
    @ConfigurationAll.setter
    def ConfigurationAll(self, value: bool) -> None: ...
    @property
    def ConfigurationCurrent(self) -> bool: ...
    @ConfigurationCurrent.setter
    def ConfigurationCurrent(self, value: bool) -> None: ...
    @property
    def ConfigurationOffsetX(self) -> float: ...
    @ConfigurationOffsetX.setter
    def ConfigurationOffsetX(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetY(self) -> float: ...
    @ConfigurationOffsetY.setter
    def ConfigurationOffsetY(self, value: float) -> None: ...
    @property
    def ConfigurationOffsetZ(self) -> float: ...
    @ConfigurationOffsetZ.setter
    def ConfigurationOffsetZ(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleX(self) -> float: ...
    @CameraViewpointAngleX.setter
    def CameraViewpointAngleX(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleY(self) -> float: ...
    @CameraViewpointAngleY.setter
    def CameraViewpointAngleY(self, value: float) -> None: ...
    @property
    def CameraViewpointAngleZ(self) -> float: ...
    @CameraViewpointAngleZ.setter
    def CameraViewpointAngleZ(self, value: float) -> None: ...
    @property
    def DrawSection(self) -> DrawSectionOptions: ...
    @DrawSection.setter
    def DrawSection(self, value: DrawSectionOptions) -> None: ...
    def SetCameraViewpoint(self, cameraViewpoint: CameraViewpointOptions) -> None: ...
    def SetConfigurationEnabled(self, config: int, enabled: bool) -> None: ...
    def SetFieldsAll(self) -> None: ...
    def SetWavelengthsAll(self) -> None: ...

class LineThicknessOptions:
    Standard = 0
    Thick = 1
    Thickest = 2
    Thinnest = -2
    Thin = -1

class NumberSegmentsOptions:
    S_8 = 0
    S_16 = 1
    S_32 = 2
    S_64 = 3
    S_128 = 4

class OpacityOptions:
    Ignore = 0
    Consider = 1
    All50Percent = 2

class RayTraceOptions:
    UseRays = 0
    LightningTraceTrueColor = 1
    LightningTraceAvgWavelength = 2

class RealPupilOptions:
    Pupils_Off = 0
    Pupils_4 = 4
    Pupils_8 = 8
    Pupils_16 = 16
    Pupils_32 = 32
