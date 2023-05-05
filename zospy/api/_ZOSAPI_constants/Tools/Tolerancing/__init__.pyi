"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

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

class CriterionComps(Enum):
    OptimizeAll_DLS = 0
    NONSEQOptimizeAll = 0
    ParaxialFocus = 1
    NONSEQNone = 1
    NONSEQOptimizeAll_OD = 2
    None_ = 2
    OptimizeAll_OD = 3

class CriterionFields(Enum):
    NONSEQUserDefined = 0
    Y_Symmetric = 0
    XY_Symmetric = 1
    UserDefined = 2

class Criterions(Enum):
    NONSEQMeritFunction = 0
    RMSSpotRadius = 0
    RMSSpotX = 1
    NONSEQUserScript = 1
    RMSSpotY = 2
    RMSWavefront = 3
    MeritFunction = 4
    GeometricMTFAverage = 5
    GeometricMTFTan = 6
    GeometricMTFSag = 7
    DiffMTFAverage = 8
    DiffMTFTan = 9
    DiffMTFSag = 10
    BoresightError = 11
    RMSAngularRadius = 12
    RMSAngularX = 13
    RMSAngularY = 14
    UserScript = 15

class MonteCarloStatistics(Enum):
    Normal = 0
    Uniform = 1
    Parabolic = 2

class QSCriterions(Enum):
    RMSSpotRadius = 0
    RMSSpotX = 1
    RMSSpotY = 2
    RMSWavefront = 3
    BoresightError = 4
    RMSAngularRadius = 5
    RMSAngularX = 6
    RMSAngularY = 7

class SetupCaches(Enum):
    RecomputeAll = 0
    RecomputeChanged = 1
    UsePolynomial = 2

class SetupChanges(Enum):
    LinearDifference = 0
    RSSDifference = 1

class SetupModes(Enum):
    Sensitivity = 0
    InverseLimit = 1
    InverseIncrement = 2
    SkipSensitivity = 3

class SetupPolynomials(Enum):
    None_ = 0
    ThreeMinusTerm = 1
    FiveMinusTerm = 2

class TolerancingColumnName(Enum):
    UserMeritFunction = 11959
    UserScript = 11960
    RmsSpotRadius = 11961
    RmsSpotX = 11962
    RmsSpotY = 11963
    RmsWavefrontError = 11964
    MtfGeometricAverage = 11965
    MtfGeometricTangential = 11966
    MtfGeometricSaggital = 11967
    MtfDiffractionAverage = 11968
    MtfDiffractionTangential = 11969
    MtfDiffractionSagittal = 11970
    BoresightError = 11971
    RmsAngularRadius = 11972
    RmsAngularX = 11973
    RmsAngularY = 11974
    BackFocusChange = 75417
    Unknown = -1

class TolerancingOperand(Enum):
    NULL = 0
    TRAD = 1
    TCUR = 2
    TFRN = 3
    TTHI = 4
    TCON = 5
    TSDI = 6
    TSDX = 7
    TSDY = 8
    TSTX = 9
    TSTY = 10
    TIRX = 11
    TIRY = 12
    TIRR = 13
    TPAR = 14
    TEDV = 15
    TEDX = 16
    TEDY = 17
    TETX = 18
    TETY = 19
    TETZ = 20
    TUDX = 21
    TUDY = 22
    TUTX = 23
    TUTY = 24
    TUTZ = 25
    TIND = 26
    TABB = 27
    TEXI = 28
    SAVE = 29
    COMP = 30
    CPAR = 31
    CEDV = 32
    CMCO = 33
    STAT = 34
    TWAV = 35
    TNPS = 36
    TNPA = 37
    TMCO = 38
    TEZI = 39
    TCMU = 40
    SEED = 41
    COMM = 42
    TPAI = 43
    TCIO = 44
    TCEO = 45
    TNMA = 46
    CNPA = 47
    CNPS = 48
    TRLX = 49
    TRLY = 50
    TRLR = 51
    TARX = 52
    TARY = 53
    TARR = 54
    TEDR = 55
    TSDR = 56
    Unknown = -1

class TolerancingParameterName(Enum):
    CompensatorSetting = 11400
    ConfigurationNumber = 16304
    CommentField = 20004
    NominalValue = 20566
    Surface = 20567
    MinimumValue = 20568
    MaximumValue = 20569
    Surface1 = 20570
    Surface2 = 20571
    AdjustSurface = 20572
    ParameterNumber = 20573
    Layer = 20574
    MaximumNumber = 20576
    MinimumNumber = 20577
    Code = 20578
    RowNumber = 20579
    ConfigurationParameter = 20580
    Object = 20585
    Data = 20586
    FieldNumber = 20683
    SamplingSetting = 20694
    FieldSetting = 50027
    TdeRowNumber = 75418
    Undefined = -1
