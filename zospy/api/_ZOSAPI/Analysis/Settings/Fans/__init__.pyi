"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis.Settings import (
    IAS_,
    IAS_Field,
    IAS_Surface,
    IAS_Wavelength,
)

__all__ = ("IAS_Fan", "SagittalAberrationComponent", "TangentialAberrationComponent")

class IAS_Fan(IAS_):
    @property
    def CheckApertures(self) -> bool: ...
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def NumberOfRays(self) -> int: ...
    @property
    def PlotScale(self) -> float: ...
    @property
    def Sagittal(self) -> SagittalAberrationComponent: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Tangential(self) -> TangentialAberrationComponent: ...
    @property
    def UseDashes(self) -> bool: ...
    @property
    def VignettedPupil(self) -> bool: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @CheckApertures.setter
    def CheckApertures(self, value: bool) -> None: ...
    @NumberOfRays.setter
    def NumberOfRays(self, value: int) -> None: ...
    @PlotScale.setter
    def PlotScale(self, value: float) -> None: ...
    @Sagittal.setter
    def Sagittal(self, value: SagittalAberrationComponent) -> None: ...
    @Tangential.setter
    def Tangential(self, value: TangentialAberrationComponent) -> None: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @VignettedPupil.setter
    def VignettedPupil(self, value: bool) -> None: ...

class SagittalAberrationComponent:
    Aberration_X = 0
    Aberration_Y = 1

class TangentialAberrationComponent:
    Aberration_Y = 0
    Aberration_X = 1
