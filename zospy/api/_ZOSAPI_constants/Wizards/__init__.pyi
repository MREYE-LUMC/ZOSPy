"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = (
    "CriterionTypes",
    "DefaultAndDegrees",
    "DefaultAndFringes",
    "OptimizationTypes",
    "PupilArmsCount",
    "ReferenceTypes",
    "ToleranceGrade",
    "ToleranceVendor",
    "WizardType",
)

class CriterionTypes:
    Wavefront: CriterionTypes = None
    Contrast: CriterionTypes = None
    Spot: CriterionTypes = None
    Angular: CriterionTypes = None

class DefaultAndDegrees:
    Default: DefaultAndDegrees = None
    Degrees: DefaultAndDegrees = None

class DefaultAndFringes:
    Default: DefaultAndFringes = None
    Fringes: DefaultAndFringes = None
    Percent: DefaultAndFringes = None

class OptimizationTypes:
    RMS: OptimizationTypes = None
    PTV: OptimizationTypes = None

class PupilArmsCount:
    Arms_6: PupilArmsCount = None
    Arms_8: PupilArmsCount = None
    Arms_10: PupilArmsCount = None
    Arms_12: PupilArmsCount = None

class ReferenceTypes:
    Centroid: ReferenceTypes = None
    ChiefRay: ReferenceTypes = None
    Unreferenced: ReferenceTypes = None

class ToleranceGrade:
    Commercial: ToleranceGrade = None
    Precision: ToleranceGrade = None
    HighPrecision: ToleranceGrade = None
    CellPhoneLens: ToleranceGrade = None

class ToleranceVendor:
    Asphericon: ToleranceVendor = None
    EdmundOptics: ToleranceVendor = None
    Generic: ToleranceVendor = None
    LaCroix: ToleranceVendor = None
    Optimax: ToleranceVendor = None

class WizardType:
    NSCOptimization: WizardType = None
    NSCBitmap: WizardType = None
    NSCRoadwayLighting: WizardType = None
    SEQOptimization: WizardType = None
    NSCTolerance: WizardType = None
    SEQTolerance: WizardType = None
