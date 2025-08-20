"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from zospy.api.stubs._ZOSAPI.Analysis.Settings import (
    IAS_,
    IAS_Field,
    IAS_Surface,
    IAS_Wavelength,
)
from zospy.api.stubs._ZOSAPI.Analysis.Settings.Fans import (
    SagittalAberrationComponent,
    TangentialAberrationComponent,
)

from zospy.api.stubs._ZOSAPI_constants.Analysis.Settings.Fans import (
    SagittalAberrationComponent,
    TangentialAberrationComponent,
)

__all__ = ("IAS_Fan", "SagittalAberrationComponent", "TangentialAberrationComponent")

class IAS_Fan(IAS_):
    @property
    def Field(self) -> IAS_Field: ...
    @property
    def Surface(self) -> IAS_Surface: ...
    @property
    def Wavelength(self) -> IAS_Wavelength: ...
    @property
    def NumberOfRays(self) -> int: ...
    @NumberOfRays.setter
    def NumberOfRays(self, value: int) -> None: ...
    @property
    def PlotScale(self) -> float: ...
    @PlotScale.setter
    def PlotScale(self, value: float) -> None: ...
    @property
    def CheckApertures(self) -> bool: ...
    @CheckApertures.setter
    def CheckApertures(self, value: bool) -> None: ...
    @property
    def VignettedPupil(self) -> bool: ...
    @VignettedPupil.setter
    def VignettedPupil(self, value: bool) -> None: ...
    @property
    def UseDashes(self) -> bool: ...
    @UseDashes.setter
    def UseDashes(self, value: bool) -> None: ...
    @property
    def Sagittal(self) -> SagittalAberrationComponent: ...
    @Sagittal.setter
    def Sagittal(self, value: SagittalAberrationComponent) -> None: ...
    @property
    def Tangential(self) -> TangentialAberrationComponent: ...
    @Tangential.setter
    def Tangential(self, value: TangentialAberrationComponent) -> None: ...

# SagittalAberrationComponent is imported as constant

# TangentialAberrationComponent is imported as constant
