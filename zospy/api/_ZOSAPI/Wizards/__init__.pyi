"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = (
    "CriterionTypes",
    "DefaultAndDegrees",
    "DefaultAndFringes",
    "IImageData",
    "IImageData",
    "INSCBitmapWizard",
    "INSCOptimizationWizard",
    "INSCRoadwayLightingWizard",
    "INSCToleranceWizard",
    "INSCWizard",
    "ISEQOptimizationWizard",
    "ISEQOptimizationWizard2",
    "ISEQToleranceWizard",
    "IToleranceWizard",
    "IWizard",
    "IWizard",
    "OptimizationTypes",
    "PupilArmsCount",
    "ReferenceTypes",
    "ToleranceGrade",
    "ToleranceVendor",
    "WizardType",
)

class CriterionTypes:
    Wavefront = 0
    Contrast = 1
    Spot = 2
    Angular = 3

class DefaultAndDegrees:
    Default = 0
    Degrees = 1

class DefaultAndFringes:
    Default = 0
    Fringes = 1
    Percent = 2

class IImageData:
    @property
    def BitsPerPixel(self) -> int: ...
    @property
    def Channels(self) -> int: ...
    @property
    def Height(self) -> int: ...
    @property
    def ImageName(self) -> str: ...
    @property
    def IsRGB(self) -> bool: ...
    @property
    def Stride(self) -> int: ...
    @property
    def Width(self) -> int: ...
    def GetPixels(self) -> list[Byte]: ...
    def GetPixelsSafe(self, totalSize: int, height: int, width: int) -> tuple[list[Byte]]: ...
    def GetRawData(self) -> list[Byte]: ...
    def GetRawDataSafe(self, totalSize: int, height: int, width: int) -> tuple[list[Byte]]: ...

class INSCBitmapWizard(INSCWizard, IWizard):
    @property
    def CommonSettings(self) -> IWizard: ...
    @property
    def NSCSettings(self) -> INSCWizard: ...
    @property
    def NumberOfBitmapFiles(self) -> int: ...
    def GetBitmapFileAt(self, idx: int) -> str: ...
    def GetPreviewImage(self) -> IImageData: ...

class INSCOptimizationWizard(INSCWizard, IWizard):
    @property
    def CommonSettings(self) -> IWizard: ...
    @property
    def NSCSettings(self) -> INSCWizard: ...

class INSCRoadwayLightingWizard(IWizard):
    @property
    def Arrangement(self) -> int: ...
    @property
    def CommonSettings(self) -> IWizard: ...
    @property
    def Configuration(self) -> int: ...
    @property
    def IsIgnoreErrorsUsed(self) -> bool: ...
    @property
    def IsNSCRoadwayLightingWizard(self) -> bool: ...
    @property
    def IsScatterRaysUsed(self) -> bool: ...
    @property
    def IsSplitRaysUsed(self) -> bool: ...
    @property
    def IsUsePolarizationUsed(self) -> bool: ...
    @property
    def LaneWidth(self) -> float: ...
    @property
    def LateralOffset(self) -> float: ...
    @property
    def LongitudinalSpacing(self) -> float: ...
    @property
    def MountingHeight(self) -> float: ...
    @property
    def NumberOfArrangements(self) -> int: ...
    @property
    def NumberOfClassifications(self) -> int: ...
    @property
    def NumberOfConfigurations(self) -> int: ...
    @property
    def NumberOfLanes(self) -> int: ...
    @property
    def NumberOfOrigins(self) -> int: ...
    @property
    def NumberOfRoadClasses(self) -> int: ...
    @property
    def Origin(self) -> int: ...
    @property
    def OverallWeight(self) -> float: ...
    @property
    def RoadClass(self) -> int: ...
    @property
    def StartAt(self) -> int: ...
    @property
    def SurfaceClassification(self) -> int: ...
    def GetArrangementAt(self, idx: int) -> str: ...
    def GetClassificationAt(self, idx: int) -> str: ...
    def GetConfigurationAt(self, idx: int) -> str: ...
    def GetOriginAt(self, idx: int) -> str: ...
    def GetRoadClassAt(self, idx: int) -> str: ...
    @Arrangement.setter
    def Arrangement(self, value: int) -> None: ...
    @Configuration.setter
    def Configuration(self, value: int) -> None: ...
    @IsIgnoreErrorsUsed.setter
    def IsIgnoreErrorsUsed(self, value: bool) -> None: ...
    @IsScatterRaysUsed.setter
    def IsScatterRaysUsed(self, value: bool) -> None: ...
    @IsSplitRaysUsed.setter
    def IsSplitRaysUsed(self, value: bool) -> None: ...
    @IsUsePolarizationUsed.setter
    def IsUsePolarizationUsed(self, value: bool) -> None: ...
    @LaneWidth.setter
    def LaneWidth(self, value: float) -> None: ...
    @LateralOffset.setter
    def LateralOffset(self, value: float) -> None: ...
    @LongitudinalSpacing.setter
    def LongitudinalSpacing(self, value: float) -> None: ...
    @MountingHeight.setter
    def MountingHeight(self, value: float) -> None: ...
    @NumberOfLanes.setter
    def NumberOfLanes(self, value: int) -> None: ...
    @Origin.setter
    def Origin(self, value: int) -> None: ...
    @OverallWeight.setter
    def OverallWeight(self, value: float) -> None: ...
    @RoadClass.setter
    def RoadClass(self, value: int) -> None: ...
    @StartAt.setter
    def StartAt(self, value: int) -> None: ...
    @SurfaceClassification.setter
    def SurfaceClassification(self, value: int) -> None: ...

class INSCToleranceWizard(IToleranceWizard, IWizard):
    @property
    def ToleranceSettings(self) -> IToleranceWizard: ...

class INSCWizard(IWizard):
    @property
    def BitmapFile(self) -> int: ...
    @property
    def Boundary(self) -> int: ...
    @property
    def ClearDetector(self) -> int: ...
    @property
    def Configuration(self) -> int: ...
    @property
    def Criterion(self) -> int: ...
    @property
    def EdgeSampling(self) -> int: ...
    @property
    def IsClearDataSettingsUsed(self) -> bool: ...
    @property
    def IsColorTargetsUsed(self) -> bool: ...
    @property
    def IsCriterionSettingsUsed(self) -> bool: ...
    @property
    def IsIgnoreErrorsUsed(self) -> bool: ...
    @property
    def IsMinimumFluxUsed(self) -> bool: ...
    @property
    def IsNSCBitmapWizard(self) -> bool: ...
    @property
    def IsNSCOptimizingWizard(self) -> bool: ...
    @property
    def IsOverwriteUsed(self) -> bool: ...
    @property
    def IsRaytraceSettingsUsed(self) -> bool: ...
    @property
    def IsResampleDetectorUsed(self) -> bool: ...
    @property
    def IsScatterRaysUsed(self) -> bool: ...
    @property
    def IsSplitRaysUsed(self) -> bool: ...
    @property
    def IsTargetSettingsUsed(self) -> bool: ...
    @property
    def IsUseLightningTraceUsed(self) -> bool: ...
    @property
    def IsUsePolarizationUsed(self) -> bool: ...
    @property
    def MinimumFlux(self) -> float: ...
    @property
    def NumberOfBoundaries(self) -> int: ...
    @property
    def NumberOfConfigurations(self) -> int: ...
    @property
    def NumberOfCriterion(self) -> int: ...
    @property
    def NumberOfDetectors(self) -> int: ...
    @property
    def NumberOfEdgeSamplings(self) -> int: ...
    @property
    def NumberOfRaySamplings(self) -> int: ...
    @property
    def NumberOfSources(self) -> int: ...
    @property
    def OverallWeight(self) -> float: ...
    @property
    def RaySampling(self) -> int: ...
    @property
    def StartAt(self) -> int: ...
    @property
    def Target(self) -> float: ...
    @property
    def TotalFlux(self) -> float: ...
    @property
    def UseDetector(self) -> int: ...
    @property
    def UseSource(self) -> int: ...
    def GetBoundaryAt(self, idx: int) -> str: ...
    def GetConfigurationAt(self, idx: int) -> str: ...
    def GetCriterionAt(self, idx: int) -> str: ...
    def GetDetectorAt(self, idx: int) -> str: ...
    def GetEdgeSamplingAt(self, idx: int) -> str: ...
    def GetRaySamplingAt(self, idx: int) -> str: ...
    def GetSourceAt(self, idx: int) -> str: ...
    @BitmapFile.setter
    def BitmapFile(self, value: int) -> None: ...
    @Boundary.setter
    def Boundary(self, value: int) -> None: ...
    @ClearDetector.setter
    def ClearDetector(self, value: int) -> None: ...
    @Configuration.setter
    def Configuration(self, value: int) -> None: ...
    @Criterion.setter
    def Criterion(self, value: int) -> None: ...
    @EdgeSampling.setter
    def EdgeSampling(self, value: int) -> None: ...
    @IsClearDataSettingsUsed.setter
    def IsClearDataSettingsUsed(self, value: bool) -> None: ...
    @IsColorTargetsUsed.setter
    def IsColorTargetsUsed(self, value: bool) -> None: ...
    @IsCriterionSettingsUsed.setter
    def IsCriterionSettingsUsed(self, value: bool) -> None: ...
    @IsIgnoreErrorsUsed.setter
    def IsIgnoreErrorsUsed(self, value: bool) -> None: ...
    @IsMinimumFluxUsed.setter
    def IsMinimumFluxUsed(self, value: bool) -> None: ...
    @IsOverwriteUsed.setter
    def IsOverwriteUsed(self, value: bool) -> None: ...
    @IsRaytraceSettingsUsed.setter
    def IsRaytraceSettingsUsed(self, value: bool) -> None: ...
    @IsResampleDetectorUsed.setter
    def IsResampleDetectorUsed(self, value: bool) -> None: ...
    @IsScatterRaysUsed.setter
    def IsScatterRaysUsed(self, value: bool) -> None: ...
    @IsSplitRaysUsed.setter
    def IsSplitRaysUsed(self, value: bool) -> None: ...
    @IsTargetSettingsUsed.setter
    def IsTargetSettingsUsed(self, value: bool) -> None: ...
    @IsUseLightningTraceUsed.setter
    def IsUseLightningTraceUsed(self, value: bool) -> None: ...
    @IsUsePolarizationUsed.setter
    def IsUsePolarizationUsed(self, value: bool) -> None: ...
    @MinimumFlux.setter
    def MinimumFlux(self, value: float) -> None: ...
    @OverallWeight.setter
    def OverallWeight(self, value: float) -> None: ...
    @RaySampling.setter
    def RaySampling(self, value: int) -> None: ...
    @StartAt.setter
    def StartAt(self, value: int) -> None: ...
    @Target.setter
    def Target(self, value: float) -> None: ...
    @TotalFlux.setter
    def TotalFlux(self, value: float) -> None: ...
    @UseDetector.setter
    def UseDetector(self, value: int) -> None: ...
    @UseSource.setter
    def UseSource(self, value: int) -> None: ...

class ISEQOptimizationWizard(IWizard):
    @property
    def AirEdge(self) -> float: ...
    @property
    def AirMax(self) -> float: ...
    @property
    def AirMin(self) -> float: ...
    @property
    def Arm(self) -> int: ...
    @property
    def CommonSettings(self) -> IWizard: ...
    @property
    def Configuration(self) -> int: ...
    @property
    def Data(self) -> int: ...
    @property
    def GlassEdge(self) -> float: ...
    @property
    def GlassMax(self) -> float: ...
    @property
    def GlassMin(self) -> float: ...
    @property
    def Grid(self) -> int: ...
    @property
    def IsAddFavoriteOperandsUsed(self) -> bool: ...
    @property
    def IsAirUsed(self) -> bool: ...
    @property
    def IsAssumeAxialSymmetryUsed(self) -> bool: ...
    @property
    def IsDeleteVignetteUsed(self) -> bool: ...
    @property
    def IsGlassUsed(self) -> bool: ...
    @property
    def IsIgnoreLateralColorUsed(self) -> bool: ...
    @property
    def IsRelativeXWeightUsed(self) -> bool: ...
    @property
    def IsSEQOptimizationWizard(self) -> bool: ...
    @property
    def NumberOfArms(self) -> int: ...
    @property
    def NumberOfConfigurations(self) -> int: ...
    @property
    def NumberOfDataTypes(self) -> int: ...
    @property
    def NumberOfGrids(self) -> int: ...
    @property
    def NumberOfPupilIntegrationMethods(self) -> int: ...
    @property
    def NumberOfReferences(self) -> int: ...
    @property
    def NumberOfRings(self) -> int: ...
    @property
    def NumberOfTypes(self) -> int: ...
    @property
    def Obscuration(self) -> float: ...
    @property
    def OverallWeight(self) -> float: ...
    @property
    def PupilIntegrationMethod(self) -> int: ...
    @property
    def Reference(self) -> int: ...
    @property
    def RelativeXWeight(self) -> float: ...
    @property
    def Ring(self) -> int: ...
    @property
    def StartAt(self) -> int: ...
    @property
    def Type(self) -> int: ...
    def GetArmAt(self, idx: int) -> str: ...
    def GetConfigurationAt(self, idx: int) -> str: ...
    def GetDataTypeAt(self, idx: int) -> str: ...
    def GetGridAt(self, idx: int) -> str: ...
    def GetPupilIntegrationMethodAt(self, idx: int) -> str: ...
    def GetReferenceAt(self, idx: int) -> str: ...
    def GetRingAt(self, idx: int) -> str: ...
    def GetTypeAt(self, idx: int) -> str: ...
    @AirEdge.setter
    def AirEdge(self, value: float) -> None: ...
    @AirMax.setter
    def AirMax(self, value: float) -> None: ...
    @AirMin.setter
    def AirMin(self, value: float) -> None: ...
    @Arm.setter
    def Arm(self, value: int) -> None: ...
    @Configuration.setter
    def Configuration(self, value: int) -> None: ...
    @Data.setter
    def Data(self, value: int) -> None: ...
    @GlassEdge.setter
    def GlassEdge(self, value: float) -> None: ...
    @GlassMax.setter
    def GlassMax(self, value: float) -> None: ...
    @GlassMin.setter
    def GlassMin(self, value: float) -> None: ...
    @Grid.setter
    def Grid(self, value: int) -> None: ...
    @IsAddFavoriteOperandsUsed.setter
    def IsAddFavoriteOperandsUsed(self, value: bool) -> None: ...
    @IsAirUsed.setter
    def IsAirUsed(self, value: bool) -> None: ...
    @IsAssumeAxialSymmetryUsed.setter
    def IsAssumeAxialSymmetryUsed(self, value: bool) -> None: ...
    @IsDeleteVignetteUsed.setter
    def IsDeleteVignetteUsed(self, value: bool) -> None: ...
    @IsGlassUsed.setter
    def IsGlassUsed(self, value: bool) -> None: ...
    @IsIgnoreLateralColorUsed.setter
    def IsIgnoreLateralColorUsed(self, value: bool) -> None: ...
    @IsRelativeXWeightUsed.setter
    def IsRelativeXWeightUsed(self, value: bool) -> None: ...
    @Obscuration.setter
    def Obscuration(self, value: float) -> None: ...
    @OverallWeight.setter
    def OverallWeight(self, value: float) -> None: ...
    @PupilIntegrationMethod.setter
    def PupilIntegrationMethod(self, value: int) -> None: ...
    @Reference.setter
    def Reference(self, value: int) -> None: ...
    @RelativeXWeight.setter
    def RelativeXWeight(self, value: float) -> None: ...
    @Ring.setter
    def Ring(self, value: int) -> None: ...
    @StartAt.setter
    def StartAt(self, value: int) -> None: ...
    @Type.setter
    def Type(self, value: int) -> None: ...

class ISEQOptimizationWizard2(IWizard):
    @property
    def AddFavoriteOperands(self) -> bool: ...
    @property
    def AirEdgeThickness(self) -> float: ...
    @property
    def AirMax(self) -> float: ...
    @property
    def AirMin(self) -> float: ...
    @property
    def Arms(self) -> PupilArmsCount: ...
    @property
    def AssumeAxialSymmetry(self) -> bool: ...
    @property
    def CommonSettings(self) -> IWizard: ...
    @property
    def ConfigurationNumber(self) -> int: ...
    @property
    def Criterion(self) -> CriterionTypes: ...
    @property
    def DeleteVignetted(self) -> bool: ...
    @property
    def FieldNumber(self) -> int: ...
    @property
    def GlassEdgeThickness(self) -> float: ...
    @property
    def GlassMax(self) -> float: ...
    @property
    def GlassMin(self) -> float: ...
    @property
    def GridSizeNxN(self) -> int: ...
    @property
    def IgnoreLateralColor(self) -> bool: ...
    @property
    def IsHighManufacturingYieldAvailable(self) -> bool: ...
    @property
    def ManufacturingYieldWeight(self) -> float: ...
    @property
    def MaxDistortionPct(self) -> float: ...
    @property
    def Obscuration(self) -> float: ...
    @property
    def OptimizeForBestNominalPerformance(self) -> bool: ...
    @property
    def OptimizeForManufacturingYield(self) -> bool: ...
    @property
    def OverallWeight(self) -> float: ...
    @property
    def Reference(self) -> ReferenceTypes: ...
    @property
    def Rings(self) -> int: ...
    @property
    def SpatialFrequency(self) -> float: ...
    @property
    def StartAt(self) -> int: ...
    @property
    def Type(self) -> OptimizationTypes: ...
    @property
    def UseAirBoundaryValues(self) -> bool: ...
    @property
    def UseAllConfigurations(self) -> bool: ...
    @property
    def UseAllFields(self) -> bool: ...
    @property
    def UseGaussianQuadrature(self) -> bool: ...
    @property
    def UseGlassBoundaryValues(self) -> bool: ...
    @property
    def UseMaximumDistortion(self) -> bool: ...
    @property
    def UseRectangularArray(self) -> bool: ...
    @property
    def XSWeight(self) -> float: ...
    @property
    def YTWeight(self) -> float: ...
    @AddFavoriteOperands.setter
    def AddFavoriteOperands(self, value: bool) -> None: ...
    @AirEdgeThickness.setter
    def AirEdgeThickness(self, value: float) -> None: ...
    @AirMax.setter
    def AirMax(self, value: float) -> None: ...
    @AirMin.setter
    def AirMin(self, value: float) -> None: ...
    @Arms.setter
    def Arms(self, value: PupilArmsCount) -> None: ...
    @AssumeAxialSymmetry.setter
    def AssumeAxialSymmetry(self, value: bool) -> None: ...
    @ConfigurationNumber.setter
    def ConfigurationNumber(self, value: int) -> None: ...
    @Criterion.setter
    def Criterion(self, value: CriterionTypes) -> None: ...
    @DeleteVignetted.setter
    def DeleteVignetted(self, value: bool) -> None: ...
    @FieldNumber.setter
    def FieldNumber(self, value: int) -> None: ...
    @GlassEdgeThickness.setter
    def GlassEdgeThickness(self, value: float) -> None: ...
    @GlassMax.setter
    def GlassMax(self, value: float) -> None: ...
    @GlassMin.setter
    def GlassMin(self, value: float) -> None: ...
    @GridSizeNxN.setter
    def GridSizeNxN(self, value: int) -> None: ...
    @IgnoreLateralColor.setter
    def IgnoreLateralColor(self, value: bool) -> None: ...
    @ManufacturingYieldWeight.setter
    def ManufacturingYieldWeight(self, value: float) -> None: ...
    @MaxDistortionPct.setter
    def MaxDistortionPct(self, value: float) -> None: ...
    @Obscuration.setter
    def Obscuration(self, value: float) -> None: ...
    @OptimizeForBestNominalPerformance.setter
    def OptimizeForBestNominalPerformance(self, value: bool) -> None: ...
    @OptimizeForManufacturingYield.setter
    def OptimizeForManufacturingYield(self, value: bool) -> None: ...
    @OverallWeight.setter
    def OverallWeight(self, value: float) -> None: ...
    @Reference.setter
    def Reference(self, value: ReferenceTypes) -> None: ...
    @Rings.setter
    def Rings(self, value: int) -> None: ...
    @SpatialFrequency.setter
    def SpatialFrequency(self, value: float) -> None: ...
    @StartAt.setter
    def StartAt(self, value: int) -> None: ...
    @Type.setter
    def Type(self, value: OptimizationTypes) -> None: ...
    @UseAirBoundaryValues.setter
    def UseAirBoundaryValues(self, value: bool) -> None: ...
    @UseAllConfigurations.setter
    def UseAllConfigurations(self, value: bool) -> None: ...
    @UseAllFields.setter
    def UseAllFields(self, value: bool) -> None: ...
    @UseGaussianQuadrature.setter
    def UseGaussianQuadrature(self, value: bool) -> None: ...
    @UseGlassBoundaryValues.setter
    def UseGlassBoundaryValues(self, value: bool) -> None: ...
    @UseMaximumDistortion.setter
    def UseMaximumDistortion(self, value: bool) -> None: ...
    @UseRectangularArray.setter
    def UseRectangularArray(self, value: bool) -> None: ...
    @XSWeight.setter
    def XSWeight(self, value: float) -> None: ...
    @YTWeight.setter
    def YTWeight(self, value: float) -> None: ...

class ISEQToleranceWizard(IToleranceWizard, IWizard):
    @property
    def ToleranceSettings(self) -> IToleranceWizard: ...

class IToleranceWizard(IWizard):
    @property
    def CommonSettings(self) -> IWizard: ...
    @property
    def ElementDecenterX(self) -> float: ...
    @property
    def ElementDecenterY(self) -> float: ...
    @property
    def ElementTiltXDegrees(self) -> float: ...
    @property
    def ElementTiltYDegrees(self) -> float: ...
    @property
    def Index(self) -> float: ...
    @property
    def IndexAbbePercentage(self) -> float: ...
    @property
    def IsElementDecenterXUsed(self) -> bool: ...
    @property
    def IsElementDecenterYUsed(self) -> bool: ...
    @property
    def IsElementTiltXUsed(self) -> bool: ...
    @property
    def IsElementTiltYUsed(self) -> bool: ...
    @property
    def IsFocusCompensationUsed(self) -> bool: ...
    @property
    def IsIndexAbbePercentageUsed(self) -> bool: ...
    @property
    def IsIndexUsed(self) -> bool: ...
    @property
    def IsSEQToleranceWizard(self) -> bool: ...
    @property
    def IsSurfaceDecenterXUsed(self) -> bool: ...
    @property
    def IsSurfaceDecenterYUsed(self) -> bool: ...
    @property
    def IsSurfaceRadiusUsed(self) -> bool: ...
    @property
    def IsSurfaceSandAIrregularityUsed(self) -> bool: ...
    @property
    def IsSurfaceThicknessUsed(self) -> bool: ...
    @property
    def IsSurfaceTiltXUsed(self) -> bool: ...
    @property
    def IsSurfaceTiltYUsed(self) -> bool: ...
    @property
    def IsSurfaceZernikeIrregularityUsed(self) -> bool: ...
    @property
    def StartAt(self) -> int: ...
    @property
    def StartAtSurface(self) -> int: ...
    @property
    def StopAtSurface(self) -> int: ...
    @property
    def SurfaceDecenterX(self) -> float: ...
    @property
    def SurfaceDecenterY(self) -> float: ...
    @property
    def SurfaceRadius(self) -> float: ...
    @property
    def SurfaceRadiusFringes(self) -> float: ...
    @property
    def SurfaceRadiusPercent(self) -> float: ...
    @property
    def SurfaceRadiusUnitType(self) -> DefaultAndFringes: ...
    @property
    def SurfaceSandAIrregularityFringes(self) -> float: ...
    @property
    def SurfaceThickness(self) -> float: ...
    @property
    def SurfaceTiltX(self) -> float: ...
    @property
    def SurfaceTiltXDegrees(self) -> float: ...
    @property
    def SurfaceTiltXUnitType(self) -> DefaultAndDegrees: ...
    @property
    def SurfaceTiltY(self) -> float: ...
    @property
    def SurfaceTiltYDegrees(self) -> float: ...
    @property
    def SurfaceTiltYUnitType(self) -> DefaultAndDegrees: ...
    @property
    def SurfaceZernikeIrregularityFringes(self) -> float: ...
    @property
    def TestWavelength(self) -> float: ...
    def SelectTolerancePreset(self, vendor: ToleranceVendor, grade: ToleranceGrade) -> None: ...
    @ElementDecenterX.setter
    def ElementDecenterX(self, value: float) -> None: ...
    @ElementDecenterY.setter
    def ElementDecenterY(self, value: float) -> None: ...
    @ElementTiltXDegrees.setter
    def ElementTiltXDegrees(self, value: float) -> None: ...
    @ElementTiltYDegrees.setter
    def ElementTiltYDegrees(self, value: float) -> None: ...
    @Index.setter
    def Index(self, value: float) -> None: ...
    @IndexAbbePercentage.setter
    def IndexAbbePercentage(self, value: float) -> None: ...
    @IsElementDecenterXUsed.setter
    def IsElementDecenterXUsed(self, value: bool) -> None: ...
    @IsElementDecenterYUsed.setter
    def IsElementDecenterYUsed(self, value: bool) -> None: ...
    @IsElementTiltXUsed.setter
    def IsElementTiltXUsed(self, value: bool) -> None: ...
    @IsElementTiltYUsed.setter
    def IsElementTiltYUsed(self, value: bool) -> None: ...
    @IsFocusCompensationUsed.setter
    def IsFocusCompensationUsed(self, value: bool) -> None: ...
    @IsIndexAbbePercentageUsed.setter
    def IsIndexAbbePercentageUsed(self, value: bool) -> None: ...
    @IsIndexUsed.setter
    def IsIndexUsed(self, value: bool) -> None: ...
    @IsSurfaceDecenterXUsed.setter
    def IsSurfaceDecenterXUsed(self, value: bool) -> None: ...
    @IsSurfaceDecenterYUsed.setter
    def IsSurfaceDecenterYUsed(self, value: bool) -> None: ...
    @IsSurfaceRadiusUsed.setter
    def IsSurfaceRadiusUsed(self, value: bool) -> None: ...
    @IsSurfaceSandAIrregularityUsed.setter
    def IsSurfaceSandAIrregularityUsed(self, value: bool) -> None: ...
    @IsSurfaceThicknessUsed.setter
    def IsSurfaceThicknessUsed(self, value: bool) -> None: ...
    @IsSurfaceTiltXUsed.setter
    def IsSurfaceTiltXUsed(self, value: bool) -> None: ...
    @IsSurfaceTiltYUsed.setter
    def IsSurfaceTiltYUsed(self, value: bool) -> None: ...
    @IsSurfaceZernikeIrregularityUsed.setter
    def IsSurfaceZernikeIrregularityUsed(self, value: bool) -> None: ...
    @StartAt.setter
    def StartAt(self, value: int) -> None: ...
    @StartAtSurface.setter
    def StartAtSurface(self, value: int) -> None: ...
    @StopAtSurface.setter
    def StopAtSurface(self, value: int) -> None: ...
    @SurfaceDecenterX.setter
    def SurfaceDecenterX(self, value: float) -> None: ...
    @SurfaceDecenterY.setter
    def SurfaceDecenterY(self, value: float) -> None: ...
    @SurfaceRadius.setter
    def SurfaceRadius(self, value: float) -> None: ...
    @SurfaceRadiusFringes.setter
    def SurfaceRadiusFringes(self, value: float) -> None: ...
    @SurfaceRadiusPercent.setter
    def SurfaceRadiusPercent(self, value: float) -> None: ...
    @SurfaceRadiusUnitType.setter
    def SurfaceRadiusUnitType(self, value: DefaultAndFringes) -> None: ...
    @SurfaceSandAIrregularityFringes.setter
    def SurfaceSandAIrregularityFringes(self, value: float) -> None: ...
    @SurfaceThickness.setter
    def SurfaceThickness(self, value: float) -> None: ...
    @SurfaceTiltX.setter
    def SurfaceTiltX(self, value: float) -> None: ...
    @SurfaceTiltXDegrees.setter
    def SurfaceTiltXDegrees(self, value: float) -> None: ...
    @SurfaceTiltXUnitType.setter
    def SurfaceTiltXUnitType(self, value: DefaultAndDegrees) -> None: ...
    @SurfaceTiltY.setter
    def SurfaceTiltY(self, value: float) -> None: ...
    @SurfaceTiltYDegrees.setter
    def SurfaceTiltYDegrees(self, value: float) -> None: ...
    @SurfaceTiltYUnitType.setter
    def SurfaceTiltYUnitType(self, value: DefaultAndDegrees) -> None: ...
    @SurfaceZernikeIrregularityFringes.setter
    def SurfaceZernikeIrregularityFringes(self, value: float) -> None: ...
    @TestWavelength.setter
    def TestWavelength(self, value: float) -> None: ...

class IWizard:
    def Apply(self) -> None: ...
    @property
    def Wizard(self) -> WizardType: ...
    def Initialize(self) -> None: ...
    def LoadSettings(self) -> None: ...
    def OK(self) -> None: ...
    def ResetSettings(self) -> None: ...
    def SaveSettings(self) -> None: ...

class OptimizationTypes:
    RMS = 0
    PTV = 1

class PupilArmsCount:
    Arms_6 = 0
    Arms_8 = 1
    Arms_10 = 2
    Arms_12 = 3

class ReferenceTypes:
    Centroid = 0
    ChiefRay = 1
    Unreferenced = 2

class ToleranceGrade:
    Commercial = 0
    Precision = 1
    HighPrecision = 2
    CellPhoneLens = 3

class ToleranceVendor:
    Asphericon = 0
    EdmundOptics = 1
    Generic = 2
    LaCroix = 3
    Optimax = 4

class WizardType:
    NSCOptimization = 0
    NSCBitmap = 1
    NSCRoadwayLighting = 2
    SEQOptimization = 3
    NSCTolerance = 4
    SEQTolerance = 5