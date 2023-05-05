"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis import SampleSizes
from zospy.api._ZOSAPI.Analysis.Settings import IAS_, IAS_Field, IAS_Wavelength

__all__ = ("DataType", "FoucaultShowAs", "IAS_Foucault", "KnifeType", "Types")

class DataType:
    Computed = 0
    Reference = 1
    Difference = 2

class FoucaultShowAs:
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    X_CrossSection = 6
    Y_CrossSection = 7

class IAS_Foucault(IAS_):
    @property
    def Data(self) -> DataType: ...
    @property
    def Decenter_X(self) -> float: ...
    @property
    def Decenter_Y(self) -> float: ...
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def Knife(self) -> KnifeType: ...
    @property
    def RowColumn(self) -> int: ...
    @property
    def Sampling(self) -> SampleSizes: ...
    @property
    def SaveBMP(self) -> str: ...
    @property
    def Scale_X(self) -> float: ...
    @property
    def Scale_Y(self) -> float: ...
    @property
    def ShowAs(self) -> FoucaultShowAs: ...
    @property
    def Source(self) -> str: ...
    @property
    def Type(self) -> Types: ...
    @property
    def UsePolarization(self) -> bool: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @property
    def Y_Position(self) -> float: ...
    @Data.setter
    def Data(self, value: DataType) -> None: ...
    @Decenter_X.setter
    def Decenter_X(self, value: float) -> None: ...
    @Decenter_Y.setter
    def Decenter_Y(self, value: float) -> None: ...
    @Knife.setter
    def Knife(self, value: KnifeType) -> None: ...
    @RowColumn.setter
    def RowColumn(self, value: int) -> None: ...
    @Sampling.setter
    def Sampling(self, value: SampleSizes) -> None: ...
    @SaveBMP.setter
    def SaveBMP(self, value: str) -> None: ...
    @Scale_X.setter
    def Scale_X(self, value: float) -> None: ...
    @Scale_Y.setter
    def Scale_Y(self, value: float) -> None: ...
    @ShowAs.setter
    def ShowAs(self, value: FoucaultShowAs) -> None: ...
    @Source.setter
    def Source(self, value: str) -> None: ...
    @Type.setter
    def Type(self, value: Types) -> None: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @Y_Position.setter
    def Y_Position(self, value: float) -> None: ...

class KnifeType:
    Horiz_Above = 0
    Horiz_Below = 1
    Vert_Right = 2
    Vert_Left = 3

class Types:
    Linear = 0
    Log_Minus_3 = 1
    Log_Minus_6 = 2
    Log_Minus_9 = 3
    Log_Minus_12 = 4
    Log_Minus_15 = 5
    Log_Minus_18 = 6
