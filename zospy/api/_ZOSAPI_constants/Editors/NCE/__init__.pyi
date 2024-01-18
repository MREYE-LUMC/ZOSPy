"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = (
    "ApertureShapes",
    "ArrayMode",
    "BirefringentMode",
    "BirefringentReflections",
    "DetectorDataType",
    "DetectorShowAsType",
    "DiffractionSplitType",
    "DiffractiveFaceChoices",
    "DrawingResolutionType",
    "EfficiencySpectrumType",
    "EndCapOptions",
    "FaceIsType",
    "HologramTypes",
    "InterpolateChoices",
    "NCEIndexType",
    "ObjectColumn",
    "ObjectScatteringTypes",
    "ObjectType",
    "OrderChoices",
    "PixelAddressing",
    "PolarDetectorDataType",
    "RaysIgnoreObjectType",
    "RayTraceModes",
    "ScatterToType",
    "ShapeChoices",
    "SourceBulkScatterMode",
    "SourceColorMode",
    "SourceSamplingMethod",
    "UniformAngleChoices",
    "VolumePhysicsModelType",
)

class ApertureShapes:
    Annular: ApertureShapes = None
    Elliptical: ApertureShapes = None
    Rectangular: ApertureShapes = None
    CyliderWithRectangular: ApertureShapes = None

class ArrayMode:
    None_: ArrayMode = None
    Rectangular: ArrayMode = None
    Circular: ArrayMode = None
    Hexapolar: ArrayMode = None
    Hexagonal: ArrayMode = None

class BirefringentMode:
    TraceOrdinayAndExtraordinary: BirefringentMode = None
    TraceOrdinaryOnly: BirefringentMode = None
    TraceExtraordinaryOnly: BirefringentMode = None
    Waveplate: BirefringentMode = None

class BirefringentReflections:
    TraceReflectedAndRefracted: BirefringentReflections = None
    TraceRefractedOnly: BirefringentReflections = None
    TraceReflectedOnly: BirefringentReflections = None

class DetectorDataType:
    Real: DetectorDataType = None
    Imaginary: DetectorDataType = None
    Amplitude: DetectorDataType = None
    Power: DetectorDataType = None

class DetectorShowAsType:
    GreyScaleFlux: DetectorShowAsType = None
    InverseGreyScaleFlux: DetectorShowAsType = None
    FalseColorFlux: DetectorShowAsType = None
    InverseFalseColorFlux: DetectorShowAsType = None
    GreyScaleIrradiance: DetectorShowAsType = None
    InverseGreyScaleIrradiance: DetectorShowAsType = None
    FalseColorIrradiance: DetectorShowAsType = None
    InverseFalseColorIrradiance: DetectorShowAsType = None

class DiffractionSplitType:
    DontSplitByOrder: DiffractionSplitType = None
    SplitByTable: DiffractionSplitType = None
    SplitByDLL: DiffractionSplitType = None

class DiffractiveFaceChoices:
    FrontFace: DiffractiveFaceChoices = None
    BackFace: DiffractiveFaceChoices = None

class DrawingResolutionType:
    Standard: DrawingResolutionType = None
    Medium: DrawingResolutionType = None
    High: DrawingResolutionType = None
    Presentation: DrawingResolutionType = None
    Custom: DrawingResolutionType = None

class EfficiencySpectrumType:
    QuantumYield: EfficiencySpectrumType = None
    Excitation: EfficiencySpectrumType = None

class EndCapOptions:
    None_: EndCapOptions = None
    First: EndCapOptions = None
    Second: EndCapOptions = None
    Both: EndCapOptions = None

class FaceIsType:
    ObjectDefault: FaceIsType = None
    Reflective: FaceIsType = None
    Absorbing: FaceIsType = None

class HologramTypes:
    Type_1: HologramTypes = None
    Type_2: HologramTypes = None

class InterpolateChoices:
    Bicubic: InterpolateChoices = None
    Linear: InterpolateChoices = None

class NCEIndexType:
    Isotropic: NCEIndexType = None
    Birefringent: NCEIndexType = None
    GRIN: NCEIndexType = None

class ObjectColumn:
    Comment: ObjectColumn = None
    RefObject: ObjectColumn = None
    InsideOf: ObjectColumn = None
    XPosition: ObjectColumn = None
    YPosition: ObjectColumn = None
    ZPosition: ObjectColumn = None
    TiltX: ObjectColumn = None
    TiltY: ObjectColumn = None
    TiltZ: ObjectColumn = None
    Material: ObjectColumn = None
    Par1: ObjectColumn = None
    Par2: ObjectColumn = None
    Par3: ObjectColumn = None
    Par4: ObjectColumn = None
    Par5: ObjectColumn = None
    Par6: ObjectColumn = None
    Par7: ObjectColumn = None
    Par8: ObjectColumn = None
    Par9: ObjectColumn = None
    Par10: ObjectColumn = None
    Par11: ObjectColumn = None
    Par12: ObjectColumn = None
    Par13: ObjectColumn = None
    Par14: ObjectColumn = None
    Par15: ObjectColumn = None
    Par16: ObjectColumn = None
    Par17: ObjectColumn = None
    Par18: ObjectColumn = None
    Par19: ObjectColumn = None
    Par20: ObjectColumn = None
    Par21: ObjectColumn = None
    Par22: ObjectColumn = None
    Par23: ObjectColumn = None
    Par24: ObjectColumn = None
    Par25: ObjectColumn = None
    Par26: ObjectColumn = None
    Par27: ObjectColumn = None
    Par28: ObjectColumn = None
    Par29: ObjectColumn = None
    Par30: ObjectColumn = None
    Par31: ObjectColumn = None
    Par32: ObjectColumn = None
    Par33: ObjectColumn = None
    Par34: ObjectColumn = None
    Par35: ObjectColumn = None
    Par36: ObjectColumn = None
    Par37: ObjectColumn = None
    Par38: ObjectColumn = None
    Par39: ObjectColumn = None
    Par40: ObjectColumn = None
    Par41: ObjectColumn = None
    Par42: ObjectColumn = None
    Par43: ObjectColumn = None
    Par44: ObjectColumn = None
    Par45: ObjectColumn = None
    Par46: ObjectColumn = None
    Par47: ObjectColumn = None
    Par48: ObjectColumn = None
    Par49: ObjectColumn = None
    Par50: ObjectColumn = None
    Par51: ObjectColumn = None
    Par52: ObjectColumn = None
    Par53: ObjectColumn = None
    Par54: ObjectColumn = None
    Par55: ObjectColumn = None
    Par56: ObjectColumn = None
    Par57: ObjectColumn = None
    Par58: ObjectColumn = None
    Par59: ObjectColumn = None
    Par60: ObjectColumn = None
    Par61: ObjectColumn = None
    Par62: ObjectColumn = None
    Par63: ObjectColumn = None
    Par64: ObjectColumn = None
    Par65: ObjectColumn = None
    Par66: ObjectColumn = None
    Par67: ObjectColumn = None
    Par68: ObjectColumn = None
    Par69: ObjectColumn = None
    Par70: ObjectColumn = None
    Par71: ObjectColumn = None
    Par72: ObjectColumn = None
    Par73: ObjectColumn = None
    Par74: ObjectColumn = None
    Par75: ObjectColumn = None
    Par76: ObjectColumn = None
    Par77: ObjectColumn = None
    Par78: ObjectColumn = None
    Par79: ObjectColumn = None
    Par80: ObjectColumn = None
    Par81: ObjectColumn = None
    Par82: ObjectColumn = None
    Par83: ObjectColumn = None
    Par84: ObjectColumn = None
    Par85: ObjectColumn = None
    Par86: ObjectColumn = None
    Par87: ObjectColumn = None
    Par88: ObjectColumn = None
    Par89: ObjectColumn = None
    Par90: ObjectColumn = None
    Par91: ObjectColumn = None
    Par92: ObjectColumn = None
    Par93: ObjectColumn = None
    Par94: ObjectColumn = None
    Par95: ObjectColumn = None
    Par96: ObjectColumn = None
    Par97: ObjectColumn = None
    Par98: ObjectColumn = None
    Par99: ObjectColumn = None
    Par100: ObjectColumn = None
    Par101: ObjectColumn = None
    Par102: ObjectColumn = None
    Par103: ObjectColumn = None
    Par104: ObjectColumn = None
    Par105: ObjectColumn = None
    Par106: ObjectColumn = None
    Par107: ObjectColumn = None
    Par108: ObjectColumn = None
    Par109: ObjectColumn = None
    Par110: ObjectColumn = None
    Par111: ObjectColumn = None
    Par112: ObjectColumn = None
    Par113: ObjectColumn = None
    Par114: ObjectColumn = None
    Par115: ObjectColumn = None
    Par116: ObjectColumn = None
    Par117: ObjectColumn = None
    Par118: ObjectColumn = None
    Par119: ObjectColumn = None
    Par120: ObjectColumn = None
    Par121: ObjectColumn = None
    Par122: ObjectColumn = None
    Par123: ObjectColumn = None
    Par124: ObjectColumn = None
    Par125: ObjectColumn = None
    Par126: ObjectColumn = None
    Par127: ObjectColumn = None
    Par128: ObjectColumn = None
    Par129: ObjectColumn = None
    Par130: ObjectColumn = None
    Par131: ObjectColumn = None
    Par132: ObjectColumn = None
    Par133: ObjectColumn = None
    Par134: ObjectColumn = None
    Par135: ObjectColumn = None
    Par136: ObjectColumn = None
    Par137: ObjectColumn = None
    Par138: ObjectColumn = None
    Par139: ObjectColumn = None
    Par140: ObjectColumn = None
    Par141: ObjectColumn = None
    Par142: ObjectColumn = None
    Par143: ObjectColumn = None
    Par144: ObjectColumn = None
    Par145: ObjectColumn = None
    Par146: ObjectColumn = None
    Par147: ObjectColumn = None
    Par148: ObjectColumn = None
    Par149: ObjectColumn = None
    Par150: ObjectColumn = None
    Par151: ObjectColumn = None
    Par152: ObjectColumn = None
    Par153: ObjectColumn = None
    Par154: ObjectColumn = None
    Par155: ObjectColumn = None
    Par156: ObjectColumn = None
    Par157: ObjectColumn = None
    Par158: ObjectColumn = None
    Par159: ObjectColumn = None
    Par160: ObjectColumn = None
    Par161: ObjectColumn = None
    Par162: ObjectColumn = None
    Par163: ObjectColumn = None
    Par164: ObjectColumn = None
    Par165: ObjectColumn = None
    Par166: ObjectColumn = None
    Par167: ObjectColumn = None
    Par168: ObjectColumn = None
    Par169: ObjectColumn = None
    Par170: ObjectColumn = None
    Par171: ObjectColumn = None
    Par172: ObjectColumn = None
    Par173: ObjectColumn = None
    Par174: ObjectColumn = None
    Par175: ObjectColumn = None
    Par176: ObjectColumn = None
    Par177: ObjectColumn = None
    Par178: ObjectColumn = None
    Par179: ObjectColumn = None
    Par180: ObjectColumn = None
    Par181: ObjectColumn = None
    Par182: ObjectColumn = None
    Par183: ObjectColumn = None
    Par184: ObjectColumn = None
    Par185: ObjectColumn = None
    Par186: ObjectColumn = None
    Par187: ObjectColumn = None
    Par188: ObjectColumn = None
    Par189: ObjectColumn = None
    Par190: ObjectColumn = None
    Par191: ObjectColumn = None
    Par192: ObjectColumn = None
    Par193: ObjectColumn = None
    Par194: ObjectColumn = None
    Par195: ObjectColumn = None
    Par196: ObjectColumn = None
    Par197: ObjectColumn = None
    Par198: ObjectColumn = None
    Par199: ObjectColumn = None
    Par200: ObjectColumn = None
    Par201: ObjectColumn = None
    Par202: ObjectColumn = None
    Par203: ObjectColumn = None
    Par204: ObjectColumn = None
    Par205: ObjectColumn = None
    Par206: ObjectColumn = None
    Par207: ObjectColumn = None
    Par208: ObjectColumn = None
    Par209: ObjectColumn = None
    Par210: ObjectColumn = None
    Par211: ObjectColumn = None
    Par212: ObjectColumn = None
    Par213: ObjectColumn = None
    Par214: ObjectColumn = None
    Par215: ObjectColumn = None
    Par216: ObjectColumn = None
    Par217: ObjectColumn = None
    Par218: ObjectColumn = None
    Par219: ObjectColumn = None
    Par220: ObjectColumn = None
    Par221: ObjectColumn = None
    Par222: ObjectColumn = None
    Par223: ObjectColumn = None
    Par224: ObjectColumn = None
    Par225: ObjectColumn = None
    Par226: ObjectColumn = None
    Par227: ObjectColumn = None
    Par228: ObjectColumn = None
    Par229: ObjectColumn = None
    Par230: ObjectColumn = None
    Par231: ObjectColumn = None
    Par232: ObjectColumn = None
    Par233: ObjectColumn = None
    Par234: ObjectColumn = None
    Par235: ObjectColumn = None
    Par236: ObjectColumn = None
    Par237: ObjectColumn = None
    Par238: ObjectColumn = None
    Par239: ObjectColumn = None
    Par240: ObjectColumn = None
    Par241: ObjectColumn = None
    Par242: ObjectColumn = None
    Par243: ObjectColumn = None
    Par244: ObjectColumn = None
    Par245: ObjectColumn = None
    Par246: ObjectColumn = None
    Par247: ObjectColumn = None
    Par248: ObjectColumn = None
    Par249: ObjectColumn = None
    Par250: ObjectColumn = None

class ObjectScatteringTypes:
    None_: ObjectScatteringTypes = None
    Lambertian: ObjectScatteringTypes = None
    Gaussian: ObjectScatteringTypes = None
    ABg: ObjectScatteringTypes = None
    ABgFile: ObjectScatteringTypes = None
    BSDF: ObjectScatteringTypes = None
    ISScatterCatalog: ObjectScatteringTypes = None
    User: ObjectScatteringTypes = None

class ObjectType:
    AnnularAsphericLens: ObjectType = None
    AnnularAxialLens: ObjectType = None
    AnnularVolume: ObjectType = None
    Annulus: ObjectType = None
    Array: ObjectType = None
    ArrayRing: ObjectType = None
    AsphericSurface: ObjectType = None
    AsphericSurface2: ObjectType = None
    AxiconSurface: ObjectType = None
    BiconicLens: ObjectType = None
    BiconicSurface: ObjectType = None
    BiconicZernike: ObjectType = None
    BiconicZernikeSurface: ObjectType = None
    Binary1: ObjectType = None
    Binary2: ObjectType = None
    Binary2A: ObjectType = None
    Boolean: ObjectType = None
    BooleanCAD: ObjectType = None
    CADAssemblyAutodeskInventor: ObjectType = None
    CADAssemblyCreoParametric: ObjectType = None
    CADAssemblySolidWorks: ObjectType = None
    CADPartAutodeskInventor: ObjectType = None
    CADPartCreoParametric: ObjectType = None
    CADPartSolidWorks: ObjectType = None
    CADPartSTEPIGESSAT: ObjectType = None
    CADPartSTL: ObjectType = None
    CADPartZPD: ObjectType = None
    Cone: ObjectType = None
    CPC: ObjectType = None
    CPCRectangular: ObjectType = None
    CylinderPipe: ObjectType = None
    CylinderVolume: ObjectType = None
    Cylinder2Pipe: ObjectType = None
    Cylinder2Volume: ObjectType = None
    DetectorColor: ObjectType = None
    DetectorPolar: ObjectType = None
    DetectorRectangle: ObjectType = None
    DetectorSurface: ObjectType = None
    DetectorVolume: ObjectType = None
    DiffractionGrating: ObjectType = None
    DualBEFSurface: ObjectType = None
    Ellipse: ObjectType = None
    EllipticalVolume: ObjectType = None
    EvenAsphereLens: ObjectType = None
    ExtendedOddAsphereLens: ObjectType = None
    ExtendedPolynomialLens: ObjectType = None
    ExtendedPolynomialSurface: ObjectType = None
    Extruded: ObjectType = None
    FacetedSurface: ObjectType = None
    FreeformZ: ObjectType = None
    Fresnel1: ObjectType = None
    Fresnel2: ObjectType = None
    GridSagLens: ObjectType = None
    GridSagSurface: ObjectType = None
    GridSagFrontBack: ObjectType = None
    HexagonalLensletArray: ObjectType = None
    HologramLens: ObjectType = None
    HologramSurface: ObjectType = None
    JonesMatrix: ObjectType = None
    LensletArray1: ObjectType = None
    LensletArray2: ObjectType = None
    MEMS: ObjectType = None
    NullObject: ObjectType = None
    OddAsphereLens: ObjectType = None
    ParaxialLens: ObjectType = None
    PolygonObject: ObjectType = None
    RayRotator: ObjectType = None
    RectangularCorner: ObjectType = None
    Rectangle: ObjectType = None
    RectangularPipe: ObjectType = None
    RectangularPipeGrating: ObjectType = None
    RectangularRoof: ObjectType = None
    RectangularTorusSurface: ObjectType = None
    RectangularTorusVolume: ObjectType = None
    RectangularVolume: ObjectType = None
    RectangularVolumeGrating: ObjectType = None
    ReverseRadianceDetector: ObjectType = None
    ReverseRadianceTarget: ObjectType = None
    Slide: ObjectType = None
    SourceDiffractive: ObjectType = None
    SourceDiode: ObjectType = None
    SourceDLL: ObjectType = None
    SourceEllipse: ObjectType = None
    SourceEULUMDATFile: ObjectType = None
    SourceFilament: ObjectType = None
    SourceFile: ObjectType = None
    SourceGaussian: ObjectType = None
    SourceIESNAFile: ObjectType = None
    SourceImported: ObjectType = None
    SourceObject: ObjectType = None
    SourcePoint: ObjectType = None
    SourceRadial: ObjectType = None
    SourceRay: ObjectType = None
    SourceRectangle: ObjectType = None
    SourceTube: ObjectType = None
    SourceTwoAngle: ObjectType = None
    SourceVolumeCylindrical: ObjectType = None
    SourceVolumeElliptical: ObjectType = None
    SourceVolumeRectangular: ObjectType = None
    Sphere: ObjectType = None
    StandardLens: ObjectType = None
    StandardSurface: ObjectType = None
    Swept: ObjectType = None
    TabulatedFactedRadial: ObjectType = None
    TabulatedFactedToroid: ObjectType = None
    TabulatedFrenselRadial: ObjectType = None
    ToroidalHologram: ObjectType = None
    ToroidalLens: ObjectType = None
    ToroidalSurface: ObjectType = None
    ToroidalSurfaceOddASphere: ObjectType = None
    TorusSurface: ObjectType = None
    TorusVolume: ObjectType = None
    TriangularCorner: ObjectType = None
    Triangle: ObjectType = None
    UserDefinedObject: ObjectType = None
    WolterSurface: ObjectType = None
    ZernikeSurface: ObjectType = None
    BooleanNative: ObjectType = None
    CompoundLens: ObjectType = None
    QTypeAsphereSurface: ObjectType = None
    OffAxisMirror: ObjectType = None

class OrderChoices:
    Before: OrderChoices = None
    After: OrderChoices = None

class PixelAddressing:
    ByRow: PixelAddressing = None
    ByColumn: PixelAddressing = None
    Individually: PixelAddressing = None

class PolarDetectorDataType:
    Power: PolarDetectorDataType = None
    PowerSolidAngle: PolarDetectorDataType = None
    Lumens: PolarDetectorDataType = None
    LumensSolidAngle: PolarDetectorDataType = None
    Cx: PolarDetectorDataType = None
    Cy: PolarDetectorDataType = None
    u_T: PolarDetectorDataType = None
    u_V: PolarDetectorDataType = None
    TriX: PolarDetectorDataType = None
    TriY: PolarDetectorDataType = None
    TriZ: PolarDetectorDataType = None

class RaysIgnoreObjectType:
    Never: RaysIgnoreObjectType = None
    Always: RaysIgnoreObjectType = None
    OnLaunch: RaysIgnoreObjectType = None

class RayTraceModes:
    Standard: RayTraceModes = None
    Flat: RayTraceModes = None
    Shaded: RayTraceModes = None
    Kernel: RayTraceModes = None

class ScatterToType:
    ScatterToList: ScatterToType = None
    ImportanceSampling: ScatterToType = None

class ShapeChoices:
    Rectangular: ShapeChoices = None
    Elliptical: ShapeChoices = None

class SourceBulkScatterMode:
    Many: SourceBulkScatterMode = None
    Once: SourceBulkScatterMode = None
    Never: SourceBulkScatterMode = None

class SourceColorMode:
    SystemWavelengths: SourceColorMode = None
    CIE1931Tristimulus: SourceColorMode = None
    CIE1931Chromaticity: SourceColorMode = None
    CIE1931RGB: SourceColorMode = None
    UniformPowerSpectrum: SourceColorMode = None
    D65White: SourceColorMode = None
    ColorTemperature: SourceColorMode = None
    BlackBodySpectrum: SourceColorMode = None
    SpectrumFile: SourceColorMode = None
    CIE1976: SourceColorMode = None

class SourceSamplingMethod:
    Random: SourceSamplingMethod = None
    Sobol: SourceSamplingMethod = None

class UniformAngleChoices:
    UniformIrradiance: UniformAngleChoices = None
    UniformInAngleSpace: UniformAngleChoices = None

class VolumePhysicsModelType:
    None_: VolumePhysicsModelType = None
    AngleScattering: VolumePhysicsModelType = None
    DLLDefinedScattering: VolumePhysicsModelType = None
    PhotoluminescenceModel: VolumePhysicsModelType = None
