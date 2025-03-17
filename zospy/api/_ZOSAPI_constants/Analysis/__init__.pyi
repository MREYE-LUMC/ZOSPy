"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations
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
    "SurfacePhaseSlopeCrossData",
    "SurfacePhaseSlopeData",
    "SurfaceSagData",
    "SurfaceSlopeCrossData",
    "SurfaceSlopeData",
    "UserAnalysisDataType",
)

class AnalysisIDM:
    RayFan: AnalysisIDM = None
    OpticalPathFan: AnalysisIDM = None
    PupilAberrationFan: AnalysisIDM = None
    FieldCurvatureAndDistortion: AnalysisIDM = None
    FocalShiftDiagram: AnalysisIDM = None
    GridDistortion: AnalysisIDM = None
    LateralColor: AnalysisIDM = None
    LongitudinalAberration: AnalysisIDM = None
    RayTrace: AnalysisIDM = None
    SeidelCoefficients: AnalysisIDM = None
    SeidelDiagram: AnalysisIDM = None
    ZernikeAnnularCoefficients: AnalysisIDM = None
    ZernikeCoefficientsVsField: AnalysisIDM = None
    ZernikeFringeCoefficients: AnalysisIDM = None
    ZernikeStandardCoefficients: AnalysisIDM = None
    FftMtf: AnalysisIDM = None
    FftThroughFocusMtf: AnalysisIDM = None
    GeometricThroughFocusMtf: AnalysisIDM = None
    GeometricMtf: AnalysisIDM = None
    FftMtfMap: AnalysisIDM = None
    GeometricMtfMap: AnalysisIDM = None
    FftSurfaceMtf: AnalysisIDM = None
    FftMtfvsField: AnalysisIDM = None
    GeometricMtfvsField: AnalysisIDM = None
    HuygensMtfvsField: AnalysisIDM = None
    HuygensMtf: AnalysisIDM = None
    HuygensSurfaceMtf: AnalysisIDM = None
    HuygensThroughFocusMtf: AnalysisIDM = None
    FftPsf: AnalysisIDM = None
    FftPsfCrossSection: AnalysisIDM = None
    FftPsfLineEdgeSpread: AnalysisIDM = None
    HuygensPsfCrossSection: AnalysisIDM = None
    HuygensPsf: AnalysisIDM = None
    DiffractionEncircledEnergy: AnalysisIDM = None
    GeometricEncircledEnergy: AnalysisIDM = None
    GeometricLineEdgeSpread: AnalysisIDM = None
    ExtendedSourceEncircledEnergy: AnalysisIDM = None
    SurfaceCurvatureCross: AnalysisIDM = None
    SurfacePhaseCross: AnalysisIDM = None
    SurfaceSagCross: AnalysisIDM = None
    SurfaceCurvature: AnalysisIDM = None
    SurfacePhase: AnalysisIDM = None
    SurfaceSag: AnalysisIDM = None
    StandardSpot: AnalysisIDM = None
    ThroughFocusSpot: AnalysisIDM = None
    FullFieldSpot: AnalysisIDM = None
    MatrixSpot: AnalysisIDM = None
    ConfigurationMatrixSpot: AnalysisIDM = None
    RMSField: AnalysisIDM = None
    RMSFieldMap: AnalysisIDM = None
    RMSLambdaDiagram: AnalysisIDM = None
    RMSFocus: AnalysisIDM = None
    Foucault: AnalysisIDM = None
    Interferogram: AnalysisIDM = None
    WavefrontMap: AnalysisIDM = None
    DetectorViewer: AnalysisIDM = None
    Draw2D: AnalysisIDM = None
    Draw3D: AnalysisIDM = None
    ImageSimulation: AnalysisIDM = None
    GeometricImageAnalysis: AnalysisIDM = None
    IMABIMFileViewer: AnalysisIDM = None
    GeometricBitmapImageAnalysis: AnalysisIDM = None
    BitmapFileViewer: AnalysisIDM = None
    LightSourceAnalysis: AnalysisIDM = None
    PartiallyCoherentImageAnalysis: AnalysisIDM = None
    ExtendedDiffractionImageAnalysis: AnalysisIDM = None
    BiocularFieldOfViewAnalysis: AnalysisIDM = None
    BiocularDipvergenceConvergence: AnalysisIDM = None
    RelativeIllumination: AnalysisIDM = None
    VignettingDiagramSettings: AnalysisIDM = None
    FootprintSettings: AnalysisIDM = None
    YYbarDiagram: AnalysisIDM = None
    PowerFieldMapSettings: AnalysisIDM = None
    PowerPupilMapSettings: AnalysisIDM = None
    IncidentAnglevsImageHeight: AnalysisIDM = None
    FiberCouplingSettings: AnalysisIDM = None
    YNIContributions: AnalysisIDM = None
    SagTable: AnalysisIDM = None
    CardinalPoints: AnalysisIDM = None
    DispersionDiagram: AnalysisIDM = None
    GlassMap: AnalysisIDM = None
    AthermalGlassMap: AnalysisIDM = None
    InternalTransmissionvsWavelength: AnalysisIDM = None
    DispersionvsWavelength: AnalysisIDM = None
    GrinProfile: AnalysisIDM = None
    GradiumProfile: AnalysisIDM = None
    UniversalPlot1D: AnalysisIDM = None
    UniversalPlot2D: AnalysisIDM = None
    PolarizationRayTrace: AnalysisIDM = None
    PolarizationPupilMap: AnalysisIDM = None
    Transmission: AnalysisIDM = None
    PhaseAberration: AnalysisIDM = None
    TransmissionFan: AnalysisIDM = None
    ParaxialGaussianBeam: AnalysisIDM = None
    SkewGaussianBeam: AnalysisIDM = None
    PhysicalOpticsPropagation: AnalysisIDM = None
    BeamFileViewer: AnalysisIDM = None
    ReflectionvsAngle: AnalysisIDM = None
    TransmissionvsAngle: AnalysisIDM = None
    AbsorptionvsAngle: AnalysisIDM = None
    DiattenuationvsAngle: AnalysisIDM = None
    PhasevsAngle: AnalysisIDM = None
    RetardancevsAngle: AnalysisIDM = None
    ReflectionvsWavelength: AnalysisIDM = None
    TransmissionvsWavelength: AnalysisIDM = None
    AbsorptionvsWavelength: AnalysisIDM = None
    DiattenuationvsWavelength: AnalysisIDM = None
    PhasevsWavelength: AnalysisIDM = None
    RetardancevsWavelength: AnalysisIDM = None
    DirectivityPlot: AnalysisIDM = None
    SourcePolarViewer: AnalysisIDM = None
    PhotoluminscenceViewer: AnalysisIDM = None
    SourceSpectrumViewer: AnalysisIDM = None
    RadiantSourceModelViewerSettings: AnalysisIDM = None
    SurfaceDataSettings: AnalysisIDM = None
    PrescriptionDataSettings: AnalysisIDM = None
    FileComparatorSettings: AnalysisIDM = None
    PartViewer: AnalysisIDM = None
    ReverseRadianceAnalysis: AnalysisIDM = None
    PathAnalysis: AnalysisIDM = None
    FluxvsWavelength: AnalysisIDM = None
    RoadwayLighting: AnalysisIDM = None
    SourceIlluminationMap: AnalysisIDM = None
    ScatterFunctionViewer: AnalysisIDM = None
    ScatterPolarPlotSettings: AnalysisIDM = None
    ZemaxElementDrawing: AnalysisIDM = None
    ShadedModel: AnalysisIDM = None
    NSCShadedModel: AnalysisIDM = None
    NSC3DLayout: AnalysisIDM = None
    NSCObjectViewer: AnalysisIDM = None
    RayDatabaseViewer: AnalysisIDM = None
    ISOElementDrawing: AnalysisIDM = None
    SystemData: AnalysisIDM = None
    TestPlateList: AnalysisIDM = None
    SourceColorChart1931: AnalysisIDM = None
    SourceColorChart1976: AnalysisIDM = None
    PrescriptionGraphic: AnalysisIDM = None
    CriticalRayTracer: AnalysisIDM = None
    ContrastLoss: AnalysisIDM = None
    CoatingListing: AnalysisIDM = None
    FullFieldAberration: AnalysisIDM = None
    SurfaceSlope: AnalysisIDM = None
    SurfaceSlopeCross: AnalysisIDM = None
    QuickYield: AnalysisIDM = None
    SystemCheck: AnalysisIDM = None
    ToleranceYield: AnalysisIDM = None
    ToleranceHistogram: AnalysisIDM = None
    DiffEfficiency2D: AnalysisIDM = None
    DiffEfficiencyAngular: AnalysisIDM = None
    DiffEfficiencyChromatic: AnalysisIDM = None
    NSCSurfaceSag: AnalysisIDM = None
    NSCSingleRayTrace: AnalysisIDM = None
    NSCGeometricMtf: AnalysisIDM = None
    SurfacePhaseSlope: AnalysisIDM = None
    SurfacePhaseSlopeCross: AnalysisIDM = None
    STARAlignCheck: AnalysisIDM = None
    STARSysViewer: AnalysisIDM = None
    STAR2DDefPlot: AnalysisIDM = None
    STARPerfChange: AnalysisIDM = None
    STARIndexVsTemp: AnalysisIDM = None
    STARInspectFEA: AnalysisIDM = None
    UserDefinedCOM: AnalysisIDM = None
    XXXTemplateXXX: AnalysisIDM = None

class Beam:
    Reference: Beam = None
    Configuration_1: Beam = None
    Configuration_2: Beam = None
    Configuration_3: Beam = None
    Configuration_4: Beam = None
    Configuration_5: Beam = None
    Configuration_6: Beam = None
    Configuration_7: Beam = None
    Configuration_8: Beam = None
    Configuration_9: Beam = None
    Configuration_10: Beam = None
    Configuration_11: Beam = None
    Configuration_12: Beam = None
    Configuration_13: Beam = None
    Configuration_14: Beam = None
    Configuration_15: Beam = None
    Configuration_16: Beam = None
    Configuration_17: Beam = None
    Configuration_18: Beam = None
    Configuration_19: Beam = None
    Configuration_20: Beam = None

class BestFitSphereOptions:
    MinimumVolume: BestFitSphereOptions = None
    MinimumRMS: BestFitSphereOptions = None
    MinimumRMSWithOffset: BestFitSphereOptions = None

class ColorPaletteType:
    GreyScale: ColorPaletteType = None
    FalseColor: ColorPaletteType = None
    FalseColorOriginal: ColorPaletteType = None
    Viridis: ColorPaletteType = None
    Magma: ColorPaletteType = None

class DetectorViewerShowAsTypes:
    GreyScale: DetectorViewerShowAsTypes = None
    FullListing: DetectorViewerShowAsTypes = None
    Text_CrossSection_Row: DetectorViewerShowAsTypes = None
    AzimuthCrossSection: DetectorViewerShowAsTypes = None
    GreyScale_Inverted: DetectorViewerShowAsTypes = None
    Text_CrossSection_Column: DetectorViewerShowAsTypes = None
    FalseColor: DetectorViewerShowAsTypes = None
    FluxVsWaveLength: DetectorViewerShowAsTypes = None
    FalseColor_Inverted: DetectorViewerShowAsTypes = None
    TrueColor: DetectorViewerShowAsTypes = None
    CrossSection_Row: DetectorViewerShowAsTypes = None
    CrossSection: DetectorViewerShowAsTypes = None
    Color_CrossSection_Row: DetectorViewerShowAsTypes = None
    CrossSection_Column: DetectorViewerShowAsTypes = None
    Directivity_Full: DetectorViewerShowAsTypes = None
    Color_CrossSection_Column: DetectorViewerShowAsTypes = None
    GeometricMtf: DetectorViewerShowAsTypes = None
    Color_FluxVsWavelength: DetectorViewerShowAsTypes = None
    Directivity_Half: DetectorViewerShowAsTypes = None

class DetectorViewerShowDataTypes:
    IncoherentIrradiance: DetectorViewerShowDataTypes = None
    Polar_AngleSpace: DetectorViewerShowDataTypes = None
    IncoherentFluence: DetectorViewerShowDataTypes = None
    IncidentFlux: DetectorViewerShowDataTypes = None
    PositionSpace: DetectorViewerShowDataTypes = None
    IncoherentIlluminance: DetectorViewerShowDataTypes = None
    CoherentFluence: DetectorViewerShowDataTypes = None
    AngleSpace: DetectorViewerShowDataTypes = None
    CoherentIrradiance: DetectorViewerShowDataTypes = None
    AbsorbedFlux: DetectorViewerShowDataTypes = None
    CoherentIlluminance: DetectorViewerShowDataTypes = None
    AbsorbedFluxVolume: DetectorViewerShowDataTypes = None
    CoherentPhase: DetectorViewerShowDataTypes = None
    RadiantIntensity: DetectorViewerShowDataTypes = None
    LuminousIntensity: DetectorViewerShowDataTypes = None
    LuminancePositionSpace: DetectorViewerShowDataTypes = None
    RadiancePositionSpace: DetectorViewerShowDataTypes = None
    LuminanceAngleSpace: DetectorViewerShowDataTypes = None
    RadianceAngleSpace: DetectorViewerShowDataTypes = None

class ErrorType:
    Success: ErrorType = None
    InvalidParameter: ErrorType = None
    InvalidSettings: ErrorType = None
    Failed: ErrorType = None
    AnalysisUnavailableForProgramMode: ErrorType = None
    NotYetImplemented: ErrorType = None
    NoSolverLicenseAvailable: ErrorType = None
    ToolAlreadyOpen: ErrorType = None
    SequentialOnly: ErrorType = None
    NonSequentialOnly: ErrorType = None
    SingleNSCRayTraceSupported: ErrorType = None
    HPCNotAvailable: ErrorType = None
    FeatureNotSupported: ErrorType = None
    NotAvailableInLegacy: ErrorType = None

class GiaShowAsTypes:
    Surface: GiaShowAsTypes = None
    Contour: GiaShowAsTypes = None
    GreyScale: GiaShowAsTypes = None
    InverseGreyScale: GiaShowAsTypes = None
    FalseColor: GiaShowAsTypes = None
    InverseFalseColor: GiaShowAsTypes = None
    SpotDiagram: GiaShowAsTypes = None
    CrossX: GiaShowAsTypes = None
    CrossY: GiaShowAsTypes = None

class GridPlotType:
    Surface: GridPlotType = None
    Contour: GridPlotType = None
    GrayScale: GridPlotType = None
    InverseGrayScale: GridPlotType = None
    FalseColor: GridPlotType = None
    InverseFalseColor: GridPlotType = None

class HuygensShowAsTypes:
    Surface: HuygensShowAsTypes = None
    Contour: HuygensShowAsTypes = None
    GreyScale: HuygensShowAsTypes = None
    InverseGreyScale: HuygensShowAsTypes = None
    FalseColor: HuygensShowAsTypes = None
    InverseFalseColor: HuygensShowAsTypes = None
    TrueColor: HuygensShowAsTypes = None

class HuygensSurfaceMftShowAsTypes:
    GreyScale: HuygensSurfaceMftShowAsTypes = None
    InverseGreyScale: HuygensSurfaceMftShowAsTypes = None
    FalseColor: HuygensSurfaceMftShowAsTypes = None
    InverseFalseColor: HuygensSurfaceMftShowAsTypes = None

class POPSampling:
    S_32: POPSampling = None
    S_64: POPSampling = None
    S_128: POPSampling = None
    S_256: POPSampling = None
    S_512: POPSampling = None
    S_1024: POPSampling = None
    S_1K: POPSampling = None
    S_2048: POPSampling = None
    S_2K: POPSampling = None
    S_4K: POPSampling = None
    S_4096: POPSampling = None
    S_8192: POPSampling = None
    S_8K: POPSampling = None
    S_16384: POPSampling = None
    S_16K: POPSampling = None
    S_32K: POPSampling = None
    S_32768: POPSampling = None
    S_65536: POPSampling = None
    S_64K: POPSampling = None
    S_131072: POPSampling = None
    S_128K: POPSampling = None
    S_256K: POPSampling = None
    S_262144: POPSampling = None
    S_524288: POPSampling = None
    S_512K: POPSampling = None
    S_1048576: POPSampling = None
    S_1M: POPSampling = None
    S_2M: POPSampling = None
    S_2097152: POPSampling = None
    S_4194304: POPSampling = None
    S_4M: POPSampling = None
    S_8388608: POPSampling = None
    S_8M: POPSampling = None
    S_16M: POPSampling = None
    S_16777216: POPSampling = None
    S_33554432: POPSampling = None
    S_32M: POPSampling = None
    S_67108864: POPSampling = None
    S_64M: POPSampling = None
    S_128M: POPSampling = None
    S_134217728: POPSampling = None
    S_268435456: POPSampling = None
    S_256M: POPSampling = None
    S_536870912: POPSampling = None
    S_512M: POPSampling = None
    S_1073741824: POPSampling = None
    S_1G: POPSampling = None

class RemoveOptions:
    None_: RemoveOptions = None
    BaseROC: RemoveOptions = None
    BestFitSphere: RemoveOptions = None
    BaseSag: RemoveOptions = None
    CompositeSag: RemoveOptions = None

class SampleSizes:
    S_32x32: SampleSizes = None
    S_64x64: SampleSizes = None
    S_128x128: SampleSizes = None
    S_256x256: SampleSizes = None
    S_512x512: SampleSizes = None
    S_1024x1024: SampleSizes = None
    S_2048x2048: SampleSizes = None
    S_4096x4096: SampleSizes = None
    S_8192x8192: SampleSizes = None
    S_16384x16384: SampleSizes = None

class SampleSizes_ContrastLoss:
    S_3x3: SampleSizes_ContrastLoss = None
    S_5x5: SampleSizes_ContrastLoss = None
    S_7x7: SampleSizes_ContrastLoss = None
    S_9x9: SampleSizes_ContrastLoss = None
    S_11x11: SampleSizes_ContrastLoss = None
    S_13x13: SampleSizes_ContrastLoss = None
    S_15x15: SampleSizes_ContrastLoss = None
    S_17x17: SampleSizes_ContrastLoss = None
    S_19x19: SampleSizes_ContrastLoss = None
    S_21x21: SampleSizes_ContrastLoss = None
    S_23x23: SampleSizes_ContrastLoss = None
    S_25x25: SampleSizes_ContrastLoss = None
    S_27x27: SampleSizes_ContrastLoss = None
    S_29x29: SampleSizes_ContrastLoss = None
    S_31x31: SampleSizes_ContrastLoss = None
    S_33x33: SampleSizes_ContrastLoss = None
    S_35x35: SampleSizes_ContrastLoss = None
    S_37x37: SampleSizes_ContrastLoss = None
    S_39x39: SampleSizes_ContrastLoss = None
    S_41x41: SampleSizes_ContrastLoss = None
    S_43x43: SampleSizes_ContrastLoss = None
    S_45x45: SampleSizes_ContrastLoss = None
    S_47x47: SampleSizes_ContrastLoss = None
    S_49x49: SampleSizes_ContrastLoss = None
    S_51x51: SampleSizes_ContrastLoss = None
    S_53x53: SampleSizes_ContrastLoss = None
    S_55x55: SampleSizes_ContrastLoss = None
    S_57x57: SampleSizes_ContrastLoss = None
    S_59x59: SampleSizes_ContrastLoss = None
    S_61x61: SampleSizes_ContrastLoss = None
    S_63x63: SampleSizes_ContrastLoss = None
    S_65x65: SampleSizes_ContrastLoss = None
    S_67x67: SampleSizes_ContrastLoss = None
    S_69x69: SampleSizes_ContrastLoss = None
    S_71x71: SampleSizes_ContrastLoss = None
    S_73x73: SampleSizes_ContrastLoss = None
    S_75x75: SampleSizes_ContrastLoss = None
    S_77x77: SampleSizes_ContrastLoss = None
    S_79x79: SampleSizes_ContrastLoss = None
    S_81x81: SampleSizes_ContrastLoss = None
    S_83x83: SampleSizes_ContrastLoss = None

class SampleSizes_Pow2Plus1:
    S_33: SampleSizes_Pow2Plus1 = None
    S_65: SampleSizes_Pow2Plus1 = None
    S_129: SampleSizes_Pow2Plus1 = None
    S_257: SampleSizes_Pow2Plus1 = None
    S_513: SampleSizes_Pow2Plus1 = None
    S_1025: SampleSizes_Pow2Plus1 = None
    S_2049: SampleSizes_Pow2Plus1 = None
    S_4097: SampleSizes_Pow2Plus1 = None
    S_8193: SampleSizes_Pow2Plus1 = None

class SampleSizes_Pow2Plus1_X:
    S_33x33: SampleSizes_Pow2Plus1_X = None
    S_65x65: SampleSizes_Pow2Plus1_X = None
    S_129x129: SampleSizes_Pow2Plus1_X = None
    S_257x257: SampleSizes_Pow2Plus1_X = None
    S_513x513: SampleSizes_Pow2Plus1_X = None
    S_1025x1025: SampleSizes_Pow2Plus1_X = None
    S_2049x2049: SampleSizes_Pow2Plus1_X = None
    S_4097x4097: SampleSizes_Pow2Plus1_X = None
    S_8193x8193: SampleSizes_Pow2Plus1_X = None

class ShowAs:
    Surface: ShowAs = None
    Contour: ShowAs = None
    GreyScale: ShowAs = None
    InverseGreyScale: ShowAs = None
    FalseColor: ShowAs = None
    InverseFalseColor: ShowAs = None

class SurfaceCurvatureCrossData:
    TangentialCurvature: SurfaceCurvatureCrossData = None
    SagittalCurvature: SurfaceCurvatureCrossData = None
    X_Curvature: SurfaceCurvatureCrossData = None
    Y_Curvature: SurfaceCurvatureCrossData = None
    CurvatureModulus: SurfaceCurvatureCrossData = None
    CurvatureUnused: SurfaceCurvatureCrossData = None

class SurfaceCurvatureData:
    TangentialCurvature: SurfaceCurvatureData = None
    SagittalCurvature: SurfaceCurvatureData = None
    X_Curvature: SurfaceCurvatureData = None
    Y_Curvature: SurfaceCurvatureData = None
    CurvatureModulus: SurfaceCurvatureData = None
    CurvatureUnused: SurfaceCurvatureData = None

class SurfacePhaseData:
    SurfacePhase: SurfacePhaseData = None

class SurfacePhaseSlopeCrossData:
    PhaseSlopeTangential: SurfacePhaseSlopeCrossData = None
    PhaseSlopeSagittal: SurfacePhaseSlopeCrossData = None
    PhaseSlopeX: SurfacePhaseSlopeCrossData = None
    PhaseSlopeY: SurfacePhaseSlopeCrossData = None
    PhaseSlopeModulus: SurfacePhaseSlopeCrossData = None
    PhaseSlopeUnused: SurfacePhaseSlopeCrossData = None

class SurfacePhaseSlopeData:
    PhaseSlopeTangential: SurfacePhaseSlopeData = None
    PhaseSlopeSagittal: SurfacePhaseSlopeData = None
    PhaseSlopeX: SurfacePhaseSlopeData = None
    PhaseSlopeY: SurfacePhaseSlopeData = None
    PhaseSlopeModulus: SurfacePhaseSlopeData = None
    PhaseSlopeUnused: SurfacePhaseSlopeData = None

class SurfaceSagData:
    SurfaceSag: SurfaceSagData = None

class SurfaceSlopeCrossData:
    TangentialSlope: SurfaceSlopeCrossData = None
    SagittalSlope: SurfaceSlopeCrossData = None
    XSlope: SurfaceSlopeCrossData = None
    YSlope: SurfaceSlopeCrossData = None
    SlopeModulus: SurfaceSlopeCrossData = None
    SlopeUnused: SurfaceSlopeCrossData = None

class SurfaceSlopeData:
    SurfaceSlope: SurfaceSlopeData = None
    TangentialSlope: SurfaceSlopeData = None
    SagittalSlope: SurfaceSlopeData = None
    XSlope: SurfaceSlopeData = None
    YSlope: SurfaceSlopeData = None
    SlopeModulus: SurfaceSlopeData = None
    SlopeUnused: SurfaceSlopeData = None

class UserAnalysisDataType:
    None_: UserAnalysisDataType = None
    Line2D: UserAnalysisDataType = None
    Grid: UserAnalysisDataType = None
    GridRGB: UserAnalysisDataType = None
    Text: UserAnalysisDataType = None
