"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Common import IMatrixData, IVectorData
from zospy.api._ZOSAPI.Tools import HPCRunState, ISystemTool

__all__ = (
    "CriterionComps",
    "CriterionFields",
    "Criterions",
    "IMonteCarloData",
    "IMonteCarloData",
    "IQuickSensitivity",
    "ISensitivityCompensator",
    "ISensitivityCriterionMetadata",
    "ISensitivityCriterionMetadata",
    "ISensitivityData",
    "ISensitivityData",
    "ISensitivityOperandEffect",
    "ISensitivityOperandEffect",
    "ISensitivityOperandMetadata",
    "ITeziData",
    "IToleranceDataViewer",
    "ITolerancing",
    "ITolerancingColumnMetadata",
    "ITolerancingColumnMetadata",
    "ITolerancingHistogram",
    "ITolerancingHistogram",
    "ITolerancingOperandMetadata",
    "ITolerancingParameter",
    "ITolerancingParameter",
    "ITolerancingSummaryStatistics",
    "ITolerancingSummaryStatistics",
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
    OptimizeAll_DLS = 0
    NONSEQOptimizeAll = 0
    ParaxialFocus = 1
    NONSEQNone = 1
    NONSEQOptimizeAll_OD = 2
    # None = 2
    OptimizeAll_OD = 3

class CriterionFields:
    NONSEQUserDefined = 0
    Y_Symmetric = 0
    XY_Symmetric = 1
    UserDefined = 2

class Criterions:
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

class IMonteCarloData:
    @property
    def Values(self) -> IMatrixData: ...
    def GetMetadata(self, columnIndex: int) -> ITolerancingColumnMetadata: ...

class IQuickSensitivity(ISystemTool):
    @property
    def Configuration(self) -> int: ...
    @property
    def Criterion(self) -> QSCriterions: ...
    @property
    def Field(self) -> CriterionFields: ...
    @property
    def MaxSampling(self) -> int: ...
    @property
    def NumberOfConfigurations(self) -> int: ...
    @property
    def ResultsFile(self) -> str: ...
    @property
    def Sampling(self) -> int: ...
    @property
    def ZTDFile(self) -> str: ...
    def LoadSettings(self, settingsFile: str) -> None: ...
    def ResetSettings(self) -> None: ...
    def SaveSettings(self, settingsFile: str) -> None: ...
    @Configuration.setter
    def Configuration(self, value: int) -> None: ...
    @Criterion.setter
    def Criterion(self, value: QSCriterions) -> None: ...
    @Field.setter
    def Field(self, value: CriterionFields) -> None: ...
    @Sampling.setter
    def Sampling(self, value: int) -> None: ...
    @ZTDFile.setter
    def ZTDFile(self, value: str) -> None: ...
    def ValidateCompensators(self) -> bool: ...

class ISensitivityCompensator(ITolerancingOperandMetadata, ITolerancingColumnMetadata):
    @property
    def Maximum(self) -> float: ...
    @property
    def Mean(self) -> float: ...
    @property
    def Minimum(self) -> float: ...
    @property
    def PopulationStandardDeviation(self) -> float: ...
    @property
    def SampleStandardDeviation(self) -> float: ...

class ISensitivityCriterionMetadata:
    @property
    def Name(self) -> Criterions: ...
    @property
    def NominalValue(self) -> float: ...
    @property
    def NumberOfOperands(self) -> int: ...
    def GetEffectByOperand(self, operandIndex: int) -> ISensitivityOperandEffect: ...

class ISensitivityData:
    @property
    def NumberOfCompensators(self) -> int: ...
    @property
    def NumberOfCriteria(self) -> int: ...
    @property
    def NumberOfResultOperands(self) -> int: ...
    def GetCompensator(self, index: int) -> ISensitivityCompensator: ...
    def GetCriterion(self, index: int) -> ISensitivityCriterionMetadata: ...
    def GetOperand(self, index: int) -> ISensitivityOperandMetadata: ...

class ISensitivityOperandEffect:
    @property
    def EstimatedChangeMaximum(self) -> float: ...
    @property
    def EstimatedChangeMinimum(self) -> float: ...

class ISensitivityOperandMetadata(ITolerancingOperandMetadata, ITolerancingColumnMetadata):
    @property
    def Comment(self) -> str: ...
    @property
    def Maximum(self) -> float: ...
    @property
    def Minimum(self) -> float: ...
    @property
    def NumberOfCriteria(self) -> int: ...
    def GetEffectOnCriterion(self, criterionIndex: int) -> ISensitivityOperandEffect: ...

class ITeziData(ITolerancingOperandMetadata, ITolerancingColumnMetadata):
    @property
    def Coefficients(self) -> IMatrixData: ...

class IToleranceDataViewer(ISystemTool):
    @property
    def FileName(self) -> str: ...
    @property
    def MonteCarloData(self) -> IMonteCarloData: ...
    @property
    def SensitivityData(self) -> ISensitivityData: ...
    @property
    def Summary(self) -> str: ...
    def GetToleranceFiles(self) -> list[str]: ...
    @FileName.setter
    def FileName(self, value: str) -> None: ...
    def UseSystemTolerances(self) -> None: ...

class ITolerancing(ISystemTool):
    def EstimateHPCTime(self) -> bool: ...
    @property
    def BestWorstOutputFolder(self) -> str: ...
    @property
    def Criterion(self) -> Criterions: ...
    @property
    def CriterionComp(self) -> CriterionComps: ...
    @property
    def CriterionCompIndex(self) -> int: ...
    @property
    def CriterionConfiguration(self) -> int: ...
    @property
    def CriterionConfigurationIndex(self) -> int: ...
    @property
    def CriterionCycle(self) -> int: ...
    @property
    def CriterionCycleIndex(self) -> int: ...
    @property
    def CriterionField(self) -> CriterionFields: ...
    @property
    def CriterionFieldIndex(self) -> int: ...
    @property
    def CriterionIndex(self) -> int: ...
    @property
    def CriterionSampling(self) -> int: ...
    @property
    def CriterionSamplingIndex(self) -> int: ...
    @property
    def CriterionScript(self) -> int: ...
    @property
    def CriterionScriptIndex(self) -> int: ...
    @property
    def DisplayShowWorst(self) -> int: ...
    @property
    def DisplayShowWorstIndex(self) -> int: ...
    @property
    def FilePrefix(self) -> str: ...
    @property
    def HPCEstimatedTimeS(self) -> float: ...
    @property
    def HPCHasTimeEstimate(self) -> bool: ...
    @property
    def HPCQueuePosition(self) -> int: ...
    @property
    def HPCRemainingTimeS(self) -> float: ...
    @property
    def HPCState(self) -> HPCRunState: ...
    @property
    def HPCTimeToStartS(self) -> float: ...
    @property
    def IsForceRayAimingUsed(self) -> bool: ...
    @property
    def IsHideAllButWorstUsed(self) -> bool: ...
    @property
    def IsHPCEnabled(self) -> bool: ...
    @property
    def IsOverlayGraphicsUsed(self) -> bool: ...
    @property
    def IsSaveBestWorstUsed(self) -> bool: ...
    @property
    def IsSeperateFieldConfigurationsUsed(self) -> bool: ...
    @property
    def IsShowCompensatorsUsed(self) -> bool: ...
    @property
    def IsShowDescriptionsUsed(self) -> bool: ...
    @property
    def MaximumCriteria(self) -> float: ...
    @property
    def MonteCarloStatistic(self) -> MonteCarloStatistics: ...
    @property
    def MonteCarloStatisticIndex(self) -> int: ...
    @property
    def MTFFrequency(self) -> float: ...
    @property
    def NumberOfCriteria(self) -> int: ...
    @property
    def NumberOfCriterionComps(self) -> int: ...
    @property
    def NumberOfCriterionConfigurations(self) -> int: ...
    @property
    def NumberOfCriterionCycles(self) -> int: ...
    @property
    def NumberOfCriterionFields(self) -> int: ...
    @property
    def NumberOfCriterionSamplings(self) -> int: ...
    @property
    def NumberOfCriterionScripts(self) -> int: ...
    @property
    def NumberOfDisplayShowWorsts(self) -> int: ...
    @property
    def NumberOfMonteCarloStatistics(self) -> int: ...
    @property
    def NumberOfRuns(self) -> int: ...
    @property
    def NumberOfSetupCaches(self) -> int: ...
    @property
    def NumberOfSetupChanges(self) -> int: ...
    @property
    def NumberOfSetupCores(self) -> int: ...
    @property
    def NumberOfSetupModes(self) -> int: ...
    @property
    def NumberOfSetupPolynomials(self) -> int: ...
    @property
    def NumberToSave(self) -> int: ...
    @property
    def OpenDataViewer(self) -> bool: ...
    @property
    def OutputFile(self) -> str: ...
    @property
    def ResultFilename(self) -> str: ...
    @property
    def SaveTolDataFile(self) -> bool: ...
    @property
    def SetupCache(self) -> SetupCaches: ...
    @property
    def SetupCacheIndex(self) -> int: ...
    @property
    def SetupChange(self) -> SetupChanges: ...
    @property
    def SetupChangeIndex(self) -> int: ...
    @property
    def SetupCore(self) -> int: ...
    @property
    def SetupCoreIndex(self) -> int: ...
    @property
    def SetupMode(self) -> SetupModes: ...
    @property
    def SetupModeIndex(self) -> int: ...
    @property
    def SetupPolynomial(self) -> SetupPolynomials: ...
    @property
    def SetupPolynomialsIndex(self) -> int: ...
    @property
    def TolDataFile(self) -> str: ...
    @property
    def UseDataRetention(self) -> bool: ...
    def GetCriterionAt(self, idx: int) -> str: ...
    def GetCriterionCompAt(self, idx: int) -> str: ...
    def GetCriterionConfigurationAt(self, idx: int) -> str: ...
    def GetCriterionCycleAt(self, idx: int) -> str: ...
    def GetCriterionFieldAt(self, idx: int) -> str: ...
    def GetCriterionSampleAt(self, idx: int) -> str: ...
    def GetCriterionScriptAt(self, idx: int) -> str: ...
    def GetDisplayShowWorstAt(self, idx: int) -> str: ...
    def GetMonteCarloStatisticAt(self, idx: int) -> str: ...
    def GetSetupCacheAt(self, idx: int) -> str: ...
    def GetSetupChangeAt(self, idx: int) -> str: ...
    def GetSetupCoreAt(self, idx: int) -> str: ...
    def GetSetupModeAt(self, idx: int) -> str: ...
    def GetSetupPolynomialAt(self, idx: int) -> str: ...
    def Load(self, filename: str) -> bool: ...
    def Reset(self) -> bool: ...
    def Save(self, filename: str) -> bool: ...
    @Criterion.setter
    def Criterion(self, value: Criterions) -> None: ...
    @CriterionComp.setter
    def CriterionComp(self, value: CriterionComps) -> None: ...
    @CriterionCompIndex.setter
    def CriterionCompIndex(self, value: int) -> None: ...
    @CriterionConfiguration.setter
    def CriterionConfiguration(self, value: int) -> None: ...
    @CriterionConfigurationIndex.setter
    def CriterionConfigurationIndex(self, value: int) -> None: ...
    @CriterionCycle.setter
    def CriterionCycle(self, value: int) -> None: ...
    @CriterionCycleIndex.setter
    def CriterionCycleIndex(self, value: int) -> None: ...
    @CriterionField.setter
    def CriterionField(self, value: CriterionFields) -> None: ...
    @CriterionFieldIndex.setter
    def CriterionFieldIndex(self, value: int) -> None: ...
    @CriterionIndex.setter
    def CriterionIndex(self, value: int) -> None: ...
    @CriterionSampling.setter
    def CriterionSampling(self, value: int) -> None: ...
    @CriterionSamplingIndex.setter
    def CriterionSamplingIndex(self, value: int) -> None: ...
    @CriterionScript.setter
    def CriterionScript(self, value: int) -> None: ...
    @CriterionScriptIndex.setter
    def CriterionScriptIndex(self, value: int) -> None: ...
    @DisplayShowWorst.setter
    def DisplayShowWorst(self, value: int) -> None: ...
    @DisplayShowWorstIndex.setter
    def DisplayShowWorstIndex(self, value: int) -> None: ...
    @FilePrefix.setter
    def FilePrefix(self, value: str) -> None: ...
    @IsForceRayAimingUsed.setter
    def IsForceRayAimingUsed(self, value: bool) -> None: ...
    @IsHideAllButWorstUsed.setter
    def IsHideAllButWorstUsed(self, value: bool) -> None: ...
    @IsOverlayGraphicsUsed.setter
    def IsOverlayGraphicsUsed(self, value: bool) -> None: ...
    @IsSaveBestWorstUsed.setter
    def IsSaveBestWorstUsed(self, value: bool) -> None: ...
    @IsSeperateFieldConfigurationsUsed.setter
    def IsSeperateFieldConfigurationsUsed(self, value: bool) -> None: ...
    @IsShowCompensatorsUsed.setter
    def IsShowCompensatorsUsed(self, value: bool) -> None: ...
    @IsShowDescriptionsUsed.setter
    def IsShowDescriptionsUsed(self, value: bool) -> None: ...
    @MaximumCriteria.setter
    def MaximumCriteria(self, value: float) -> None: ...
    @MonteCarloStatistic.setter
    def MonteCarloStatistic(self, value: MonteCarloStatistics) -> None: ...
    @MonteCarloStatisticIndex.setter
    def MonteCarloStatisticIndex(self, value: int) -> None: ...
    @MTFFrequency.setter
    def MTFFrequency(self, value: float) -> None: ...
    @NumberOfRuns.setter
    def NumberOfRuns(self, value: int) -> None: ...
    @NumberToSave.setter
    def NumberToSave(self, value: int) -> None: ...
    @OpenDataViewer.setter
    def OpenDataViewer(self, value: bool) -> None: ...
    @OutputFile.setter
    def OutputFile(self, value: str) -> None: ...
    @SaveTolDataFile.setter
    def SaveTolDataFile(self, value: bool) -> None: ...
    @SetupCache.setter
    def SetupCache(self, value: SetupCaches) -> None: ...
    @SetupCacheIndex.setter
    def SetupCacheIndex(self, value: int) -> None: ...
    @SetupChange.setter
    def SetupChange(self, value: SetupChanges) -> None: ...
    @SetupChangeIndex.setter
    def SetupChangeIndex(self, value: int) -> None: ...
    @SetupCore.setter
    def SetupCore(self, value: int) -> None: ...
    @SetupCoreIndex.setter
    def SetupCoreIndex(self, value: int) -> None: ...
    @SetupMode.setter
    def SetupMode(self, value: SetupModes) -> None: ...
    @SetupModeIndex.setter
    def SetupModeIndex(self, value: int) -> None: ...
    @SetupPolynomial.setter
    def SetupPolynomial(self, value: SetupPolynomials) -> None: ...
    @SetupPolynomialsIndex.setter
    def SetupPolynomialsIndex(self, value: int) -> None: ...
    @TolDataFile.setter
    def TolDataFile(self, value: str) -> None: ...
    @UseDataRetention.setter
    def UseDataRetention(self, value: bool) -> None: ...
    def SetPartialMCTMode(self) -> None: ...

class ITolerancingColumnMetadata:
    def AsTeziData(self) -> ITeziData: ...
    @property
    def IsOperand(self) -> bool: ...
    @property
    def Name(self) -> TolerancingColumnName: ...
    @property
    def NumberOfParameters(self) -> int: ...
    @property
    def SummaryStatistics(self) -> ITolerancingSummaryStatistics: ...
    def GetOperandType(self) -> TolerancingOperand: ...
    def GetParameter(self, index: int) -> ITolerancingParameter: ...

class ITolerancingHistogram:
    @property
    def BinCounts(self) -> IVectorData: ...
    @property
    def BinValues(self) -> IVectorData: ...
    @property
    def NumberOfBins(self) -> int: ...
    @property
    def Overflow(self) -> float: ...
    @property
    def Underflow(self) -> float: ...

class ITolerancingOperandMetadata(ITolerancingColumnMetadata):
    @property
    def OperandType(self) -> TolerancingOperand: ...

class ITolerancingParameter:
    @property
    def DoubleValue(self) -> float: ...
    @property
    def IntValue(self) -> int: ...
    @property
    def IsDouble(self) -> bool: ...
    @property
    def IsInt(self) -> bool: ...
    @property
    def IsString(self) -> bool: ...
    @property
    def Name(self) -> TolerancingParameterName: ...
    @property
    def StringValue(self) -> str: ...

class ITolerancingSummaryStatistics:
    @property
    def Histogram(self) -> ITolerancingHistogram: ...
    @property
    def Maximum(self) -> float: ...
    @property
    def Mean(self) -> float: ...
    @property
    def Minimum(self) -> float: ...
    @property
    def PopulationStandardDeviation(self) -> float: ...
    @property
    def SampleError(self) -> float: ...
    @property
    def SampleSize(self) -> int: ...
    @property
    def SampleStandardDeviation(self) -> float: ...
    @property
    def Variance(self) -> float: ...

class MonteCarloStatistics:
    Normal = 0
    Uniform = 1
    Parabolic = 2

class QSCriterions:
    RMSSpotRadius = 0
    RMSSpotX = 1
    RMSSpotY = 2
    RMSWavefront = 3
    BoresightError = 4
    RMSAngularRadius = 5
    RMSAngularX = 6
    RMSAngularY = 7

class SetupCaches:
    RecomputeAll = 0
    RecomputeChanged = 1
    UsePolynomial = 2

class SetupChanges:
    LinearDifference = 0
    RSSDifference = 1

class SetupModes:
    Sensitivity = 0
    InverseLimit = 1
    InverseIncrement = 2
    SkipSensitivity = 3

class SetupPolynomials:
    # None = 0
    ThreeMinusTerm = 1
    FiveMinusTerm = 2

class TolerancingColumnName:
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

class TolerancingOperand:
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

class TolerancingParameterName:
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