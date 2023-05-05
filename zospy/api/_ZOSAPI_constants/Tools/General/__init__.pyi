"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = (
    "ACISExportVersion",
    "ArchiveFileStatus",
    "CADAngularToleranceType",
    "CADFileType",
    "CADToleranceType",
    "DataTypes",
    "EntryCompressionModes",
    "LensShape",
    "LensType",
    "QuickAdjustCriterion",
    "QuickAdjustType",
    "QuickFocusCriterion",
    "RayPatternType",
    "ScaleToUnits",
    "SplineSegmentsType",
    "ZemaxFileTypes",
)

class ACISExportVersion(Enum):
    Current = 0
    V25 = 1
    V26 = 2
    V27 = 3
    V28 = 4
    V29 = 5
    V30 = 6

class ArchiveFileStatus(Enum):
    Okay = 0
    InvalidVersion = -3
    InvalidFile = -2
    UnableToOpen = -1

class CADAngularToleranceType(Enum):
    Low = 0
    Medium = 1
    High = 2
    Presentation = 3

class CADFileType(Enum):
    IGES = 0
    STEP = 1
    SAT = 2
    STL = 3
    SAB = 4
    ASAT = 5
    ASAB = 6
    MODEL = 7
    CATPART = 8
    CATPRODUCT = 9
    XCGM = 10

class CADToleranceType(Enum):
    N_TenEMinus4 = 0
    N_TenEMinus5 = 1
    N_TenEMinus6 = 2
    N_TenEMinus7 = 3

class DataTypes(Enum):
    NotSet = 0
    Boolean = 1
    Integer = 2
    IntegerArray = 3
    IntegerMatrix = 4
    Float = 5
    FloatArray = 6
    FloatMatrix = 7
    Double = 8
    DoubleArray = 9
    DoubleMatrix = 10
    String = 11
    StringArray = 12
    StringMatrix = 13
    ByteArray = 14
    Dictionary = 15
    Serializable = 16
    File = 17

class EntryCompressionModes(Enum):
    Auto = 0
    On = 1
    Off = 2

class LensShape(Enum):
    Unknown = 0
    Equi = 1
    Bi = 2
    Plano = 3
    Meniscus = 4

class LensType(Enum):
    Other = 0
    Spherical = 1
    GRIN = 2
    Aspheric = 3
    Toroidal = 4

class QuickAdjustCriterion(Enum):
    SpotSizeRadial = 0
    SpotSizeXOnly = 1
    SpotSizeYOnly = 2
    AngularRadial = 3
    AngularXOnly = 4
    AngularYOnly = 5

class QuickAdjustType(Enum):
    Radius = 0
    Thickness = 1

class QuickFocusCriterion(Enum):
    SpotSizeRadial = 0
    SpotSizeXOnly = 1
    SpotSizeYOnly = 2
    RMSWavefront = 3

class RayPatternType(Enum):
    XYFan = 0
    XFan = 1
    YFan = 2
    Ring = 3
    List = 4
    Random = 5
    Grid = 6
    SolidRing = 7

class ScaleToUnits(Enum):
    Millimeters = 0
    Centimeters = 1
    Inches = 2
    Meters = 3

class SplineSegmentsType(Enum):
    N_016 = 0
    N_032 = 1
    N_064 = 2
    N_128 = 3
    N_256 = 4
    N_512 = 5

class ZemaxFileTypes(Enum):
    Unknown = 0
    LMX = 1
    User = 2
