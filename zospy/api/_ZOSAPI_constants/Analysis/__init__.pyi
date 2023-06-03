"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

from . import PhysicalOptics, RayTracing, Settings, Tolerancing

__all__ = (
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

class AnalysisIDM(Enum):
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

class Beam(Enum):
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

class BestFitSphereOptions(Enum):
    MinimumVolume = 0
    MinimumRMS = 1
    MinimumRMSWithOffset = 2

class ColorPaletteType(Enum):
    GreyScale = 0
    FalseColor = 1
    FalseColorOriginal = 2
    Viridis = 3
    Magma = 4

class DetectorViewerShowAsTypes(Enum):
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

class DetectorViewerShowDataTypes(Enum):
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

class ErrorType(Enum):
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

class GiaShowAsTypes(Enum):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    SpotDiagram = 6
    CrossX = 7
    CrossY = 8

class GridPlotType(Enum):
    Surface = 0
    Contour = 1
    GrayScale = 2
    InverseGrayScale = 3
    FalseColor = 4
    InverseFalseColor = 5

class HuygensShowAsTypes(Enum):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    TrueColor = 6

class HuygensSurfaceMftShowAsTypes(Enum):
    GreyScale = 0
    InverseGreyScale = 1
    FalseColor = 2
    InverseFalseColor = 3

class POPSampling(Enum):
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

class RemoveOptions(Enum):
    None_ = 0
    BaseROC = 1
    BestFitSphere = 2
    BaseSag = 3

class SampleSizes(Enum):
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

class SampleSizes_ContrastLoss(Enum):
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

class SampleSizes_Pow2Plus1(Enum):
    S_33 = 1
    S_65 = 2
    S_129 = 3
    S_257 = 4
    S_513 = 5
    S_1025 = 6
    S_2049 = 7
    S_4097 = 8
    S_8193 = 9

class SampleSizes_Pow2Plus1_X(Enum):
    S_33x33 = 1
    S_65x65 = 2
    S_129x129 = 3
    S_257x257 = 4
    S_513x513 = 5
    S_1025x1025 = 6
    S_2049x2049 = 7
    S_4097x4097 = 8
    S_8193x8193 = 9

class ShowAs(Enum):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5

class SurfaceCurvatureCrossData(Enum):
    TangentialCurvature = 0
    SagitalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3
    TanPlusSagCurvature = 4
    XPlusYCurvature = 5

class SurfaceCurvatureData(Enum):
    TangentialCurvature = 0
    SagitalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3

class SurfacePhaseData(Enum):
    SurfacePhase = 0

class SurfaceSagData(Enum):
    SurfaceSag = 0

class SurfaceSlopeCrossData(Enum):
    TangentialCurvature = 0
    SagitalCurvature = 1
    X_Curvature = 2
    Y_Curvature = 3
    TanPlusSagCurvature = 4
    XPlusYCurvature = 5

class SurfaceSlopeData(Enum):
    SurfaceSlope = 0
    TangentialSlope = 0
    SagittalSlope = 1
    XSlope = 2
    YSlope = 3

class UserAnalysisDataType(Enum):
    None_ = 0
    Line2D = 1
    Grid = 2
    GridRGB = 3
    Text = 4
