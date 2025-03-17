"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis import SampleSizes
from zospy.api._ZOSAPI.Analysis.Settings import IAS_

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
    def Field(self) -> IAS_Field: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @property
    def Type(self) -> Types: ...
    @Type.setter
    def Type(self, value: Types) -> None: ...
    @property
    def Sampling(self) -> SampleSizes: ...
    @Sampling.setter
    def Sampling(self, value: SampleSizes) -> None: ...
    @property
    def ShowAs(self) -> FoucaultShowAs: ...
    @ShowAs.setter
    def ShowAs(self, value: FoucaultShowAs) -> None: ...
    @property
    def Knife(self) -> KnifeType: ...
    @Knife.setter
    def Knife(self, value: KnifeType) -> None: ...
    @property
    def Data(self) -> DataType: ...
    @Data.setter
    def Data(self, value: DataType) -> None: ...
    @property
    def RowColumn(self) -> int: ...
    @RowColumn.setter
    def RowColumn(self, value: int) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def Y_Position(self) -> float: ...
    @Y_Position.setter
    def Y_Position(self, value: float) -> None: ...
    @property
    def Decenter_X(self) -> float: ...
    @Decenter_X.setter
    def Decenter_X(self, value: float) -> None: ...
    @property
    def Decenter_Y(self) -> float: ...
    @Decenter_Y.setter
    def Decenter_Y(self, value: float) -> None: ...
    @property
    def Scale_X(self) -> float: ...
    @Scale_X.setter
    def Scale_X(self, value: float) -> None: ...
    @property
    def Scale_Y(self) -> float: ...
    @Scale_Y.setter
    def Scale_Y(self, value: float) -> None: ...
    @property
    def Source(self) -> str: ...
    @Source.setter
    def Source(self, value: str) -> None: ...
    @property
    def SaveBMP(self) -> str: ...
    @SaveBMP.setter
    def SaveBMP(self, value: str) -> None: ...

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
