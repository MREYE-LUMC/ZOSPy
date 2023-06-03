"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from typing import overload

from zospy.api._ZOSAPI.Analysis.Data import IAR_
from zospy.api._ZOSAPI.Analysis.Settings import IAS_
from zospy.api._ZOSAPI.Common import ISettingsData, ZemaxColor

from . import Data, PhysicalOptics, RayTracing, Settings, Tolerancing

__all__ = (
    "Data",
    "PhysicalOptics",
    "RayTracing",
    "Settings",
    "Tolerancing",
    "AnalysisIDM",
    "Beam",
    "BestFitSphereOptions",
    "ColorPaletteType",
    "DetectorViewerShowAsTypes",
    "DetectorViewerShowDataTypes",
    "ErrorType",
    "GiaShowAsTypes",
    "GridPlotType",
    "HuygensShowAsTypes",
    "HuygensSurfaceMftShowAsTypes",
    "I_Analyses",
    "I_Analyses",
    "IA_",
    "IA_",
    "IColorTranslator",
    "IColorTranslator",
    "IMessage",
    "IMessage",
    "IMessages",
    "IMessages",
    "IUser2DLineData",
    "IUser2DLineData",
    "IUserAnalysisData",
    "IUserAnalysisData",
    "IUserGridData",
    "IUserGridData",
    "IUserGridRGBData",
    "IUserGridRGBData",
    "IUserTextData",
    "IUserTextData",
    "POPSampling",
    "RemoveOptions",
    "SampleSizes",
    "SampleSizes_ContrastLoss",
    "SampleSizes_Pow2Plus1",
    "SampleSizes_Pow2Plus1_X",
    "ShowAs",
    "SurfaceCurvatureCrossData",
    "SurfaceCurvatureData",
    "SurfacePhaseData",
    "SurfaceSagData",
    "SurfaceSlopeCrossData",
    "SurfaceSlopeData",
    "UserAnalysisDataType",
)

class AnalysisIDM:
    RayFan = 0
    OpticalPathFan = 1
    PupilAberrationFan = 2
    FieldCurvatureAndDistortion = 3
    FocalShiftDiagram = 4
    GridDistortion = 5
    LateralColor = 6
    LongitudinalAberration = 7
    RayTrace = 8
    SeidelCoefficients = 9
    SeidelDiagram = 10
    ZernikeAnnularCoefficients = 11
    ZernikeCoefficientsVsField = 12
    ZernikeFringeCoefficients = 13
    ZernikeStandardCoefficients = 14
    FftMtf = 15
    FftThroughFocusMtf = 16
    GeometricThroughFocusMtf = 17
    GeometricMtf = 18
    FftMtfMap = 19
    GeometricMtfMap = 20
    FftSurfaceMtf = 21
    FftMtfvsField = 22
    GeometricMtfvsField = 23
    HuygensMtfvsField = 24
    HuygensMtf = 25
    HuygensSurfaceMtf = 26
    HuygensThroughFocusMtf = 27
    FftPsf = 28
    FftPsfCrossSection = 29
    FftPsfLineEdgeSpread = 30
    HuygensPsfCrossSection = 31
    HuygensPsf = 32
    DiffractionEncircledEnergy = 33
    GeometricEncircledEnergy = 34
    GeometricLineEdgeSpread = 35
    ExtendedSourceEncircledEnergy = 36
    SurfaceCurvatureCross = 37
    SurfacePhaseCross = 38
    SurfaceSagCross = 39
    SurfaceCurvature = 40
    SurfacePhase = 41
    SurfaceSag = 42
    StandardSpot = 43
    ThroughFocusSpot = 44
    FullFieldSpot = 45
    MatrixSpot = 46
    ConfigurationMatrixSpot = 47
    RMSField = 48
    RMSFieldMap = 49
    RMSLambdaDiagram = 50
    RMSFocus = 51
    Foucault = 52
    Interferogram = 53
    WavefrontMap = 54
    DetectorViewer = 55
    Draw2D = 56
    Draw3D = 57
    ImageSimulation = 58
    GeometricImageAnalysis = 59
    IMABIMFileViewer = 60
    GeometricBitmapImageAnalysis = 61
    BitmapFileViewer = 62
    LightSourceAnalysis = 63
    PartiallyCoherentImageAnalysis = 64
    ExtendedDiffractionImageAnalysis = 65
    BiocularFieldOfViewAnalysis = 66
    BiocularDipvergenceConvergence = 67
    RelativeIllumination = 68
    VignettingDiagramSettings = 69
    FootprintSettings = 70
    YYbarDiagram = 71
    PowerFieldMapSettings = 72
    PowerPupilMapSettings = 73
    IncidentAnglevsImageHeight = 74
    FiberCouplingSettings = 75
    YNIContributions = 76
    SagTable = 77
    CardinalPoints = 78
    DispersionDiagram = 79
    GlassMap = 80
    AthermalGlassMap = 81
    InternalTransmissionvsWavelength = 82
    DispersionvsWavelength = 83
    GrinProfile = 84
    GradiumProfile = 85
    UniversalPlot1D = 86
    UniversalPlot2D = 87
    PolarizationRayTrace = 88
    PolarizationPupilMap = 89
    Transmission = 90
    PhaseAberration = 91
    TransmissionFan = 92
    ParaxialGaussianBeam = 93
    SkewGaussianBeam = 94
    PhysicalOpticsPropagation = 95
    BeamFileViewer = 96
    ReflectionvsAngle = 97
    TransmissionvsAngle = 98
    AbsorptionvsAngle = 99
    DiattenuationvsAngle = 100
    PhasevsAngle = 101
    RetardancevsAngle = 102
    ReflectionvsWavelength = 103
    TransmissionvsWavelength = 104
    AbsorptionvsWavelength = 105
    DiattenuationvsWavelength = 106
    PhasevsWavelength = 107
    RetardancevsWavelength = 108
    DirectivityPlot = 109
    SourcePolarViewer = 110
    PhotoluminscenceViewer = 111
    SourceSpectrumViewer = 112
    RadiantSourceModelViewerSettings = 113
    SurfaceDataSettings = 114
    PrescriptionDataSettings = 115
    FileComparatorSettings = 116
    PartViewer = 117
    ReverseRadianceAnalysis = 118
    PathAnalysis = 119
    FluxvsWavelength = 120
    RoadwayLighting = 121
    SourceIlluminationMap = 122
    ScatterFunctionViewer = 123
    ScatterPolarPlotSettings = 124
    ZemaxElementDrawing = 125
    ShadedModel = 126
    NSCShadedModel = 127
    NSC3DLayout = 128
    NSCObjectViewer = 129
    RayDatabaseViewer = 130
    ISOElementDrawing = 131
    SystemData = 132
    TestPlateList = 133
    SourceColorChart1931 = 134
    SourceColorChart1976 = 135
    PrescriptionGraphic = 136
    CriticalRayTracer = 137
    ContrastLoss = 138
    CoatingListing = 139
    FullFieldAberration = 140
    SurfaceSlope = 141
    SurfaceSlopeCross = 142
    QuickYield = 143
    SystemCheck = 144
    ToleranceYield = 145
    ToleranceHistogram = 146
    DiffEfficiency2D = 147
    DiffEfficiencyAngular = 148
    DiffEfficiencyChromatic = 149
    NSCSurfaceSag = 150
    NSCSingleRayTrace = 151
    NSCGeometricMtf = 152
    XXXTemplateXXX = -1

class Beam:
    Reference = 0
    Configuration_1 = 1
    Configuration_2 = 2
    Configuration_3 = 3
    Configuration_4 = 4
    Configuration_5 = 5
    Configuration_6 = 6
    Configuration_7 = 7
    Configuration_8 = 8
    Configuration_9 = 9
    Configuration_10 = 10
    Configuration_11 = 11
    Configuration_12 = 12
    Configuration_13 = 13
    Configuration_14 = 14
    Configuration_15 = 15
    Configuration_16 = 16
    Configuration_17 = 17
    Configuration_18 = 18
    Configuration_19 = 19
    Configuration_20 = 20

class BestFitSphereOptions:
    MinimumVolume = 0
    MinimumRMS = 1
    MinimumRMSWithOffset = 2

class ColorPaletteType:
    GreyScale = 0
    FalseColor = 1
    FalseColorOriginal = 2
    Viridis = 3
    Magma = 4

class DetectorViewerShowAsTypes:
    GreyScale = 0
    FullListing = 0
    Text_CrossSection_Row = 1
    AzimuthCrossSection = 1
    GreyScale_Inverted = 1
    Text_CrossSection_Column = 2
    FalseColor = 2
    FluxVsWaveLength = 3
    FalseColor_Inverted = 3
    TrueColor = 4
    CrossSection_Row = 4
    CrossSection = 5
    Color_CrossSection_Row = 5
    CrossSection_Column = 5
    Directivity_Full = 6
    Color_CrossSection_Column = 6
    GeometricMtf = 6
    Color_FluxVsWavelength = 7
    Directivity_Half = 7

class DetectorViewerShowDataTypes:
    IncoherentIrradiance = 0
    Polar_AngleSpace = 0
    IncoherentFluence = 0
    IncidentFlux = 0
    PositionSpace = 0
    IncoherentIlluminance = 0
    CoherentFluence = 1
    AngleSpace = 1
    CoherentIrradiance = 1
    AbsorbedFlux = 1
    CoherentIlluminance = 1
    AbsorbedFluxVolume = 2
    CoherentPhase = 2
    RadiantIntensity = 3
    LuminousIntensity = 3
    LuminancePositionSpace = 4
    RadiancePositionSpace = 4
    LuminanceAngleSpace = 5
    RadianceAngleSpace = 5

class ErrorType:
    Success = 0
    InvalidParameter = 1
    InvalidSettings = 2
    Failed = 3
    AnalysisUnavailableForProgramMode = 4
    NotYetImplemented = 5
    NoSolverLicenseAvailable = 10000
    ToolAlreadyOpen = 10001
    SequentialOnly = 10002
    NonSequentialOnly = 10003
    SingleNSCRayTraceSupported = 10004
    HPCNotAvailable = 10005

class GiaShowAsTypes:
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    SpotDiagram = 6
    CrossX = 7
    CrossY = 8

class GridPlotType:
    Surface = 0
    Contour = 1
    GrayScale = 2
    InverseGrayScale = 3
    FalseColor = 4
    InverseFalseColor = 5

class HuygensShowAsTypes:
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    TrueColor = 6

class HuygensSurfaceMftShowAsTypes:
    GreyScale = 0
    InverseGreyScale = 1
    FalseColor = 2
    InverseFalseColor = 3

class I_Analyses:
    @overload
    def CloseAnalysis(self, index: int) -> bool: ...
    @overload
    def CloseAnalysis(self, analysis: IA_) -> bool: ...
    def CreateColorTranslatorAuto(
        self, palette: ColorPaletteType, inversePalette: bool, numberOfShades: int
    ) -> IColorTranslator: ...
    def CreateColorTranslatorFixed(
        self, minValue: float, maxValue: float, palette: ColorPaletteType, inversePalette: bool, numberOfShades: int
    ) -> IColorTranslator: ...
    def CreateLogColorTranslatorAuto(
        self, palette: ColorPaletteType, inversePalette: bool, logBase: float, numberOfShades: int
    ) -> IColorTranslator: ...
    def CreateLogColorTranslatorFixed(
        self,
        minValue: float,
        maxValue: float,
        palette: ColorPaletteType,
        inversePalette: bool,
        logBase: float,
        numberOfShades: int,
    ) -> IColorTranslator: ...
    def Get_AnalysisAtIndex(self, index: int) -> IA_: ...
    @property
    def NumberOfAnalyses(self) -> int: ...
    def New_Analysis(self, AnalysisType: AnalysisIDM) -> IA_: ...
    def New_Analysis_SettingsFirst(self, AnalysisType: AnalysisIDM) -> IA_: ...
    def New_ConfigurationMatrixSpot(self) -> IA_: ...
    def New_ContrastLossMap(self) -> IA_: ...
    def New_CriticalRayTracer(self) -> IA_: ...
    def New_DetectorViewer(self) -> IA_: ...
    def New_DiffractionEncircledEnergy(self) -> IA_: ...
    def New_ExtendedSourceEncircledEnergy(self) -> IA_: ...
    def New_FftMtf(self) -> IA_: ...
    def New_FftMtfMap(self) -> IA_: ...
    def New_FftMtfvsField(self) -> IA_: ...
    def New_FftPsf(self) -> IA_: ...
    def New_FftPsfCrossSection(self) -> IA_: ...
    def New_FftPsfLineEdgeSpread(self) -> IA_: ...
    def New_FftSurfaceMtf(self) -> IA_: ...
    def New_FftThroughFocusMtf(self) -> IA_: ...
    def New_FieldCurvatureAndDistortion(self) -> IA_: ...
    def New_FileComparator(self) -> IA_: ...
    def New_FocalShiftDiagram(self) -> IA_: ...
    def New_Foucault(self) -> IA_: ...
    def New_FullFieldAberration(self) -> IA_: ...
    def New_FullFieldSpot(self) -> IA_: ...
    def New_GeometricEncircledEnergy(self) -> IA_: ...
    def New_GeometricImageAnalysis(self) -> IA_: ...
    def New_GeometricLineEdgeSpread(self) -> IA_: ...
    def New_GeometricMtf(self) -> IA_: ...
    def New_GeometricMtfMap(self) -> IA_: ...
    def New_GeometricMtfvsField(self) -> IA_: ...
    def New_GeometricThroughFocusMtf(self) -> IA_: ...
    def New_GridDistortion(self) -> IA_: ...
    def New_GrinProfile(self) -> IA_: ...
    def New_HuygensMtf(self) -> IA_: ...
    def New_HuygensMtfvsField(self) -> IA_: ...
    def New_HuygensPsf(self) -> IA_: ...
    def New_HuygensPsfCrossSection(self) -> IA_: ...
    def New_HuygensSurfaceMtf(self) -> IA_: ...
    def New_HuygensThroughFocusMtf(self) -> IA_: ...
    def New_ImageSimulation(self) -> IA_: ...
    def New_Interferogram(self) -> IA_: ...
    def New_InternalTransmissionvsWavelength(self) -> IA_: ...
    def New_LateralColor(self) -> IA_: ...
    def New_LongitudinalAberration(self) -> IA_: ...
    def New_MatrixSpot(self) -> IA_: ...
    def New_NSCGeometricMtf(self) -> IA_: ...
    def New_NSCSingleRayTrace(self) -> IA_: ...
    def New_NSCSurfaceSag(self) -> IA_: ...
    def New_OpticalPathFan(self) -> IA_: ...
    def New_PathAnalysis(self) -> IA_: ...
    def New_PupilAberrationFan(self) -> IA_: ...
    def New_QuickYield(self) -> IA_: ...
    def New_RayFan(self) -> IA_: ...
    def New_RayTrace(self) -> IA_: ...
    def New_RelativeIllumination(self) -> IA_: ...
    def New_RMSField(self) -> IA_: ...
    def New_RMSFieldMap(self) -> IA_: ...
    def New_RMSFocus(self) -> IA_: ...
    def New_RMSLambdaDiagram(self) -> IA_: ...
    def New_SeidelCoefficients(self) -> IA_: ...
    def New_SeidelDiagram(self) -> IA_: ...
    def New_StandardSpot(self) -> IA_: ...
    def New_SurfaceCurvature(self) -> IA_: ...
    def New_SurfaceCurvatureCross(self) -> IA_: ...
    def New_SurfacePhase(self) -> IA_: ...
    def New_SurfacePhaseCross(self) -> IA_: ...
    def New_SurfaceSag(self) -> IA_: ...
    def New_SurfaceSagCross(self) -> IA_: ...
    def New_SurfaceSlope(self) -> IA_: ...
    def New_SurfaceSlopeCross(self) -> IA_: ...
    def New_ThroughFocusSpot(self) -> IA_: ...
    def New_TolerancingHistogram(self) -> IA_: ...
    def New_TolerancingYield(self) -> IA_: ...
    def New_WavefrontMap(self) -> IA_: ...
    def New_XXXTemplateXXX(self) -> IA_: ...
    def New_ZernikeAnnularCoefficients(self) -> IA_: ...
    def New_ZernikeCoefficientsVsField(self) -> IA_: ...
    def New_ZernikeFringeCoefficients(self) -> IA_: ...
    def New_ZernikeStandardCoefficients(self) -> IA_: ...
    def RunHighSamplingPOP(
        self,
        configFile: str,
        xSampling: POPSampling,
        ySampling: POPSampling,
        outputTextFile: str,
        outputBeamFileName: str,
        saveBeamAtAllSurfaces: bool,
    ) -> IMessage: ...

class IA_:
    def Apply(self) -> IMessage: ...
    def ApplyAndWaitForCompletion(self) -> IMessage: ...
    def Close(self) -> None: ...
    @property
    def AnalysisType(self) -> AnalysisIDM: ...
    @property
    def GetAnalysisName(self) -> str: ...
    @property
    def HasAnalysisSpecificSettings(self) -> bool: ...
    @property
    def StatusMessages(self) -> IMessages: ...
    @property
    def Title(self) -> str: ...
    def GetResults(self) -> IAR_: ...
    def GetSettings(self) -> IAS_: ...
    def IsRunning(self) -> bool: ...
    def Release(self) -> None: ...
    def Terminate(self) -> bool: ...
    def ToFile(self, Filename: str, showSettings: bool, verify: bool) -> None: ...
    def WaitForCompletion(self) -> None: ...

class IColorTranslator:
    @property
    def CanConvertSingleValue(self) -> bool: ...
    @property
    def IsAutoScaled(self) -> bool: ...
    @property
    def IsInversePalette(self) -> bool: ...
    @property
    def IsLog(self) -> bool: ...
    @property
    def LogBase(self) -> float: ...
    @property
    def MaxValue(self) -> float: ...
    @property
    def MinValue(self) -> float: ...
    @property
    def NumberOfShades(self) -> int: ...
    @property
    def Palette(self) -> ColorPaletteType: ...
    def GetRGB(self, fullSize: int, data: list[float]) -> tuple[list[int], list[int], list[int]]: ...
    def GetRGB2DFloatSafe(self, vals: list[list[float]]) -> list[list[list[float]]]: ...
    def GetRGB2DSafe(self, vals: list[list[float]]) -> list[list[list[int]]]: ...
    def GetRGBFloat(self, fullSize: int, data: list[float]) -> tuple[list[float], list[float], list[float]]: ...
    def GetRGBFloatSafe(self, vals: list[float]) -> list[list[float]]: ...
    def GetRGBSafe(self, vals: list[float]) -> list[list[int]]: ...
    def GetSingleRGB(self, x: float) -> tuple[bool, int, int, int]: ...
    def GetSingleRGBFloat(self, x: float) -> tuple[bool, float, float, float]: ...

class IMessage:
    @property
    def ErrorCode(self) -> ErrorType: ...
    @property
    def Text(self) -> str: ...

class IMessages:
    def AllToString(self) -> str: ...
    @overload
    def WriteLine(self, s: str, userV: int, settingsV: int) -> None: ...
    @overload
    def WriteLine(self, s: str, userV: bool, settingsV: bool) -> None: ...
    @overload
    def WriteLine(self, s: str, userV: float, settingsV: float) -> None: ...
    @overload
    def WriteLine(self, s: str, userV: str, settingsV: str) -> None: ...

class IUser2DLineData:
    def AddSeries(
        self, seriesName: str, seriesColor: ZemaxColor, numberOfYValues: int, yValues: list[float]
    ) -> None: ...
    def AddSeriesSafe(self, seriesName: str, seriesColor: ZemaxColor, yValues: list[float]) -> None: ...
    @property
    def NumberOfSeries(self) -> int: ...
    @property
    def NumberOfXValues(self) -> int: ...
    @property
    def NumberOfYValues(self) -> int: ...
    @property
    def PlotDescription(self) -> str: ...
    @property
    def XAxisLog(self) -> bool: ...
    @property
    def XAxisMax(self) -> float: ...
    @property
    def XAxisMaxAuto(self) -> bool: ...
    @property
    def XAxisMin(self) -> float: ...
    @property
    def XAxisMinAuto(self) -> bool: ...
    @property
    def XAxisReversed(self) -> bool: ...
    @property
    def XAxisSymmetric(self) -> bool: ...
    @property
    def XLabel(self) -> str: ...
    @property
    def YAxisLog(self) -> bool: ...
    @property
    def YAxisMax(self) -> float: ...
    @property
    def YAxisMaxAuto(self) -> bool: ...
    @property
    def YAxisMin(self) -> float: ...
    @property
    def YAxisMinAuto(self) -> bool: ...
    @property
    def YAxisReversed(self) -> bool: ...
    @property
    def YAxisSymmetric(self) -> bool: ...
    @property
    def YLabel(self) -> str: ...
    @XAxisLog.setter
    def XAxisLog(self, value: bool) -> None: ...
    @XAxisMax.setter
    def XAxisMax(self, value: float) -> None: ...
    @XAxisMaxAuto.setter
    def XAxisMaxAuto(self, value: bool) -> None: ...
    @XAxisMin.setter
    def XAxisMin(self, value: float) -> None: ...
    @XAxisMinAuto.setter
    def XAxisMinAuto(self, value: bool) -> None: ...
    @XAxisReversed.setter
    def XAxisReversed(self, value: bool) -> None: ...
    @XAxisSymmetric.setter
    def XAxisSymmetric(self, value: bool) -> None: ...
    @XLabel.setter
    def XLabel(self, value: str) -> None: ...
    @YAxisLog.setter
    def YAxisLog(self, value: bool) -> None: ...
    @YAxisMax.setter
    def YAxisMax(self, value: float) -> None: ...
    @YAxisMaxAuto.setter
    def YAxisMaxAuto(self, value: bool) -> None: ...
    @YAxisMin.setter
    def YAxisMin(self, value: float) -> None: ...
    @YAxisMinAuto.setter
    def YAxisMinAuto(self, value: bool) -> None: ...
    @YAxisReversed.setter
    def YAxisReversed(self, value: bool) -> None: ...
    @YAxisSymmetric.setter
    def YAxisSymmetric(self, value: bool) -> None: ...
    @YLabel.setter
    def YLabel(self, value: str) -> None: ...

class IUserAnalysisData:
    @property
    def AnalysisNumber(self) -> int: ...
    @property
    def FeatureDescription(self) -> str: ...
    @property
    def HeaderData(self) -> list[str]: ...
    @property
    def PlotType(self) -> UserAnalysisDataType: ...
    @property
    def RunAnalysisOnSettingsClosed(self) -> bool: ...
    @property
    def ShowLegend(self) -> bool: ...
    @property
    def UserSettings(self) -> ISettingsData: ...
    @property
    def WindowTitle(self) -> str: ...
    def Make2DLinePlot(self, PlotDescription: str, numValues: int, xValues: list[float]) -> IUser2DLineData: ...
    def Make2DLinePlotSafe(self, PlotDescription: str, xValues: list[float]) -> IUser2DLineData: ...
    def MakeGridPlot(self, PlotDescription: str) -> IUserGridData: ...
    def MakeGridRGBPlot(self, PlotDescription: str) -> IUserGridRGBData: ...
    def MakeText(self) -> IUserTextData: ...
    @FeatureDescription.setter
    def FeatureDescription(self, value: str) -> None: ...
    @HeaderData.setter
    def HeaderData(self, value: list[str]) -> None: ...
    @RunAnalysisOnSettingsClosed.setter
    def RunAnalysisOnSettingsClosed(self, value: bool) -> None: ...
    @ShowLegend.setter
    def ShowLegend(self, value: bool) -> None: ...
    @WindowTitle.setter
    def WindowTitle(self, value: str) -> None: ...

class IUserGridData:
    @property
    def DataDX(self) -> float: ...
    @property
    def DataDY(self) -> float: ...
    @property
    def InterpolateLowResolutionContours(self) -> bool: ...
    @property
    def LogColorMap(self) -> bool: ...
    @property
    def NumberOfXDataValues(self) -> int: ...
    @property
    def NumberOfYDataValues(self) -> int: ...
    @property
    def PlotDescription(self) -> str: ...
    @property
    def ShowAsType(self) -> GridPlotType: ...
    @property
    def ValueLabel(self) -> str: ...
    @property
    def XAxisMax(self) -> float: ...
    @property
    def XAxisMaxAuto(self) -> bool: ...
    @property
    def XAxisMin(self) -> float: ...
    @property
    def XAxisMinAuto(self) -> bool: ...
    @property
    def XAxisSymmetric(self) -> bool: ...
    @property
    def XDataMax(self) -> float: ...
    @property
    def XDataMin(self) -> float: ...
    @property
    def XLabel(self) -> str: ...
    @property
    def XYAspectRatio(self) -> float: ...
    @property
    def YAxisMax(self) -> float: ...
    @property
    def YAxisMaxAuto(self) -> bool: ...
    @property
    def YAxisMin(self) -> float: ...
    @property
    def YAxisMinAuto(self) -> bool: ...
    @property
    def YAxisSymmetric(self) -> bool: ...
    @property
    def YDataMax(self) -> float: ...
    @property
    def YDataMin(self) -> float: ...
    @property
    def YLabel(self) -> str: ...
    @property
    def ZAxisLog(self) -> bool: ...
    @property
    def ZAxisMax(self) -> float: ...
    @property
    def ZAxisMaxAuto(self) -> bool: ...
    @property
    def ZAxisMin(self) -> float: ...
    @property
    def ZAxisMinAuto(self) -> bool: ...
    @InterpolateLowResolutionContours.setter
    def InterpolateLowResolutionContours(self, value: bool) -> None: ...
    @LogColorMap.setter
    def LogColorMap(self, value: bool) -> None: ...
    @ShowAsType.setter
    def ShowAsType(self, value: GridPlotType) -> None: ...
    @ValueLabel.setter
    def ValueLabel(self, value: str) -> None: ...
    @XAxisMax.setter
    def XAxisMax(self, value: float) -> None: ...
    @XAxisMaxAuto.setter
    def XAxisMaxAuto(self, value: bool) -> None: ...
    @XAxisMin.setter
    def XAxisMin(self, value: float) -> None: ...
    @XAxisMinAuto.setter
    def XAxisMinAuto(self, value: bool) -> None: ...
    @XAxisSymmetric.setter
    def XAxisSymmetric(self, value: bool) -> None: ...
    @XLabel.setter
    def XLabel(self, value: str) -> None: ...
    @XYAspectRatio.setter
    def XYAspectRatio(self, value: float) -> None: ...
    @YAxisMax.setter
    def YAxisMax(self, value: float) -> None: ...
    @YAxisMaxAuto.setter
    def YAxisMaxAuto(self, value: bool) -> None: ...
    @YAxisMin.setter
    def YAxisMin(self, value: float) -> None: ...
    @YAxisMinAuto.setter
    def YAxisMinAuto(self, value: bool) -> None: ...
    @YAxisSymmetric.setter
    def YAxisSymmetric(self, value: bool) -> None: ...
    @YLabel.setter
    def YLabel(self, value: str) -> None: ...
    @ZAxisLog.setter
    def ZAxisLog(self, value: bool) -> None: ...
    @ZAxisMax.setter
    def ZAxisMax(self, value: float) -> None: ...
    @ZAxisMaxAuto.setter
    def ZAxisMaxAuto(self, value: bool) -> None: ...
    @ZAxisMin.setter
    def ZAxisMin(self, value: float) -> None: ...
    @ZAxisMinAuto.setter
    def ZAxisMinAuto(self, value: bool) -> None: ...
    def SetData(self, totalSize: int, numXValues: int, numYValues: int, Data: list[float]) -> None: ...
    def SetDataSafe(self, Data: list[list[float]]) -> None: ...
    def SetXDataDimensions(self, xDataMin: float, xDataMax: float) -> None: ...
    def SetYDataDimensions(self, yDataMin: float, yDataMax: float) -> None: ...

class IUserGridRGBData:
    @property
    def DataDX(self) -> float: ...
    @property
    def DataDY(self) -> float: ...
    @property
    def NumberOfXDataValues(self) -> int: ...
    @property
    def NumberOfYDataValues(self) -> int: ...
    @property
    def PlotDescription(self) -> str: ...
    @property
    def ValueLabel(self) -> str: ...
    @property
    def XAxisMax(self) -> float: ...
    @property
    def XAxisMaxAuto(self) -> bool: ...
    @property
    def XAxisMin(self) -> float: ...
    @property
    def XAxisMinAuto(self) -> bool: ...
    @property
    def XAxisSymmetric(self) -> bool: ...
    @property
    def XDataMax(self) -> float: ...
    @property
    def XDataMin(self) -> float: ...
    @property
    def XLabel(self) -> str: ...
    @property
    def XYAspectRatio(self) -> float: ...
    @property
    def YAxisMax(self) -> float: ...
    @property
    def YAxisMaxAuto(self) -> bool: ...
    @property
    def YAxisMin(self) -> float: ...
    @property
    def YAxisMinAuto(self) -> bool: ...
    @property
    def YAxisSymmetric(self) -> bool: ...
    @property
    def YDataMax(self) -> float: ...
    @property
    def YDataMin(self) -> float: ...
    @property
    def YLabel(self) -> str: ...
    @ValueLabel.setter
    def ValueLabel(self, value: str) -> None: ...
    @XAxisMax.setter
    def XAxisMax(self, value: float) -> None: ...
    @XAxisMaxAuto.setter
    def XAxisMaxAuto(self, value: bool) -> None: ...
    @XAxisMin.setter
    def XAxisMin(self, value: float) -> None: ...
    @XAxisMinAuto.setter
    def XAxisMinAuto(self, value: bool) -> None: ...
    @XAxisSymmetric.setter
    def XAxisSymmetric(self, value: bool) -> None: ...
    @XLabel.setter
    def XLabel(self, value: str) -> None: ...
    @XYAspectRatio.setter
    def XYAspectRatio(self, value: float) -> None: ...
    @YAxisMax.setter
    def YAxisMax(self, value: float) -> None: ...
    @YAxisMaxAuto.setter
    def YAxisMaxAuto(self, value: bool) -> None: ...
    @YAxisMin.setter
    def YAxisMin(self, value: float) -> None: ...
    @YAxisMinAuto.setter
    def YAxisMinAuto(self, value: bool) -> None: ...
    @YAxisSymmetric.setter
    def YAxisSymmetric(self, value: bool) -> None: ...
    @YLabel.setter
    def YLabel(self, value: str) -> None: ...
    def SetData(self, fullSize: int, numXValues: int, numYValues: int, rgbData: list[float]) -> None: ...
    def SetDataRGB(
        self,
        fullSize: int,
        numXValues: int,
        numYValues: int,
        rData: list[float],
        gData: list[float],
        bData: list[float],
    ) -> None: ...
    def SetDataRGBSafe(self, rData: list[list[float]], gData: list[list[float]], bData: list[list[float]]) -> None: ...
    def SetDataSafe(self, rgbData: list[list[list[float]]]) -> None: ...
    def SetXDataDimensions(self, xDataMin: float, xDataMax: float) -> None: ...
    def SetYDataDimensions(self, yDataMin: float, yDataMax: float) -> None: ...

class IUserTextData:
    @property
    def Data(self) -> str: ...
    @Data.setter
    def Data(self, value: str) -> None: ...

class POPSampling:
    S_32 = 5
    S_64 = 6
    S_128 = 7
    S_256 = 8
    S_512 = 9
    S_1024 = 10
    S_1K = 10
    S_2048 = 11
    S_2K = 11
    S_4K = 12
    S_4096 = 12
    S_8192 = 13
    S_8K = 13
    S_16384 = 14
    S_16K = 14
    S_32K = 15
    S_32768 = 15
    S_65536 = 16
    S_64K = 16
    S_131072 = 17
    S_128K = 17
    S_256K = 18
    S_262144 = 18
    S_524288 = 19
    S_512K = 19
    S_1048576 = 20
    S_1M = 20
    S_2M = 21
    S_2097152 = 21
    S_4194304 = 22
    S_4M = 22
    S_8388608 = 23
    S_8M = 23
    S_16M = 24
    S_16777216 = 24
    S_33554432 = 25
    S_32M = 25
    S_67108864 = 26
    S_64M = 26
    S_128M = 27
    S_134217728 = 27
    S_268435456 = 28
    S_256M = 28
    S_536870912 = 29
    S_512M = 29
    S_1073741824 = 30
    S_1G = 30

class RemoveOptions:
    # None = 0
    BaseROC = 1
    BestFitSphere = 2
    BaseSag = 3

class SampleSizes:
    S_32x32 = 1
    S_64x64 = 2
    S_128x128 = 3
    S_256x256 = 4
    S_512x512 = 5
    S_1024x1024 = 6
    S_2048x2048 = 7
    S_4096x4096 = 8
    S_8192x8192 = 9
    S_16384x16384 = 10

class SampleSizes_ContrastLoss:
    S_3x3 = 1
    S_5x5 = 2
    S_7x7 = 3
    S_9x9 = 4
    S_11x11 = 5
    S_13x13 = 6
    S_15x15 = 7
    S_17x17 = 8
    S_19x19 = 9
    S_21x21 = 10
    S_23x23 = 11
    S_25x25 = 12
    S_27x27 = 13
    S_29x29 = 14
    S_31x31 = 15
    S_33x33 = 16
    S_35x35 = 17
    S_37x37 = 18
    S_39x39 = 19
    S_41x41 = 20
    S_43x43 = 21
    S_45x45 = 22
    S_47x47 = 23
    S_49x49 = 24
    S_51x51 = 25
    S_53x53 = 26
    S_55x55 = 27
    S_57x57 = 28
    S_59x59 = 29
    S_61x61 = 30
    S_63x63 = 31
    S_65x65 = 32
    S_67x67 = 33
    S_69x69 = 34
    S_71x71 = 35
    S_73x73 = 36
    S_75x75 = 37
    S_77x77 = 38
    S_79x79 = 39
    S_81x81 = 40
    S_83x83 = 41

class SampleSizes_Pow2Plus1:
    S_33 = 1
    S_65 = 2
    S_129 = 3
    S_257 = 4
    S_513 = 5
    S_1025 = 6
    S_2049 = 7
    S_4097 = 8
    S_8193 = 9

class SampleSizes_Pow2Plus1_X:
    S_33x33 = 1
    S_65x65 = 2
    S_129x129 = 3
    S_257x257 = 4
    S_513x513 = 5
    S_1025x1025 = 6
    S_2049x2049 = 7
    S_4097x4097 = 8
    S_8193x8193 = 9

class ShowAs:
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5

class SurfaceCurvatureCrossData:
    TangentialCurvature = 0
    SagitalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3
    TanPlusSagCurvature = 4
    XPlusYCurvature = 5

class SurfaceCurvatureData:
    TangentialCurvature = 0
    SagitalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3

class SurfacePhaseData:
    SurfacePhase = 0

class SurfaceSagData:
    SurfaceSag = 0

class SurfaceSlopeCrossData:
    TangentialCurvature = 0
    SagitalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3
    TanPlusSagCurvature = 4
    XPlusYCurvature = 5

class SurfaceSlopeData:
    SurfaceSlope = 0
    TangentialSlope = 0
    SagittalSlope = 1
    XSlope = 2
    YSlope = 3

class UserAnalysisDataType:
    # None = 0
    Line2D = 1
    Grid = 2
    GridRGB = 3
    Text = 4
