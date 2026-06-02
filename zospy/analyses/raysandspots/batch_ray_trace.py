"""Batch Ray Trace analysis."""

from __future__ import annotations

from typing import Literal, Annotated, Union

import pandas as pd
from pydantic import confloat, conint, Field, model_validator
from System import Int32, Double

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.api import constants

__all__ = ("NormUnpol", "NormUnpolSettings")


# Constrained types
FloatInRange = Annotated[float, confloat(le=1.0, ge=-1.0)]
PositiveInt = Annotated[int, conint(gt=0)]

@analysis_settings
class NormUnpolSettings:
    """Settings for the Batch Ray Trace of unpolarized light.

    Attributes
    ----------
    hx : list[float]
        List of normalized X field coordinates. Defaults to [0].
    hy : list[float]
        List of normalized Y field coordinates. Defaults to [0].
    px : list[float]
        List of normalized X pupil coordinates. Defaults to [0].
    py : list[float]
        List of normalized Y pupil coordinates. Defaults to [0].
    wavelength : int | list[int]
        The wavelength number that is to be used. Must be an integer or a list of integers specifying the wavelength number.
        Defaults to 1.
    surface : str | int
        Surface up to which the rays will be traced. Either 'Image' or an integer specifying the surface number.
        Defaults to 'Image'.
    rays_type : zospy.api.constants.Tools.RayTrace.RaysType
        Type of rays to trace ('Real' or 'Paraxial'). Defaults to 'Real'.
    opd_mode : zospy.api.constants.Tools.RayTrace.OPDMode
        Mode of optical path difference for rays (e.g. 'None'). Defaults to 'None'.
    """

    hx: list[FloatInRange] = Field(default=[0], description="Normalized X field coordinate")
    hy: list[FloatInRange] = Field(default=[0], description="Normalized Y field coordinate")
    px: list[FloatInRange] = Field(default=[0], description="Normalized X pupil coordinate")
    py: list[FloatInRange] = Field(default=[0], description="Normalized Y pupil coordinate")
    wavelength: Union[PositiveInt, list[PositiveInt]] = Field(default=1, description="Wavelength number")
    surface: Literal["Image"] | Annotated[int, Field(ge=0)] = Field(default="Image", description="Surface number")
    rays_type: Literal["Real", "Paraxial"] = Field(default="Real", description="Type of rays to trace")
    opd_mode: Literal["None", "Current", "CurrentAndChief"] = Field(default="None", description="Mode of optical path difference")

    @model_validator(mode="after")
    def validate_lengths(self):
        """Validate that hx, hy, px, py (and wavelength) have the same lengths."""
        lengths = [len(self.hx), len(self.hy), len(self.px), len(self.py)]
        if len(set(lengths)) != 1:
            raise ValueError(
                f"Hx, Hy, Px, Py must all have the same length; got lengths {lengths}."
            )
        expected_len = lengths[0]

        if isinstance(self.wavelength, list):
            if len(self.wavelength) != expected_len:
                raise ValueError(
                    f"`wavelength` list length ({len(self.wavelength)}) must match "
                    f"the length of Hx, Hy, Px, Py ({expected_len})."
                )

        return self
    

class NormUnpol(BaseAnalysisWrapper[pd.DataFrame | None, NormUnpolSettings],
    analysis_type="RayTrace",
):
    """Batch Ray Trace of unpolarized light."""

    def __init__(
        self,
        *,
        hx: list[float] = [0],
        hy: list[float] = [0],
        px: list[float] = [0],
        py: list[float] = [0],
        wavelength: int | list[int] = 1,
        surface: Literal["Image"] | int = "Image",
        rays_type: str = "Real",
        opd_mode: str = "None",
    ):
        """Create a new Batch Ray Trace of unpolarized light.

        See Also
        --------
        NormUnpolSettings : Settings for the Batch Ray Trace of unpolarized light.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> pd.DataFrame | None:
        """Run the Batch Ray Trace of unpolarized light."""
        number_of_rays = len(self.settings.hx)
        if isinstance(self.settings.wavelength, int):
            wvls = [self.settings.wavelength]*number_of_rays
        else:
            wvls = self.settings.wavelength
        rays_type = constants.process_constant(
            constants.Tools.RayTrace.RaysType, self.settings.rays_type
        )
        opd_mode = constants.process_constant(
            constants.Tools.RayTrace.OPDMode, self.settings.opd_mode
        )
        surface = -1 if self.settings.surface == "Image" else self.settings.surface

        # Initiate batch ray trace
        raytrace = self.oss.Tools.OpenBatchRayTrace()
        normUnPolData = raytrace.CreateNormUnpol(
            number_of_rays,
            rays_type,
            surface,
        )

        # Add rays
        for ii in range(number_of_rays):
            normUnPolData.AddRay(
                wvls[ii],
                self.settings.hx[ii],
                self.settings.hy[ii],
                self.settings.px[ii],
                self.settings.py[ii],
                opd_mode,
            )

        # Run ray trace and read results
        self.analysis.ApplyAndWaitForCompletion()
        raytrace.RunAndWaitForCompletion()
        normUnPolData.StartReadingResults()

        # Create placeholders for all output arguments
        placeholders = [Int32(1)]*3 + [Double(1.0)]*11

        # Read all results and append to outputs
        outputs = []
        columns = ["rayNumber","ErrorCode","vignetteCode",
                   "X","Y","Z","L","M","N",
                   "l2","m2","n2","opd","Intensity"]
        for ii in range(number_of_rays):
            outputs.append(normUnPolData.ReadNextResult(*placeholders)[1:])

        # Convert to DataFrame and return
        return pd.DataFrame(outputs, columns=columns)

