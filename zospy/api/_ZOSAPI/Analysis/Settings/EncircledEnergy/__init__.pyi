"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis import SampleSizes
from zospy.api._ZOSAPI.Analysis.Settings import (
    IAS_,
    IAS_Field,
    IAS_Surface,
    IAS_Wavelength,
)

__all__ = (
    "EncircledEnergyTypes",
    "ExtendedSourceTypes",
    "GeometricLineEdgeSpreadTypes",
    "IAS_DiffractionEncircledEnergy",
    "IAS_ExtendedSourceEncircledEnergy",
    "IAS_GeometricEncircledEnergy",
    "IAS_GeometricLineEdgeSpread",
    "ReferToTypes",
)

class EncircledEnergyTypes:
    Encircled = 1
    X_Only = 2
    Y_Only = 3
    Ensquared = 4

class ExtendedSourceTypes:
    Encircled = 1
    X_Only = 2
    Y_Only = 3
    Ensquared = 4
    X_Distrib = 5
    Y_Distrib = 6

class GeometricLineEdgeSpreadTypes:
    LineEdge = 1
    Line = 2
    Edge = 3

class IAS_DiffractionEncircledEnergy(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def HuygensDelta(self) -> float: ...
    @property
    def HuygensSample(self) -> SampleSizes: ...
    @property
    def RadiusMaximum(self) -> float: ...
    @property
    def ReferTo(self) -> ReferToTypes: ...
    @property
    def SampleSize(self) -> SampleSizes: ...
    @property
    def ScatterRays(self) -> bool: ...
    @property
    def ShowDiffractionLimit(self) -> bool: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Type(self) -> EncircledEnergyTypes: ...
    @property
    def UseDashes(self) -> bool: ...
    @property
    def UseHuygensPSF(self) -> bool: ...
    @property
    def UsePolarization(self) -> bool: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @HuygensDelta.setter
    def HuygensDelta(self, value: float) -> None: ...
    @HuygensSample.setter
    def HuygensSample(self, value: SampleSizes) -> None: ...
    @RadiusMaximum.setter
    def RadiusMaximum(self, value: float) -> None: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferToTypes) -> None: ...
    @SampleSize.setter
    def SampleSize(self, value: SampleSizes) -> None: ...
    @ScatterRays.setter
    def ScatterRays(self, value: bool) -> None: ...
    @ShowDiffractionLimit.setter
    def ShowDiffractionLimit(self, value: bool) -> None: ...
    @Type.setter
    def Type(self, value: EncircledEnergyTypes) -> None: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @UseHuygensPSF.setter
    def UseHuygensPSF(self, value: bool) -> None: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...

class IAS_ExtendedSourceEncircledEnergy(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def FieldSize(self) -> float: ...
    @property
    def ImageName(self) -> str: ...
    @property
    def MaximumDistance(self) -> float: ...
    @property
    def MultiplyByDiffractionLimit(self) -> bool: ...
    @property
    def RaysX1000(self) -> int: ...
    @property
    def ReferTo(self) -> ReferToTypes: ...
    @property
    def RemoveVignettingFactors(self) -> bool: ...
    @property
    def Rotation(self) -> float: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Type(self) -> ExtendedSourceTypes: ...
    @property
    def UseDashes(self) -> bool: ...
    @property
    def UsePolarization(self) -> bool: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @FieldSize.setter
    def FieldSize(self, value: float) -> None: ...
    @ImageName.setter
    def ImageName(self, value: str) -> None: ...
    @MaximumDistance.setter
    def MaximumDistance(self, value: float) -> None: ...
    @MultiplyByDiffractionLimit.setter
    def MultiplyByDiffractionLimit(self, value: bool) -> None: ...
    @RaysX1000.setter
    def RaysX1000(self, value: int) -> None: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferToTypes) -> None: ...
    @RemoveVignettingFactors.setter
    def RemoveVignettingFactors(self, value: bool) -> None: ...
    @Rotation.setter
    def Rotation(self, value: float) -> None: ...
    @Type.setter
    def Type(self, value: ExtendedSourceTypes) -> None: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...

class IAS_GeometricEncircledEnergy(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def HuygensDelta(self) -> float: ...
    @property
    def HuygensSample(self) -> SampleSizes: ...
    @property
    def RadiusMaximum(self) -> float: ...
    @property
    def ReferTo(self) -> ReferToTypes: ...
    @property
    def SampleSize(self) -> SampleSizes: ...
    @property
    def ScatterRays(self) -> bool: ...
    @property
    def ShowDiffractionLimit(self) -> bool: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Type(self) -> EncircledEnergyTypes: ...
    @property
    def UseDashes(self) -> bool: ...
    @property
    def UseHuygensPSF(self) -> bool: ...
    @property
    def UsePolarization(self) -> bool: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @HuygensDelta.setter
    def HuygensDelta(self, value: float) -> None: ...
    @HuygensSample.setter
    def HuygensSample(self, value: SampleSizes) -> None: ...
    @RadiusMaximum.setter
    def RadiusMaximum(self, value: float) -> None: ...
    @ReferTo.setter
    def ReferTo(self, value: ReferToTypes) -> None: ...
    @SampleSize.setter
    def SampleSize(self, value: SampleSizes) -> None: ...
    @ScatterRays.setter
    def ScatterRays(self, value: bool) -> None: ...
    @ShowDiffractionLimit.setter
    def ShowDiffractionLimit(self, value: bool) -> None: ...
    @Type.setter
    def Type(self, value: EncircledEnergyTypes) -> None: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @UseHuygensPSF.setter
    def UseHuygensPSF(self, value: bool) -> None: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...

class IAS_GeometricLineEdgeSpread(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def RadiusMaximum(self) -> float: ...
    @property
    def SampleSize(self) -> SampleSizes: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Type(self) -> GeometricLineEdgeSpreadTypes: ...
    @property
    def UsePolarization(self) -> bool: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @RadiusMaximum.setter
    def RadiusMaximum(self, value: float) -> None: ...
    @SampleSize.setter
    def SampleSize(self, value: SampleSizes) -> None: ...
    @Type.setter
    def Type(self, value: GeometricLineEdgeSpreadTypes) -> None: ...
    @UsePolarization.setter
    def UsePolarization(self, value: bool) -> None: ...

class ReferToTypes:
    ChiefRay = 0
    Centroid = 1
    Vertex = 2