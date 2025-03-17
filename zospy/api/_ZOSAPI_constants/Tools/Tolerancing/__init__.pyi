"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = (
    "CriterionComps",
    "CriterionFields",
    "Criterions",
    "MonteCarloStatistics",
    "QSCriterions",
    "SetupCaches",
    "SetupChanges",
    "SetupModes",
    "SetupPolynomials",
    "TolerancingColumnName",
    "TolerancingOperand",
    "TolerancingParameterName",
)

class CriterionComps:
    OptimizeAll_DLS: CriterionComps = None
    NONSEQOptimizeAll: CriterionComps = None
    ParaxialFocus: CriterionComps = None
    NONSEQNone: CriterionComps = None
    NONSEQOptimizeAll_OD: CriterionComps = None
    None_: CriterionComps = None
    OptimizeAll_OD: CriterionComps = None

class CriterionFields:
    NONSEQUserDefined: CriterionFields = None
    Y_Symmetric: CriterionFields = None
    XY_Symmetric: CriterionFields = None
    UserDefined: CriterionFields = None

class Criterions:
    NONSEQMeritFunction: Criterions = None
    RMSSpotRadius: Criterions = None
    RMSSpotX: Criterions = None
    NONSEQUserScript: Criterions = None
    RMSSpotY: Criterions = None
    RMSWavefront: Criterions = None
    MeritFunction: Criterions = None
    GeometricMTFAverage: Criterions = None
    GeometricMTFTan: Criterions = None
    GeometricMTFSag: Criterions = None
    DiffMTFAverage: Criterions = None
    DiffMTFTan: Criterions = None
    DiffMTFSag: Criterions = None
    BoresightError: Criterions = None
    RMSAngularRadius: Criterions = None
    RMSAngularX: Criterions = None
    RMSAngularY: Criterions = None
    UserScript: Criterions = None

class MonteCarloStatistics:
    Normal: MonteCarloStatistics = None
    Uniform: MonteCarloStatistics = None
    Parabolic: MonteCarloStatistics = None

class QSCriterions:
    RMSSpotRadius: QSCriterions = None
    RMSSpotX: QSCriterions = None
    RMSSpotY: QSCriterions = None
    RMSWavefront: QSCriterions = None
    BoresightError: QSCriterions = None
    RMSAngularRadius: QSCriterions = None
    RMSAngularX: QSCriterions = None
    RMSAngularY: QSCriterions = None

class SetupCaches:
    RecomputeAll: SetupCaches = None
    RecomputeChanged: SetupCaches = None
    UsePolynomial: SetupCaches = None

class SetupChanges:
    LinearDifference: SetupChanges = None
    RSSDifference: SetupChanges = None

class SetupModes:
    Sensitivity: SetupModes = None
    InverseLimit: SetupModes = None
    InverseIncrement: SetupModes = None
    SkipSensitivity: SetupModes = None

class SetupPolynomials:
    None_: SetupPolynomials = None
    ThreeMinusTerm: SetupPolynomials = None
    FiveMinusTerm: SetupPolynomials = None

class TolerancingColumnName:
    UserMeritFunction: TolerancingColumnName = None
    UserScript: TolerancingColumnName = None
    RmsSpotRadius: TolerancingColumnName = None
    RmsSpotX: TolerancingColumnName = None
    RmsSpotY: TolerancingColumnName = None
    RmsWavefrontError: TolerancingColumnName = None
    MtfGeometricAverage: TolerancingColumnName = None
    MtfGeometricTangential: TolerancingColumnName = None
    MtfGeometricSaggital: TolerancingColumnName = None
    MtfDiffractionAverage: TolerancingColumnName = None
    MtfDiffractionTangential: TolerancingColumnName = None
    MtfDiffractionSagittal: TolerancingColumnName = None
    BoresightError: TolerancingColumnName = None
    RmsAngularRadius: TolerancingColumnName = None
    RmsAngularX: TolerancingColumnName = None
    RmsAngularY: TolerancingColumnName = None
    BackFocusChange: TolerancingColumnName = None
    Unknown: TolerancingColumnName = None

class TolerancingOperand:
    NULL: TolerancingOperand = None
    TRAD: TolerancingOperand = None
    TCUR: TolerancingOperand = None
    TFRN: TolerancingOperand = None
    TTHI: TolerancingOperand = None
    TCON: TolerancingOperand = None
    TSDI: TolerancingOperand = None
    TSDX: TolerancingOperand = None
    TSDY: TolerancingOperand = None
    TSTX: TolerancingOperand = None
    TSTY: TolerancingOperand = None
    TIRX: TolerancingOperand = None
    TIRY: TolerancingOperand = None
    TIRR: TolerancingOperand = None
    TPAR: TolerancingOperand = None
    TEDV: TolerancingOperand = None
    TEDX: TolerancingOperand = None
    TEDY: TolerancingOperand = None
    TETX: TolerancingOperand = None
    TETY: TolerancingOperand = None
    TETZ: TolerancingOperand = None
    TUDX: TolerancingOperand = None
    TUDY: TolerancingOperand = None
    TUTX: TolerancingOperand = None
    TUTY: TolerancingOperand = None
    TUTZ: TolerancingOperand = None
    TIND: TolerancingOperand = None
    TABB: TolerancingOperand = None
    TEXI: TolerancingOperand = None
    SAVE: TolerancingOperand = None
    COMP: TolerancingOperand = None
    CPAR: TolerancingOperand = None
    CEDV: TolerancingOperand = None
    CMCO: TolerancingOperand = None
    STAT: TolerancingOperand = None
    TWAV: TolerancingOperand = None
    TNPS: TolerancingOperand = None
    TNPA: TolerancingOperand = None
    TMCO: TolerancingOperand = None
    TEZI: TolerancingOperand = None
    TCMU: TolerancingOperand = None
    SEED: TolerancingOperand = None
    COMM: TolerancingOperand = None
    TPAI: TolerancingOperand = None
    TCIO: TolerancingOperand = None
    TCEO: TolerancingOperand = None
    TNMA: TolerancingOperand = None
    CNPA: TolerancingOperand = None
    CNPS: TolerancingOperand = None
    TRLX: TolerancingOperand = None
    TRLY: TolerancingOperand = None
    TRLR: TolerancingOperand = None
    TARX: TolerancingOperand = None
    TARY: TolerancingOperand = None
    TARR: TolerancingOperand = None
    TEDR: TolerancingOperand = None
    TSDR: TolerancingOperand = None
    ISOA: TolerancingOperand = None
    ISOB: TolerancingOperand = None
    ISOC: TolerancingOperand = None
    ISOD: TolerancingOperand = None
    MPVT: TolerancingOperand = None
    Unknown: TolerancingOperand = None

class TolerancingParameterName:
    CompensatorSetting: TolerancingParameterName = None
    ConfigurationNumber: TolerancingParameterName = None
    CommentField: TolerancingParameterName = None
    NominalValue: TolerancingParameterName = None
    Surface: TolerancingParameterName = None
    MinimumValue: TolerancingParameterName = None
    MaximumValue: TolerancingParameterName = None
    Surface1: TolerancingParameterName = None
    Surface2: TolerancingParameterName = None
    AdjustSurface: TolerancingParameterName = None
    ParameterNumber: TolerancingParameterName = None
    Layer: TolerancingParameterName = None
    MaximumNumber: TolerancingParameterName = None
    MinimumNumber: TolerancingParameterName = None
    Code: TolerancingParameterName = None
    RowNumber: TolerancingParameterName = None
    ConfigurationParameter: TolerancingParameterName = None
    Object: TolerancingParameterName = None
    Data: TolerancingParameterName = None
    FieldNumber: TolerancingParameterName = None
    SamplingSetting: TolerancingParameterName = None
    Units: TolerancingParameterName = None
    Statistics: TolerancingParameterName = None
    PivotPointOption: TolerancingParameterName = None
    FieldSetting: TolerancingParameterName = None
    TdeRowNumber: TolerancingParameterName = None
    Undefined: TolerancingParameterName = None
