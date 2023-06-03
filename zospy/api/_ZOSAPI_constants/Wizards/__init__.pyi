"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

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

class CriterionTypes(Enum):
    Wavefront = 0
    Contrast = 1
    Spot = 2
    Angular = 3

class DefaultAndDegrees(Enum):
    Default = 0
    Degrees = 1

class DefaultAndFringes(Enum):
    Default = 0
    Fringes = 1
    Percent = 2

class OptimizationTypes(Enum):
    RMS = 0
    PTV = 1

class PupilArmsCount(Enum):
    Arms_6 = 0
    Arms_8 = 1
    Arms_10 = 2
    Arms_12 = 3

class ReferenceTypes(Enum):
    Centroid = 0
    ChiefRay = 1
    Unreferenced = 2

class ToleranceGrade(Enum):
    Commercial = 0
    Precision = 1
    HighPrecision = 2
    CellPhoneLens = 3

class ToleranceVendor(Enum):
    Asphericon = 0
    EdmundOptics = 1
    Generic = 2
    LaCroix = 3
    Optimax = 4

class WizardType(Enum):
    NSCOptimization = 0
    NSCBitmap = 1
    NSCRoadwayLighting = 2
    SEQOptimization = 3
    NSCTolerance = 4
    SEQTolerance = 5
