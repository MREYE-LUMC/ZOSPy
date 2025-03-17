"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis import ShowAs
from zospy.api._ZOSAPI.Analysis.Settings import IAS_
from zospy.api._ZOSAPI.Analysis.Settings.RMS.RMSField import DataType
from zospy.api._ZOSAPI.Analysis.Settings.RMS.RMSFieldMap import DataType

from . import RMSField, RMSFieldMap

__all__ = (
    "RMSField",
    "RMSFieldMap",
    "FieldDensities",
    "FocusDensities",
    "IAS_RMSField",
    "IAS_RMSFieldMap",
    "IAS_RMSFocus",
    "IAS_RMSLambdaDiagram",
    "Method",
    "Orientations",
    "RayDensities",
    "ReferTo",
    "WaveDensities",
)

class FieldDensities:
    FieldDens_5 = 1
    FieldDens_10 = 2
    FieldDens_15 = 3
    FieldDens_20 = 4
    FieldDens_25 = 5
    FieldDens_30 = 6
    FieldDens_35 = 7
    FieldDens_40 = 8
    FieldDens_45 = 9
    FieldDens_50 = 10
    FieldDens_55 = 11
    FieldDens_60 = 12
    FieldDens_65 = 13
    FieldDens_70 = 14
    FieldDens_75 = 15
    FieldDens_80 = 16
    FieldDens_85 = 17
    FieldDens_90 = 18
    FieldDens_95 = 19
    FieldDens_100 = 20

class FocusDensities:
    FocusDens_5 = 1
    FocusDens_10 = 2
    FocusDens_15 = 3
    FocusDens_20 = 4
    FocusDens_25 = 5
    FocusDens_30 = 6
    FocusDens_35 = 7
    FocusDens_40 = 8
    FocusDens_45 = 9
    FocusDens_50 = 10
    FocusDens_55 = 11
    FocusDens_60 = 12
    FocusDens_65 = 13
    FocusDens_70 = 14
    FocusDens_75 = 15
    FocusDens_80 = 16
    FocusDens_85 = 17
    FocusDens_90 = 18
    FocusDens_95 = 19
    FocusDens_100 = 20

class IAS_RMSField(IAS_):
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @property
    def Data(self) -> DataType: ...
    @Data.setter
    def Data(self, value: DataType) -> None: ...
    @property
    def FieldDensity(self) -> FieldDensities: ...
    @FieldDensity.setter
    def FieldDensity(self, value: FieldDensities) -> None: ...
    @property
    def RayDensity(self) -> RayDensities: ...
    @RayDensity.setter
    def RayDensity(self, value: RayDensities) -> None: ...
    @property
    def ReferTo(self) -> ReferTo: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferTo) -> None: ...
    @property
    def Method(self) -> Method: ...
    @Method.setter
    def Method(self, value: Method) -> None: ...
    @property
    def Orientation(self) -> Orientations: ...
    @Orientation.setter
    def Orientation(self, value: Orientations) -> None: ...
    @property
    def ShowDiffractionLimit(self) -> bool: ...
    @ShowDiffractionLimit.setter
    def ShowDiffractionLimit(self, value: bool) -> None: ...
    @property
    def UseDashes(self) -> bool: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def RemoveVignettingFactors(self) -> bool: ...
    @RemoveVignettingFactors.setter
    def RemoveVignettingFactors(self, value: bool) -> None: ...
    @property
    def PlotScale(self) -> float: ...
    @PlotScale.setter
    def PlotScale(self, value: float) -> None: ...

class IAS_RMSFieldMap(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @property
    def Data(self) -> DataType: ...
    @Data.setter
    def Data(self, value: DataType) -> None: ...
    @property
    def MethodType(self) -> Method: ...
    @MethodType.setter
    def MethodType(self, value: Method) -> None: ...
    @property
    def RayDensity(self) -> RayDensities: ...
    @RayDensity.setter
    def RayDensity(self, value: RayDensities) -> None: ...
    @property
    def ReferTo(self) -> ReferTo: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferTo) -> None: ...
    @property
    def ShowAs(self) -> ShowAs: ...
    @ShowAs.setter
    def ShowAs(self, value: ShowAs) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def RemoveVignettingFactors(self) -> bool: ...
    @RemoveVignettingFactors.setter
    def RemoveVignettingFactors(self, value: bool) -> None: ...
    @property
    def X_FieldSampling(self) -> int: ...
    @X_FieldSampling.setter
    def X_FieldSampling(self, value: int) -> None: ...
    @property
    def Y_FieldSampling(self) -> int: ...
    @Y_FieldSampling.setter
    def Y_FieldSampling(self, value: int) -> None: ...
    @property
    def X_FieldSize(self) -> float: ...
    @X_FieldSize.setter
    def X_FieldSize(self, value: float) -> None: ...
    @property
    def Y_FieldSize(self) -> float: ...
    @Y_FieldSize.setter
    def Y_FieldSize(self, value: float) -> None: ...
    @property
    def PlotScale(self) -> float: ...
    @PlotScale.setter
    def PlotScale(self, value: float) -> None: ...
    @property
    def ContourFormat(self) -> str: ...
    @ContourFormat.setter
    def ContourFormat(self, value: str) -> None: ...

class IAS_RMSFocus(IAS_):
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @property
    def RayDensity(self) -> RayDensities: ...
    @RayDensity.setter
    def RayDensity(self, value: RayDensities) -> None: ...
    @property
    def FocusDensity(self) -> FocusDensities: ...
    @FocusDensity.setter
    def FocusDensity(self, value: FocusDensities) -> None: ...
    @property
    def Data(self) -> DataType: ...
    @Data.setter
    def Data(self, value: DataType) -> None: ...
    @property
    def ReferTo(self) -> ReferTo: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferTo) -> None: ...
    @property
    def Method(self) -> Method: ...
    @Method.setter
    def Method(self, value: Method) -> None: ...
    @property
    def UseDashes(self) -> bool: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @property
    def ShowDiffractionLimit(self) -> bool: ...
    @ShowDiffractionLimit.setter
    def ShowDiffractionLimit(self, value: bool) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def PlotScale(self) -> float: ...
    @PlotScale.setter
    def PlotScale(self, value: float) -> None: ...
    @property
    def MinimumFocus(self) -> float: ...
    @MinimumFocus.setter
    def MinimumFocus(self, value: float) -> None: ...
    @property
    def MaximumFocus(self) -> float: ...
    @MaximumFocus.setter
    def MaximumFocus(self, value: float) -> None: ...

class IAS_RMSLambdaDiagram(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def RayDensity(self) -> RayDensities: ...
    @RayDensity.setter
    def RayDensity(self, value: RayDensities) -> None: ...
    @property
    def WaveDensity(self) -> WaveDensities: ...
    @WaveDensity.setter
    def WaveDensity(self, value: WaveDensities) -> None: ...
    @property
    def Data(self) -> DataType: ...
    @Data.setter
    def Data(self, value: DataType) -> None: ...
    @property
    def ReferTo(self) -> ReferTo: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferTo) -> None: ...
    @property
    def Method(self) -> Method: ...
    @Method.setter
    def Method(self, value: Method) -> None: ...
    @property
    def UseDashes(self) -> bool: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @property
    def ShowDiffractionLimit(self) -> bool: ...
    @ShowDiffractionLimit.setter
    def ShowDiffractionLimit(self, value: bool) -> None: ...
    @property
    def UsePolarization(self) -> bool: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...
    @property
    def PlotScale(self) -> float: ...
    @PlotScale.setter
    def PlotScale(self, value: float) -> None: ...

class Method:
    GaussQuad = 0
    RectArray = 1

class Orientations:
    Plus_Y = 0
    Minus_Y = 1
    Plus_X = 2
    Minus_X = 3

class RayDensities:
    RayDens_1 = 1
    RayDens_32x32 = 1
    RayDens_64x64 = 2
    RayDens_2 = 2
    RayDens_128x128 = 3
    RayDens_3 = 3
    RayDens_256x256 = 4
    RayDens_4 = 4
    RayDens_5 = 5
    RayDens_512x512 = 5
    RayDens_1024x1024 = 6
    RayDens_6 = 6
    RayDens_2048x2048 = 7
    RayDens_7 = 7
    RayDens_4096x4096 = 8
    RayDens_8 = 8
    RayDens_8192x8192 = 9
    RayDens_9 = 9
    RayDens_10 = 10
    RayDens_16384x16384 = 10
    RayDens_11 = 11
    RayDens_12 = 12
    RayDens_13 = 13
    RayDens_14 = 14
    RayDens_15 = 15
    RayDens_16 = 16
    RayDens_17 = 17
    RayDens_18 = 18
    RayDens_19 = 19
    RayDens_20 = 20

class ReferTo:
    ChiefRay = 0
    Centroid = 1

class WaveDensities:
    WaveDens_5 = 1
    WaveDens_10 = 2
    WaveDens_15 = 3
    WaveDens_20 = 4
    WaveDens_25 = 5
    WaveDens_30 = 6
    WaveDens_35 = 7
    WaveDens_40 = 8
    WaveDens_45 = 9
    WaveDens_50 = 10
    WaveDens_55 = 11
    WaveDens_60 = 12
    WaveDens_65 = 13
    WaveDens_70 = 14
    WaveDens_75 = 15
    WaveDens_80 = 16
    WaveDens_85 = 17
    WaveDens_90 = 18
    WaveDens_95 = 19
    WaveDens_100 = 20
