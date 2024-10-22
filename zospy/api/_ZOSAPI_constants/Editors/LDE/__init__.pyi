"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = (
    "CoatingStatusType",
    "ConversionOrder",
    "CoordinateConversionResult",
    "CoordinateReturnType",
    "IndexDataType",
    "InterpolationMethod",
    "NodesDataType",
    "PilotRadiusMode",
    "PointCloudFileFormat",
    "PupilApodizationType",
    "QTypes",
    "STARDeformationOption",
    "SubstrateType",
    "SurfaceApertureTypes",
    "SurfaceColumn",
    "SurfaceEdgeDraw",
    "SurfaceScatteringTypes",
    "SurfaceType",
    "TiltDecenterOrderType",
    "TiltDecenterPickupType",
    "TiltType",
    "XYSampling",
)

class CoatingStatusType:
    Fixed: CoatingStatusType = None
    Variable: CoatingStatusType = None
    Pickup: CoatingStatusType = None

class ConversionOrder:
    Forward: ConversionOrder = None
    Reverse: ConversionOrder = None

class CoordinateConversionResult:
    Success: CoordinateConversionResult = None
    Error_MultiConfig: CoordinateConversionResult = None
    Error_TiltDecenter: CoordinateConversionResult = None
    Error_IgnoredSurface: CoordinateConversionResult = None
    Error_CoordianteBreak: CoordinateConversionResult = None
    Error_InvalidRange: CoordinateConversionResult = None

class CoordinateReturnType:
    None_: CoordinateReturnType = None
    OrientationOnly: CoordinateReturnType = None
    OrientationXY: CoordinateReturnType = None
    OrientationXYZ: CoordinateReturnType = None

class IndexDataType:
    None_: IndexDataType = None
    PhysicsBasedIndex: IndexDataType = None
    DirectRefractiveIndex: IndexDataType = None
    Unknown: IndexDataType = None

class InterpolationMethod:
    BicubicSpline: InterpolationMethod = None
    Linear: InterpolationMethod = None

class NodesDataType:
    SurfaceDeformationNoRBM: NodesDataType = None
    RefractiveIndex: NodesDataType = None
    TemperatureAndRefractiveIndex: NodesDataType = None
    SurfaceDeformation: NodesDataType = None

class PilotRadiusMode:
    BestFit: PilotRadiusMode = None
    Shorter: PilotRadiusMode = None
    Longer: PilotRadiusMode = None
    X: PilotRadiusMode = None
    Y: PilotRadiusMode = None
    Plane: PilotRadiusMode = None
    User: PilotRadiusMode = None

class PointCloudFileFormat:
    ASCII: PointCloudFileFormat = None
    Binary: PointCloudFileFormat = None
    CompressedBinary: PointCloudFileFormat = None

class PupilApodizationType:
    None_: PupilApodizationType = None
    Gaussian: PupilApodizationType = None
    Tangential: PupilApodizationType = None

class QTypes:
    Qbfs: QTypes = None
    Qcon: QTypes = None

class STARDeformationOption:
    DeformationWithRBMs: STARDeformationOption = None
    DeformationWithoutRBMs: STARDeformationOption = None
    OnlyRBMs: STARDeformationOption = None
    NoDeformation: STARDeformationOption = None

class SubstrateType:
    None_: SubstrateType = None
    Flat: SubstrateType = None
    Curved: SubstrateType = None

class SurfaceApertureTypes:
    None_: SurfaceApertureTypes = None
    CircularAperture: SurfaceApertureTypes = None
    CircularObscuration: SurfaceApertureTypes = None
    Spider: SurfaceApertureTypes = None
    RectangularAperture: SurfaceApertureTypes = None
    RectangularObscuration: SurfaceApertureTypes = None
    EllipticalAperture: SurfaceApertureTypes = None
    EllipticalObscuration: SurfaceApertureTypes = None
    UserAperture: SurfaceApertureTypes = None
    UserObscuration: SurfaceApertureTypes = None
    FloatingAperture: SurfaceApertureTypes = None

class SurfaceColumn:
    Comment: SurfaceColumn = None
    Radius: SurfaceColumn = None
    Thickness: SurfaceColumn = None
    Material: SurfaceColumn = None
    Coating: SurfaceColumn = None
    SemiDiameter: SurfaceColumn = None
    ChipZone: SurfaceColumn = None
    MechanicalSemiDiameter: SurfaceColumn = None
    Conic: SurfaceColumn = None
    TCE: SurfaceColumn = None
    Par0: SurfaceColumn = None
    Par1: SurfaceColumn = None
    Par2: SurfaceColumn = None
    Par3: SurfaceColumn = None
    Par4: SurfaceColumn = None
    Par5: SurfaceColumn = None
    Par6: SurfaceColumn = None
    Par7: SurfaceColumn = None
    Par8: SurfaceColumn = None
    Par9: SurfaceColumn = None
    Par10: SurfaceColumn = None
    Par11: SurfaceColumn = None
    Par12: SurfaceColumn = None
    Par13: SurfaceColumn = None
    Par14: SurfaceColumn = None
    Par15: SurfaceColumn = None
    Par16: SurfaceColumn = None
    Par17: SurfaceColumn = None
    Par18: SurfaceColumn = None
    Par19: SurfaceColumn = None
    Par20: SurfaceColumn = None
    Par21: SurfaceColumn = None
    Par22: SurfaceColumn = None
    Par23: SurfaceColumn = None
    Par24: SurfaceColumn = None
    Par25: SurfaceColumn = None
    Par26: SurfaceColumn = None
    Par27: SurfaceColumn = None
    Par28: SurfaceColumn = None
    Par29: SurfaceColumn = None
    Par30: SurfaceColumn = None
    Par31: SurfaceColumn = None
    Par32: SurfaceColumn = None
    Par33: SurfaceColumn = None
    Par34: SurfaceColumn = None
    Par35: SurfaceColumn = None
    Par36: SurfaceColumn = None
    Par37: SurfaceColumn = None
    Par38: SurfaceColumn = None
    Par39: SurfaceColumn = None
    Par40: SurfaceColumn = None
    Par41: SurfaceColumn = None
    Par42: SurfaceColumn = None
    Par43: SurfaceColumn = None
    Par44: SurfaceColumn = None
    Par45: SurfaceColumn = None
    Par46: SurfaceColumn = None
    Par47: SurfaceColumn = None
    Par48: SurfaceColumn = None
    Par49: SurfaceColumn = None
    Par50: SurfaceColumn = None
    Par51: SurfaceColumn = None
    Par52: SurfaceColumn = None
    Par53: SurfaceColumn = None
    Par54: SurfaceColumn = None
    Par55: SurfaceColumn = None
    Par56: SurfaceColumn = None
    Par57: SurfaceColumn = None
    Par58: SurfaceColumn = None
    Par59: SurfaceColumn = None
    Par60: SurfaceColumn = None
    Par61: SurfaceColumn = None
    Par62: SurfaceColumn = None
    Par63: SurfaceColumn = None
    Par64: SurfaceColumn = None
    Par65: SurfaceColumn = None
    Par66: SurfaceColumn = None
    Par67: SurfaceColumn = None
    Par68: SurfaceColumn = None
    Par69: SurfaceColumn = None
    Par70: SurfaceColumn = None
    Par71: SurfaceColumn = None
    Par72: SurfaceColumn = None
    Par73: SurfaceColumn = None
    Par74: SurfaceColumn = None
    Par75: SurfaceColumn = None
    Par76: SurfaceColumn = None
    Par77: SurfaceColumn = None
    Par78: SurfaceColumn = None
    Par79: SurfaceColumn = None
    Par80: SurfaceColumn = None
    Par81: SurfaceColumn = None
    Par82: SurfaceColumn = None
    Par83: SurfaceColumn = None
    Par84: SurfaceColumn = None
    Par85: SurfaceColumn = None
    Par86: SurfaceColumn = None
    Par87: SurfaceColumn = None
    Par88: SurfaceColumn = None
    Par89: SurfaceColumn = None
    Par90: SurfaceColumn = None
    Par91: SurfaceColumn = None
    Par92: SurfaceColumn = None
    Par93: SurfaceColumn = None
    Par94: SurfaceColumn = None
    Par95: SurfaceColumn = None
    Par96: SurfaceColumn = None
    Par97: SurfaceColumn = None
    Par98: SurfaceColumn = None
    Par99: SurfaceColumn = None
    Par100: SurfaceColumn = None
    Par101: SurfaceColumn = None
    Par102: SurfaceColumn = None
    Par103: SurfaceColumn = None
    Par104: SurfaceColumn = None
    Par105: SurfaceColumn = None
    Par106: SurfaceColumn = None
    Par107: SurfaceColumn = None
    Par108: SurfaceColumn = None
    Par109: SurfaceColumn = None
    Par110: SurfaceColumn = None
    Par111: SurfaceColumn = None
    Par112: SurfaceColumn = None
    Par113: SurfaceColumn = None
    Par114: SurfaceColumn = None
    Par115: SurfaceColumn = None
    Par116: SurfaceColumn = None
    Par117: SurfaceColumn = None
    Par118: SurfaceColumn = None
    Par119: SurfaceColumn = None
    Par120: SurfaceColumn = None
    Par121: SurfaceColumn = None
    Par122: SurfaceColumn = None
    Par123: SurfaceColumn = None
    Par124: SurfaceColumn = None
    Par125: SurfaceColumn = None
    Par126: SurfaceColumn = None
    Par127: SurfaceColumn = None
    Par128: SurfaceColumn = None
    Par129: SurfaceColumn = None
    Par130: SurfaceColumn = None
    Par131: SurfaceColumn = None
    Par132: SurfaceColumn = None
    Par133: SurfaceColumn = None
    Par134: SurfaceColumn = None
    Par135: SurfaceColumn = None
    Par136: SurfaceColumn = None
    Par137: SurfaceColumn = None
    Par138: SurfaceColumn = None
    Par139: SurfaceColumn = None
    Par140: SurfaceColumn = None
    Par141: SurfaceColumn = None
    Par142: SurfaceColumn = None
    Par143: SurfaceColumn = None
    Par144: SurfaceColumn = None
    Par145: SurfaceColumn = None
    Par146: SurfaceColumn = None
    Par147: SurfaceColumn = None
    Par148: SurfaceColumn = None
    Par149: SurfaceColumn = None
    Par150: SurfaceColumn = None
    Par151: SurfaceColumn = None
    Par152: SurfaceColumn = None
    Par153: SurfaceColumn = None
    Par154: SurfaceColumn = None
    Par155: SurfaceColumn = None
    Par156: SurfaceColumn = None
    Par157: SurfaceColumn = None
    Par158: SurfaceColumn = None
    Par159: SurfaceColumn = None
    Par160: SurfaceColumn = None
    Par161: SurfaceColumn = None
    Par162: SurfaceColumn = None
    Par163: SurfaceColumn = None
    Par164: SurfaceColumn = None
    Par165: SurfaceColumn = None
    Par166: SurfaceColumn = None
    Par167: SurfaceColumn = None
    Par168: SurfaceColumn = None
    Par169: SurfaceColumn = None
    Par170: SurfaceColumn = None
    Par171: SurfaceColumn = None
    Par172: SurfaceColumn = None
    Par173: SurfaceColumn = None
    Par174: SurfaceColumn = None
    Par175: SurfaceColumn = None
    Par176: SurfaceColumn = None
    Par177: SurfaceColumn = None
    Par178: SurfaceColumn = None
    Par179: SurfaceColumn = None
    Par180: SurfaceColumn = None
    Par181: SurfaceColumn = None
    Par182: SurfaceColumn = None
    Par183: SurfaceColumn = None
    Par184: SurfaceColumn = None
    Par185: SurfaceColumn = None
    Par186: SurfaceColumn = None
    Par187: SurfaceColumn = None
    Par188: SurfaceColumn = None
    Par189: SurfaceColumn = None
    Par190: SurfaceColumn = None
    Par191: SurfaceColumn = None
    Par192: SurfaceColumn = None
    Par193: SurfaceColumn = None
    Par194: SurfaceColumn = None
    Par195: SurfaceColumn = None
    Par196: SurfaceColumn = None
    Par197: SurfaceColumn = None
    Par198: SurfaceColumn = None
    Par199: SurfaceColumn = None
    Par200: SurfaceColumn = None
    Par201: SurfaceColumn = None
    Par202: SurfaceColumn = None
    Par203: SurfaceColumn = None
    Par204: SurfaceColumn = None
    Par205: SurfaceColumn = None
    Par206: SurfaceColumn = None
    Par207: SurfaceColumn = None
    Par208: SurfaceColumn = None
    Par209: SurfaceColumn = None
    Par210: SurfaceColumn = None
    Par211: SurfaceColumn = None
    Par212: SurfaceColumn = None
    Par213: SurfaceColumn = None
    Par214: SurfaceColumn = None
    Par215: SurfaceColumn = None
    Par216: SurfaceColumn = None
    Par217: SurfaceColumn = None
    Par218: SurfaceColumn = None
    Par219: SurfaceColumn = None
    Par220: SurfaceColumn = None
    Par221: SurfaceColumn = None
    Par222: SurfaceColumn = None
    Par223: SurfaceColumn = None
    Par224: SurfaceColumn = None
    Par225: SurfaceColumn = None
    Par226: SurfaceColumn = None
    Par227: SurfaceColumn = None
    Par228: SurfaceColumn = None
    Par229: SurfaceColumn = None
    Par230: SurfaceColumn = None
    Par231: SurfaceColumn = None
    Par232: SurfaceColumn = None
    Par233: SurfaceColumn = None
    Par234: SurfaceColumn = None
    Par235: SurfaceColumn = None
    Par236: SurfaceColumn = None
    Par237: SurfaceColumn = None
    Par238: SurfaceColumn = None
    Par239: SurfaceColumn = None
    Par240: SurfaceColumn = None
    Par241: SurfaceColumn = None
    Par242: SurfaceColumn = None
    Par243: SurfaceColumn = None
    Par244: SurfaceColumn = None
    Par245: SurfaceColumn = None
    Par246: SurfaceColumn = None
    Par247: SurfaceColumn = None
    Par248: SurfaceColumn = None
    Par249: SurfaceColumn = None
    Par250: SurfaceColumn = None
    Par251: SurfaceColumn = None
    Par252: SurfaceColumn = None
    Par253: SurfaceColumn = None
    Par254: SurfaceColumn = None

class SurfaceEdgeDraw:
    Squared: SurfaceEdgeDraw = None
    Tapered: SurfaceEdgeDraw = None
    Flat: SurfaceEdgeDraw = None

class SurfaceScatteringTypes:
    None_: SurfaceScatteringTypes = None
    Lambertian: SurfaceScatteringTypes = None
    Gaussian: SurfaceScatteringTypes = None
    ABg: SurfaceScatteringTypes = None
    ABgFile: SurfaceScatteringTypes = None
    BSDF: SurfaceScatteringTypes = None
    User: SurfaceScatteringTypes = None
    ISScatterCatalog: SurfaceScatteringTypes = None

class SurfaceType:
    ABCD: SurfaceType = None
    AlternateEven: SurfaceType = None
    AlternateOdd: SurfaceType = None
    AnnularZernikeSag: SurfaceType = None
    Atmospheric: SurfaceType = None
    Biconic: SurfaceType = None
    BiconicZernike: SurfaceType = None
    Binary1: SurfaceType = None
    Binary2: SurfaceType = None
    Binary3: SurfaceType = None
    Binary4: SurfaceType = None
    BirefringentIn: SurfaceType = None
    BirefringentOut: SurfaceType = None
    BlackBoxLens: SurfaceType = None
    ChebyShv: SurfaceType = None
    Conjugate: SurfaceType = None
    CoordinateBreak: SurfaceType = None
    CubicSpline: SurfaceType = None
    CylinderFrensel: SurfaceType = None
    CylinderFresnel: SurfaceType = None
    Data: SurfaceType = None
    DiffractionGrating: SurfaceType = None
    EllipticalGrating1: SurfaceType = None
    EllipticalGrating2: SurfaceType = None
    EvenAspheric: SurfaceType = None
    ExtendedToroidalGrating: SurfaceType = None
    ExtendedAsphere: SurfaceType = None
    ExtendedCubicSpline: SurfaceType = None
    ExtendedFresnel: SurfaceType = None
    ExtendedOddAsphere: SurfaceType = None
    ExtendedPolynomial: SurfaceType = None
    Fresnel: SurfaceType = None
    GeneralizedFresnel: SurfaceType = None
    Gradient1: SurfaceType = None
    Gradient2: SurfaceType = None
    Gradient3: SurfaceType = None
    Gradient4: SurfaceType = None
    Gradient5: SurfaceType = None
    Gradient6: SurfaceType = None
    Gradient7: SurfaceType = None
    Gradient9: SurfaceType = None
    Gradient10: SurfaceType = None
    Gradient12: SurfaceType = None
    Gradium: SurfaceType = None
    GridGradient: SurfaceType = None
    GridPhase: SurfaceType = None
    GridSag: SurfaceType = None
    Hologram1: SurfaceType = None
    Hologram2: SurfaceType = None
    Irregular: SurfaceType = None
    JonesMatrix: SurfaceType = None
    NonSequential: SurfaceType = None
    OddAsphere: SurfaceType = None
    OddCosine: SurfaceType = None
    OffAxisConicFreeform: SurfaceType = None
    OpticallyFabricatedHologram: SurfaceType = None
    Paraxial: SurfaceType = None
    ParaxialXY: SurfaceType = None
    Periodic: SurfaceType = None
    Polynomial: SurfaceType = None
    QTypeAsphere: SurfaceType = None
    QTypeFreeform: SurfaceType = None
    RadialGrating: SurfaceType = None
    RadialNurbs: SurfaceType = None
    RetroReflect: SurfaceType = None
    SlideSurface: SurfaceType = None
    Standard: SurfaceType = None
    Superconic: SurfaceType = None
    Tilted: SurfaceType = None
    Toroidal: SurfaceType = None
    ToroidalGrat: SurfaceType = None
    ToroidalHologram: SurfaceType = None
    ToroidalNurbs: SurfaceType = None
    UserDefined: SurfaceType = None
    VariableLineSpaceGrating: SurfaceType = None
    ZernikeAnnularPhase: SurfaceType = None
    ZernikeFringePhase: SurfaceType = None
    ZernikeFringeSag: SurfaceType = None
    ZernikeStandardPhase: SurfaceType = None
    ZernikeStandardSag: SurfaceType = None
    ZonePlate: SurfaceType = None
    Freeform: SurfaceType = None

class TiltDecenterOrderType:
    Decenter_Tilt: TiltDecenterOrderType = None
    Tilt_Decenter: TiltDecenterOrderType = None

class TiltDecenterPickupType:
    Explicit: TiltDecenterPickupType = None
    PickupSurface: TiltDecenterPickupType = None
    ReverseSurface: TiltDecenterPickupType = None

class TiltType:
    XTilt: TiltType = None
    YTilt: TiltType = None

class XYSampling:
    S32: XYSampling = None
    S64: XYSampling = None
    S128: XYSampling = None
    S256: XYSampling = None
    S512: XYSampling = None
    S1024: XYSampling = None
    S2048: XYSampling = None
    S4096: XYSampling = None
    S8192: XYSampling = None
    S16384: XYSampling = None
