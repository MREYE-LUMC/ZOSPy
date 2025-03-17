"""Single Ray Trace analysis."""

from __future__ import annotations

from typing import Literal
from warnings import warn

import pandas as pd
from pydantic import Field, model_validator

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers.transformers import ZospyTransformer
from zospy.analyses.parsers.types import UnitField, ValidatedDataFrame  # noqa: TCH001
from zospy.api import constants

__all__ = ("SingleRayTrace", "SingleRayTraceSettings")


class SingleRayTraceTransformer(ZospyTransformer):
    """Transformer for the output of the Single Ray Trace analysis."""

    def NAN(self, args):  # noqa: N802, ARG002
        """Transform a NaN value."""
        return float("nan")

    def ray_trace_data_table(self, args):
        """Transform the ray trace data table to a DataFrame."""
        header, rows = args[0]
        header_length = len(header)

        # Fill empty columns with NaN
        for row in rows:
            if (row_length := len(row)) < header_length:
                # Warning is only raised once for the full loop
                warn("Header and row length mismatch. Empty columns will be filled with NaN.")

                # Check if the last row value is a comment
                if isinstance(row[-1], str):
                    row[-1:-1] = [float("nan")] * (header_length - row_length)
                else:
                    # Insert empty columns at the end of the row
                    row.extend([float("nan")] * (header_length - row_length))

        return pd.DataFrame(rows, columns=header)


@analysis_result
class SingleRayTraceResult:
    """Data for the Single Ray Trace analysis."""

    units: str = Field(alias="Units")
    coordinates: str = Field(alias="Coordinates")
    wavelength: UnitField[float] = Field(alias="Wavelength")

    normalized_x_field_coord: float | None = Field(alias="Normalized X Field Coord (Hx)", default=None)
    normalized_y_field_coord: float | None = Field(alias="Normalized Y Field Coord (Hy)", default=None)
    normalized_x_pupil_coord: float | None = Field(alias="Normalized X Pupil Coord (Px)", default=None)
    normalized_y_pupil_coord: float | None = Field(alias="Normalized Y Pupil Coord (Py)", default=None)

    real_ray_trace_data: ValidatedDataFrame | None = Field(alias="Real Ray Trace Data", default=None)
    paraxial_ray_trace_data: ValidatedDataFrame | None = Field(alias="Paraxial Ray Trace Data", default=None)
    ym_um_yc_uc_ray_trace_data: ValidatedDataFrame | None = Field(
        alias="Trace of Paraxial Y marginal, U marginal, Y chief, U chief only.",
        default=None,
    )

    @model_validator(mode="after")
    def validate_ray_trace_data(self):
        """Check if all ray trace data types belonging to the ray trace type are present."""
        if (
            self.real_ray_trace_data is None
            and self.paraxial_ray_trace_data is None
            and self.ym_um_yc_uc_ray_trace_data is None
        ):
            raise ValueError("Ray trace data must be specified")
        if (self.real_ray_trace_data is not None and self.paraxial_ray_trace_data is None) or (
            self.real_ray_trace_data is None and self.paraxial_ray_trace_data is not None
        ):
            raise ValueError("Both real and paraxial ray trace data must be specified")
        if self.ym_um_yc_uc_ray_trace_data is not None and (
            self.real_ray_trace_data is not None or self.paraxial_ray_trace_data is not None
        ):
            raise ValueError("Either specify real and paraxial ray trace data or Ym, Um, Yc, Uc ray trace data")

        return self


@analysis_settings
class SingleRayTraceSettings:
    """Settings for the Single Ray Trace analysis.

    Attributes
    ----------
    hx : float
        Normalized X field coordinate. Defaults to 0.
    hy : float
        Normalized Y field coordinate. Defaults to 0.
    px : float
        Normalized X pupil coordinate. Defaults to 0.
    py : float
        Normalized Y pupil coordinate. Defaults to 1.
    wavelength : int
        The wavelength number that is to be used. Must be an integer specifying the wavelength number.
        Defaults to 1.
    field : int
        The field number that is to be used. Must be an integer specifying the field number. "Arbitrary" is 0. Defaults
        to 0.
    raytrace_type : zospy.api.constants.Analysis.Settings.Aberrations.RayTraceType
        The Ray Trace type (e.g. 'DirectionCosines') that is calculated. Defaults to 'DirectionCosines'.
    global_coordinates : bool
        Defines if global coordinates are used. Defaults to `False`.
    """

    # TODO: document the fields
    hx: float = Field(ge=-1, le=1, default=0, description="Normalized X field coordinate")
    hy: float = Field(ge=-1, le=1, default=0, description="Normalized Y field coordinate")
    px: float = Field(ge=-1, le=1, default=0, description="Normalized X pupil coordinate")
    py: float = Field(ge=-1, le=1, default=0, description="Normalized Y pupil coordinate")
    wavelength: int = Field(gt=0, default=1, description="Wavelength number")
    field: int = Field(ge=0, default=0, description="Field number")
    raytrace_type: Literal["DirectionCosines", "TangentAngle", "YmUmYcUc"] = Field(default="DirectionCosines")
    global_coordinates: bool = Field(default=False, description="Use global coordinates")


class SingleRayTrace(
    BaseAnalysisWrapper[SingleRayTraceResult, SingleRayTraceSettings],
    analysis_type="RayTrace",
    needs_text_output_file=True,
):
    """Single Ray Trace analysis."""

    def __init__(
        self,
        *,
        hx: float = 0,
        hy: float = 0,
        px: float = 0,
        py: float = 0,
        wavelength: int = 1,
        field: int = 0,
        raytrace_type: constants.Analysis.Settings.Aberrations.RayTraceType | str = "DirectionCosines",
        global_coordinates: bool = False,
    ):
        """Create a new Single Ray Trace analysis.

        See Also
        --------
        SingleRayTraceSettings : Settings for the Single Ray Trace analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> SingleRayTraceResult:
        """Run the Single Ray Trace analysis."""
        self.analysis.Settings.Hx = self.settings.hx
        self.analysis.Settings.Hy = self.settings.hy
        self.analysis.Settings.Px = self.settings.px
        self.analysis.Settings.Py = self.settings.py
        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.set_field(self.settings.field)
        self.analysis.Settings.Type = constants.process_constant(
            constants.Analysis.Settings.Aberrations.RayTraceType, self.settings.raytrace_type
        )
        self.analysis.Settings.UseGlobal = self.settings.global_coordinates

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        return self.parse_output(
            "single_ray_trace", transformer=SingleRayTraceTransformer, result_type=SingleRayTraceResult
        )
