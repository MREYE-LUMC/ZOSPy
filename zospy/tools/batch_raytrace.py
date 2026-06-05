"""Batch Ray Trace tool."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pydantic import Field, PositiveInt, BeforeValidator, model_validator

from zospy.tools.base import BaseToolWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import ZOSAPIConstant
from zospy.api import constants

if TYPE_CHECKING:
    from typing import Literal, Annotated
    from collections.abc import Sequence, Callable
    
    from zospy.api import _ZOSAPI

__all__ = ("BatchRayTraceNormUnpol", "BatchRayTraceNormUnpolSettings")


def ndarray_to_list(v):
    """Function to convert ndarray to list."""
    if isinstance(v, np.ndarray):
        return v.tolist()
    return v

# Constrained types
NormalizedCoordinate = Annotated[float, Field(le=1.0, ge=-1.0)]
CoordinateVector = Annotated[
    Sequence[NormalizedCoordinate],
    BeforeValidator(ndarray_to_list),
]
PositiveIntVector = Annotated[
    Sequence[PositiveInt],
    BeforeValidator(ndarray_to_list),
]

@analysis_settings
class BatchRayTraceNormUnpolSettings:
    """Settings for the Batch Ray Trace of unpolarized light.

    Attributes
    ----------
    hx : Sequence[float]
        Sequence of normalized X field coordinates. Defaults to [0].
    hy : Sequence[float]
        Sequence of normalized Y field coordinates. Defaults to [0].
    px : Sequence[float]
        Sequence of normalized X pupil coordinates. Defaults to [0].
    py : Sequence[float]
        Sequence of normalized Y pupil coordinates. Defaults to [0].
    wavelength : int | Sequence[int]
        The wavelength number that is to be used. Must be an integer or a sequence of integers specifying the wavelength number.
        Defaults to 1.
    surface : str | int
        Surface up to which the rays will be traced. Either 'Image' or an integer specifying the surface number.
        Defaults to 'Image'.
    rays_type : zospy.api.constants.Tools.RayTrace.RaysType
        Type of rays to trace ('Real' or 'Paraxial'). Defaults to 'Real'.
    opd_mode : zospy.api.constants.Tools.RayTrace.OPDMode
        Mode of optical path difference for rays (e.g. 'None'). Defaults to 'None'.
    """

    hx: CoordinateVector = Field(default=[0], description="Normalized X field coordinate")
    hy: CoordinateVector = Field(default=[0], description="Normalized Y field coordinate")
    px: CoordinateVector = Field(default=[0], description="Normalized X pupil coordinate")
    py: CoordinateVector = Field(default=[0], description="Normalized Y pupil coordinate")
    wavelength: PositiveInt | PositiveIntVector = Field(default=1, description="Wavelength number")
    surface: Literal["Image"] | Annotated[int, Field(ge=0)] = Field(default="Image", description="Surface number")
    rays_type: ZOSAPIConstant("Tools.RayTrace.RaysType") = Field(default="Real", description="Type of rays to trace")
    opd_mode: ZOSAPIConstant("Tools.RayTrace.OPDMode") = Field(default="None", description="Mode of optical path difference")

    @model_validator(mode="after")
    def validate_lengths(self):
        """Validate that hx, hy, px, py (and wavelength) have the same lengths."""
        if not len(self.hx) == len(self.hy) == len(self.px) == len(self.py):
            raise ValueError(
                f"Hx, Hy, Px, Py must all have the same length."
            )
        expected_len = len(self.hx)

        if isinstance(self.wavelength, Sequence):
            if len(self.wavelength) != expected_len:
                raise ValueError(
                    f"`wavelength` sequence length ({len(self.wavelength)}) must match "
                    f"the length of Hx, Hy, Px, Py ({expected_len})."
                )

        return self
    

class BatchRayTraceNormUnpol(BaseToolWrapper[pd.DataFrame, BatchRayTraceNormUnpolSettings]):
    """Batch Ray Trace of unpolarized light."""

    def __init__(
        self,
        *,
        hx: Sequence[float] = (0,),
        hy: Sequence[float] = (0,),
        px: Sequence[float] = (0,),
        py: Sequence[float] = (0,),
        wavelength: int | Sequence[int] = 1,
        surface: Literal["Image"] | int = "Image",
        rays_type: str | constants.Tools.RayTrace.RaysType = "Real",
        opd_mode: str | constants.Tools.RayTrace.OPDMode = "None",
    ):
        """Create a new Batch Ray Trace of unpolarized light.

        See Also
        --------
        BatchRayTraceNormUnpolSettings : Settings for the Batch Ray Trace of unpolarized light.
        """
        super().__init__(settings_kws=locals())

    def _get_tool_opener(self, oss) -> Callable[[], _ZOSAPI.Tools.RayTrace.IBatchRayTrace]:
        """Get a callable that opens the batch raytrace tool in OpticStudio and returns the tool object."""
        return oss.Tools.OpenBatchRayTrace
        

    def run_analysis(self, tool: _ZOSAPI.Tools.RayTrace.IBatchRayTrace) -> pd.DataFrame:
        """Run the Batch Ray Trace of unpolarized light."""
        tool.Hx = self.settings.hx
        tool.Hy = self.settings.hy
        tool.Px = self.settings.px
        tool.Py = self.settings.py
        tool.number_of_rays = len(tool.Hx)
        tool.wavelengths = [self.settings.wavelength] * number_of_rays if isinstance(self.settings.wavelength, int) else self.settings.wavelength
        tool.rays_type = constants.process_constant(
            constants.Tools.RayTrace.RaysType, self.settings.rays_type
        )
        tool.opd_mode = constants.process_constant(
            constants.Tools.RayTrace.OPDMode, self.settings.opd_mode
        )
        tool.surface = -1 if self.settings.surface == "Image" else self.settings.surface

        # Initiate batch ray trace
        norm_unpol_data = tool.CreateNormUnpol(
            tool.number_of_rays,
            tool.rays_type,
            tool.surface,
        )

        # Add rays
        for wavelength, hx, hy, px, py in zip(
            tool.wavelengths,
            tool.Hx,
            tool.Hy,
            tool.Px,
            tool.Py,
        ):
            norm_unpol_data.AddRay(wavelength, hx, hy, px, py, tool.opd_mode)

        # Run ray trace and read results
        tool.RunAndWaitForCompletion()
        norm_unpol_data.StartReadingResults()

        # Read all results and append to outputs
        outputs = []
        columns = ["rayNumber","ErrorCode","vignetteCode",
                   "X","Y","Z","L","M","N",
                   "l2","m2","n2","opd","Intensity"]
        outputs = [norm_unpol_data.ReadNextResult()[1:] for _ in range(number_of_rays)]

        # Convert to DataFrame and return
        return pd.DataFrame(outputs, columns=columns)

