"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = (
    "FieldColumn",
    "FieldNormalizationType",
    "FieldPattern",
    "FieldType",
    "FNumberComputationType",
    "HuygensIntegralSettings",
    "ParaxialRaysSetting",
    "PolarizationMethod",
    "QuadratureSteps",
    "RayAimingMethod",
    "ReferenceOPDSetting",
    "WavelengthPreset",
    "ZemaxAfocalModeUnits",
    "ZemaxAnalysisUnits",
    "ZemaxApertureType",
    "ZemaxApodizationType",
    "ZemaxMTFUnits",
    "ZemaxSourceUnits",
    "ZemaxSystemUnits",
    "ZemaxUnitPrefix",
)

class FieldColumn(Enum):
    Comment = 0
    X = 1
    Y = 2
    Weight = 3
    VDX = 4
    VDY = 5
    VCX = 6
    VCY = 7
    TAN = 8
    VAN = 8

class FieldNormalizationType(Enum):
    Radial = 0
    Rectangular = 1

class FieldPattern(Enum):
    UniformY = 0
    EqualAreaY = 1
    UniformX = 2
    EqualAreaX = 3
    Grid = 4
    UniformRadial = 5
    EqualAreaRadial = 6

class FieldType(Enum):
    Angle = 0
    ObjectHeight = 1
    ParaxialImageHeight = 2
    RealImageHeight = 3
    TheodoliteAngle = 4

class FNumberComputationType(Enum):
    TracingRays = 0
    PupilSizePosition = 1

class HuygensIntegralSettings(Enum):
    Auto = 0
    Planar = 1
    Spherical = 2

class ParaxialRaysSetting(Enum):
    ConsiderCoordinateBreaks = 0
    IgnoreCoordinateBreaks = 1

class PolarizationMethod(Enum):
    XAxisMethod = 0
    YAxisMethod = 1
    ZAxisMethod = 2

class QuadratureSteps(Enum):
    S2 = 0
    S4 = 1
    S6 = 2
    S8 = 3
    S10 = 4
    S12 = 5

class RayAimingMethod(Enum):
    Off = 0
    Paraxial = 1
    Real = 2

class ReferenceOPDSetting(Enum):
    Absolute = 0
    Infinity = 1
    ExitPupil = 2
    Absolute2 = 3

class WavelengthPreset(Enum):
    FdC_Visible = 0
    Photopic_Bright = 1
    Scotopic_Dark = 2
    HeNe_0p6328 = 3
    HeNe_0p5438 = 4
    Argon_0p4880 = 5
    Argon_0p5145 = 6
    NDYAG_1p0641 = 7
    NDGlass_1p054 = 8
    CO2_10p60 = 9
    CrLiSAF_0p840 = 10
    TiAl203_0p760 = 11
    Ruby_0p6943 = 12
    HeCadmium_0p4416 = 13
    HeCadmium_0p3536 = 14
    HeCadmium_0p3250 = 15
    t_1p014 = 16
    r_0p707 = 17
    C_0p656 = 18
    d_0p587 = 19
    F_0p486 = 20
    g_0p436 = 21
    i_0p365 = 22
    Fp_0p365 = 23
    e_0p54607 = 24
    Cp_0p6438469 = 25
    FpeCp_Visible = 26
    THz_193p10 = 27

class ZemaxAfocalModeUnits(Enum):
    Microradians = 0
    Milliradians = 1
    Radians = 2
    ArcSeconds = 3
    ArcMinutes = 4
    Degrees = 5

class ZemaxAnalysisUnits(Enum):
    WattsPerMMSq = 0
    WattsPerCMSq = 1
    WattsPerinSq = 2
    WattsPerMSq = 3
    WattsPerftSq = 4

class ZemaxApertureType(Enum):
    EntrancePupilDiameter = 0
    ImageSpaceFNum = 1
    ObjectSpaceNA = 2
    FloatByStopSize = 3
    ParaxialWorkingFNum = 4
    ObjectConeAngle = 5

class ZemaxApodizationType(Enum):
    Uniform = 0
    Gaussian = 1
    CosineCubed = 2

class ZemaxMTFUnits(Enum):
    CyclesPerMillimeter = 0
    CyclesPerMilliradian = 1

class ZemaxSourceUnits(Enum):
    Watts = 0
    Lumens = 1
    Joules = 2

class ZemaxSystemUnits(Enum):
    Millimeters = 0
    Centimeters = 1
    Inches = 2
    Meters = 3

class ZemaxUnitPrefix(Enum):
    Femto = 0
    Pico = 1
    Nano = 2
    Micro = 3
    Milli = 4
    None_ = 5
    Kilo = 6
    Mega = 7
    Giga = 8
    Tera = 9
