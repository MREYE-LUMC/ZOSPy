"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

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
    "RayAimingType",
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

class FieldColumn:
    Comment: FieldColumn = None
    X: FieldColumn = None
    Y: FieldColumn = None
    Weight: FieldColumn = None
    VDX: FieldColumn = None
    VDY: FieldColumn = None
    VCX: FieldColumn = None
    VCY: FieldColumn = None
    TAN: FieldColumn = None
    VAN: FieldColumn = None

class FieldNormalizationType:
    Radial: FieldNormalizationType = None
    Rectangular: FieldNormalizationType = None

class FieldPattern:
    UniformY: FieldPattern = None
    EqualAreaY: FieldPattern = None
    UniformX: FieldPattern = None
    EqualAreaX: FieldPattern = None
    Grid: FieldPattern = None
    UniformRadial: FieldPattern = None
    EqualAreaRadial: FieldPattern = None

class FieldType:
    Angle: FieldType = None
    ObjectHeight: FieldType = None
    ParaxialImageHeight: FieldType = None
    RealImageHeight: FieldType = None
    TheodoliteAngle: FieldType = None

class FNumberComputationType:
    TracingRays: FNumberComputationType = None
    PupilSizePosition: FNumberComputationType = None

class HuygensIntegralSettings:
    Auto: HuygensIntegralSettings = None
    Planar: HuygensIntegralSettings = None
    Spherical: HuygensIntegralSettings = None

class ParaxialRaysSetting:
    ConsiderCoordinateBreaks: ParaxialRaysSetting = None
    IgnoreCoordinateBreaks: ParaxialRaysSetting = None

class PolarizationMethod:
    XAxisMethod: PolarizationMethod = None
    YAxisMethod: PolarizationMethod = None
    ZAxisMethod: PolarizationMethod = None

class QuadratureSteps:
    S2: QuadratureSteps = None
    S4: QuadratureSteps = None
    S6: QuadratureSteps = None
    S8: QuadratureSteps = None
    S10: QuadratureSteps = None
    S12: QuadratureSteps = None

class RayAimingMethod:
    Off: RayAimingMethod = None
    Paraxial: RayAimingMethod = None
    Real: RayAimingMethod = None

class RayAimingType:
    Heuristic: RayAimingType = None
    Optimize: RayAimingType = None

class ReferenceOPDSetting:
    Absolute: ReferenceOPDSetting = None
    Infinity: ReferenceOPDSetting = None
    ExitPupil: ReferenceOPDSetting = None
    Absolute2: ReferenceOPDSetting = None

class WavelengthPreset:
    FdC_Visible: WavelengthPreset = None
    Photopic_Bright: WavelengthPreset = None
    Scotopic_Dark: WavelengthPreset = None
    HeNe_0p6328: WavelengthPreset = None
    HeNe_0p5438: WavelengthPreset = None
    Argon_0p4880: WavelengthPreset = None
    Argon_0p5145: WavelengthPreset = None
    NDYAG_1p0641: WavelengthPreset = None
    NDGlass_1p054: WavelengthPreset = None
    CO2_10p60: WavelengthPreset = None
    CrLiSAF_0p840: WavelengthPreset = None
    TiAl203_0p760: WavelengthPreset = None
    Ruby_0p6943: WavelengthPreset = None
    HeCadmium_0p4416: WavelengthPreset = None
    HeCadmium_0p3536: WavelengthPreset = None
    HeCadmium_0p3250: WavelengthPreset = None
    t_1p014: WavelengthPreset = None
    r_0p707: WavelengthPreset = None
    C_0p656: WavelengthPreset = None
    d_0p587: WavelengthPreset = None
    F_0p486: WavelengthPreset = None
    g_0p436: WavelengthPreset = None
    i_0p365: WavelengthPreset = None
    Fp_0p365: WavelengthPreset = None
    e_0p54607: WavelengthPreset = None
    Cp_0p6438469: WavelengthPreset = None
    FpeCp_Visible: WavelengthPreset = None
    THz_193p10: WavelengthPreset = None

class ZemaxAfocalModeUnits:
    Microradians: ZemaxAfocalModeUnits = None
    Milliradians: ZemaxAfocalModeUnits = None
    Radians: ZemaxAfocalModeUnits = None
    ArcSeconds: ZemaxAfocalModeUnits = None
    ArcMinutes: ZemaxAfocalModeUnits = None
    Degrees: ZemaxAfocalModeUnits = None

class ZemaxAnalysisUnits:
    WattsPerMMSq: ZemaxAnalysisUnits = None
    WattsPerCMSq: ZemaxAnalysisUnits = None
    WattsPerinSq: ZemaxAnalysisUnits = None
    WattsPerMSq: ZemaxAnalysisUnits = None
    WattsPerftSq: ZemaxAnalysisUnits = None

class ZemaxApertureType:
    EntrancePupilDiameter: ZemaxApertureType = None
    ImageSpaceFNum: ZemaxApertureType = None
    ObjectSpaceNA: ZemaxApertureType = None
    FloatByStopSize: ZemaxApertureType = None
    ParaxialWorkingFNum: ZemaxApertureType = None
    ObjectConeAngle: ZemaxApertureType = None

class ZemaxApodizationType:
    Uniform: ZemaxApodizationType = None
    Gaussian: ZemaxApodizationType = None
    CosineCubed: ZemaxApodizationType = None

class ZemaxMTFUnits:
    CyclesPerMillimeter: ZemaxMTFUnits = None
    CyclesPerMilliradian: ZemaxMTFUnits = None

class ZemaxSourceUnits:
    Watts: ZemaxSourceUnits = None
    Lumens: ZemaxSourceUnits = None
    Joules: ZemaxSourceUnits = None

class ZemaxSystemUnits:
    Millimeters: ZemaxSystemUnits = None
    Centimeters: ZemaxSystemUnits = None
    Inches: ZemaxSystemUnits = None
    Meters: ZemaxSystemUnits = None

class ZemaxUnitPrefix:
    Femto: ZemaxUnitPrefix = None
    Pico: ZemaxUnitPrefix = None
    Nano: ZemaxUnitPrefix = None
    Micro: ZemaxUnitPrefix = None
    Milli: ZemaxUnitPrefix = None
    None_: ZemaxUnitPrefix = None
    Kilo: ZemaxUnitPrefix = None
    Mega: ZemaxUnitPrefix = None
    Giga: ZemaxUnitPrefix = None
    Tera: ZemaxUnitPrefix = None
