"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

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

class ACISExportVersion:
    Current: ACISExportVersion = None
    V25: ACISExportVersion = None
    V26: ACISExportVersion = None
    V27: ACISExportVersion = None
    V28: ACISExportVersion = None
    V29: ACISExportVersion = None
    V30: ACISExportVersion = None

class ArchiveFileStatus:
    Okay: ArchiveFileStatus = None
    InvalidVersion: ArchiveFileStatus = None
    InvalidFile: ArchiveFileStatus = None
    UnableToOpen: ArchiveFileStatus = None

class CADAngularToleranceType:
    Low: CADAngularToleranceType = None
    Medium: CADAngularToleranceType = None
    High: CADAngularToleranceType = None
    Presentation: CADAngularToleranceType = None

class CADFileType:
    IGES: CADFileType = None
    STEP: CADFileType = None
    SAT: CADFileType = None
    STL: CADFileType = None
    SAB: CADFileType = None
    ASAT: CADFileType = None
    ASAB: CADFileType = None
    MODEL: CADFileType = None
    CATPART: CADFileType = None
    CATPRODUCT: CADFileType = None
    XCGM: CADFileType = None
    ZMO: CADFileType = None
    XT: CADFileType = None
    XB: CADFileType = None
    PRC: CADFileType = None
    JT: CADFileType = None
    N3MF: CADFileType = None
    U3D: CADFileType = None
    VRML: CADFileType = None
    OBJ: CADFileType = None

class CADToleranceType:
    N_TenEMinus4: CADToleranceType = None
    N_TenEMinus5: CADToleranceType = None
    N_TenEMinus6: CADToleranceType = None
    N_TenEMinus7: CADToleranceType = None

class DataTypes:
    NotSet: DataTypes = None
    Boolean: DataTypes = None
    Integer: DataTypes = None
    IntegerArray: DataTypes = None
    IntegerMatrix: DataTypes = None
    Float: DataTypes = None
    FloatArray: DataTypes = None
    FloatMatrix: DataTypes = None
    Double: DataTypes = None
    DoubleArray: DataTypes = None
    DoubleMatrix: DataTypes = None
    String: DataTypes = None
    StringArray: DataTypes = None
    StringMatrix: DataTypes = None
    ByteArray: DataTypes = None
    Dictionary: DataTypes = None
    Serializable: DataTypes = None
    File: DataTypes = None

class EntryCompressionModes:
    Auto: EntryCompressionModes = None
    On: EntryCompressionModes = None
    Off: EntryCompressionModes = None

class LensShape:
    Unknown: LensShape = None
    Equi: LensShape = None
    Bi: LensShape = None
    Plano: LensShape = None
    Meniscus: LensShape = None

class LensType:
    Other: LensType = None
    Spherical: LensType = None
    GRIN: LensType = None
    Aspheric: LensType = None
    Toroidal: LensType = None

class QuickAdjustCriterion:
    SpotSizeRadial: QuickAdjustCriterion = None
    SpotSizeXOnly: QuickAdjustCriterion = None
    SpotSizeYOnly: QuickAdjustCriterion = None
    AngularRadial: QuickAdjustCriterion = None
    AngularXOnly: QuickAdjustCriterion = None
    AngularYOnly: QuickAdjustCriterion = None

class QuickAdjustType:
    Radius: QuickAdjustType = None
    Thickness: QuickAdjustType = None

class QuickFocusCriterion:
    SpotSizeRadial: QuickFocusCriterion = None
    SpotSizeXOnly: QuickFocusCriterion = None
    SpotSizeYOnly: QuickFocusCriterion = None
    RMSWavefront: QuickFocusCriterion = None

class RayPatternType:
    XYFan: RayPatternType = None
    XFan: RayPatternType = None
    YFan: RayPatternType = None
    Ring: RayPatternType = None
    List: RayPatternType = None
    Random: RayPatternType = None
    Grid: RayPatternType = None
    SolidRing: RayPatternType = None

class ScaleToUnits:
    Millimeters: ScaleToUnits = None
    Centimeters: ScaleToUnits = None
    Inches: ScaleToUnits = None
    Meters: ScaleToUnits = None

class SplineSegmentsType:
    N_016: SplineSegmentsType = None
    N_032: SplineSegmentsType = None
    N_064: SplineSegmentsType = None
    N_128: SplineSegmentsType = None
    N_256: SplineSegmentsType = None
    N_512: SplineSegmentsType = None

class ZemaxFileTypes:
    Unknown: ZemaxFileTypes = None
    LMX: ZemaxFileTypes = None
    User: ZemaxFileTypes = None
