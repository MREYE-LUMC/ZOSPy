"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Common import ZemaxColor
from zospy.api._ZOSAPI.Editors import IEditor, IEditorCell, IEditorRow

__all__ = ("IMCERow", "IMultiConfigEditor", "MultiConfigOperandType")

class IMCERow(IEditorRow):
    def AvailableConfigOperandTypes(self) -> list[MultiConfigOperandType]: ...
    def ChangeType(self, type: MultiConfigOperandType) -> bool: ...
    @property
    def IsActive(self) -> bool: ...
    @property
    def OperandNumber(self) -> int: ...
    @property
    def Param1(self) -> int: ...
    @property
    def Param1Enabled(self) -> bool: ...
    @property
    def Param2(self) -> int: ...
    @property
    def Param2Enabled(self) -> bool: ...
    @property
    def Param3(self) -> int: ...
    @property
    def Param3Enabled(self) -> bool: ...
    @property
    def RowColor(self) -> ZemaxColor: ...
    @property
    def Type(self) -> MultiConfigOperandType: ...
    @property
    def TypeName(self) -> str: ...
    def GetOperandCell(self, configuration: int) -> IEditorCell: ...
    @Param1.setter
    def Param1(self, value: int) -> None: ...
    @Param2.setter
    def Param2(self, value: int) -> None: ...
    @Param3.setter
    def Param3(self, value: int) -> None: ...
    @RowColor.setter
    def RowColor(self, value: ZemaxColor) -> None: ...

class IMultiConfigEditor(IEditor):
    def AddConfiguration(self, withPickups: bool) -> bool: ...
    def AddOperand(self) -> IMCERow: ...
    def CopyOperands(self, fromOperandNumber: int, NumberOfOperands: int, toOperandNumber: int) -> int: ...
    def CopyOperandsFrom(
        self, fromEditor: IMultiConfigEditor, fromOperandNumber: int, NumberOfOperands: int, toOperandNumber: int
    ) -> int: ...
    def DeleteAllConfigurations(self) -> bool: ...
    def DeleteConfiguration(self, ConfigurationNumber: int) -> bool: ...
    @property
    def CurrentConfiguration(self) -> int: ...
    @property
    def FirstConfiguration(self) -> int: ...
    @property
    def LastConfiguration(self) -> int: ...
    @property
    def NumberOfConfigurations(self) -> int: ...
    @property
    def NumberOfOperands(self) -> int: ...
    @property
    def RowToOperandOffset(self) -> int: ...
    def GetOperandAt(self, OperandNumber: int) -> IMCERow: ...
    def HideMCE(self) -> None: ...
    def InsertConfiguration(self, ConfigurationNumber: int, withPickups: bool) -> bool: ...
    def InsertNewOperandAt(self, OperandNumber: int) -> IMCERow: ...
    def MakeSingleConfiguration(self) -> None: ...
    def MakeSingleConfigurationOpt(self, deleteMFEOperands: bool) -> None: ...
    def NextConfiguration(self) -> bool: ...
    def PrevConfiguration(self) -> bool: ...
    def RemoveOperandAt(self, OperandNumber: int) -> bool: ...
    def RemoveOperandsAt(self, OperandNumber: int, numOperands: int) -> int: ...
    def RunTool_MakeThermal(
        self,
        existingConfigurationIndex: int,
        numberOfThemalConfigs: int,
        minTemp: float,
        maxTemp: float,
        sortBySurface: bool,
    ) -> None: ...
    def SetCurrentConfiguration(self, ConfigurationNumber: int) -> bool: ...
    def ShowMCE(self) -> bool: ...

class MultiConfigOperandType:
    MOFF = 0
    AICN = 1
    AFOC = 2
    APDF = 3
    APDT = 4
    APDX = 5
    APDY = 6
    APER = 7
    APMN = 8
    APMX = 9
    APTP = 10
    CADX = 11
    CADY = 12
    CAOR = 13
    CATX = 14
    CATY = 15
    CATZ = 16
    CBDX = 17
    CBDY = 18
    CBOR = 19
    CBTX = 20
    CBTY = 21
    CBTZ = 22
    CONN = 23
    COTN = 24
    CPCN = 25
    CROR = 26
    CRSR = 27
    CRVT = 28
    CSP1 = 29
    CSP2 = 30
    CWGT = 31
    EDVA = 32
    FLTP = 33
    FLWT = 34
    FVAN = 35
    FVCX = 36
    FVCY = 37
    FVDX = 38
    FVDY = 39
    GCRS = 40
    GLSS = 41
    GPEX = 42
    GPEY = 43
    GPIU = 44
    GPJX = 45
    GPJY = 46
    GPPX = 47
    GPPY = 48
    GQPO = 49
    HOLD = 50
    IGNM = 51
    IGNR = 52
    LTTL = 53
    MABB = 54
    MCOM = 55
    MDPG = 56
    MIND = 57
    MTFU = 58
    NCOM = 59
    NCOT = 60
    NGLS = 61
    NPAR = 62
    NPOS = 63
    NPRO = 64
    PAR1 = 65
    PAR2 = 66
    PAR3 = 67
    PAR4 = 68
    PAR5 = 69
    PAR6 = 70
    PAR7 = 71
    PAR8 = 72
    PRAM = 73
    PRES = 74
    PRWV = 75
    PSCX = 76
    PSCY = 77
    PSHX = 78
    PSHY = 79
    PSHZ = 80
    PSP1 = 81
    PSP2 = 82
    PSP3 = 83
    PUCN = 84
    PXAR = 85
    RAAM = 86
    SATP = 87
    SDIA = 88
    SDRW = 89
    STPS = 90
    SWCN = 91
    TCEX = 92
    TELE = 93
    TEMP = 94
    THIC = 95
    TSP1 = 96
    TSP2 = 97
    TSP3 = 98
    UDAF = 99
    WAVE = 100
    WLWT = 101
    XFIE = 102
    YFIE = 103
    OPDR = 104
    SRTS = 105
    MCHI = 106
    IGTO = 107
    FTAN = 108
    FCMM = 109
    CHZN = 110
    MCSD = 111
