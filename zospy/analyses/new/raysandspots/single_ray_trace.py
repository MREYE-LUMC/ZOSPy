from __future__ import annotations

from typing import Literal
from warnings import warn

import pandas as pd
from lark import Discard
from pydantic import ConfigDict, Field, model_validator
from pydantic.dataclasses import dataclass

from zospy.analyses.new.base import AnalysisWrapper
from zospy.analyses.new.parsers.transformers import ZospyTransformer
from zospy.analyses.new.parsers.types import UnitField
from zospy.api import constants


class SingleRayTraceTransformer(ZospyTransformer):
    def NAN(self, args):
        return float("nan")

    def text(self, args):
        return Discard

    def ray_trace_data_table(self, args):
        header, rows = args[0]

        empty_column_count = len(header) - len(rows[0])

        if empty_column_count > 0:
            warn("Header and row length mismatch. Empty columns will be filled with NaN.")

            # Check if the last row value is a comment
            if isinstance(rows[0][-1], str):
                for row in rows:
                    # Insert empty columns before the comment column
                    row[-2:-2] = [float("nan")] * empty_column_count
            else:
                for row in rows:
                    # Insert empty columns at the end of the row
                    row.extend([float("nan")] * empty_column_count)

        return pd.DataFrame(rows, columns=header)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class SingleRayTraceResult:
    units: str = Field(alias="Units")
    coordinates: str = Field(alias="Coordinates")
    wavelength: UnitField[float] = Field(alias="Wavelength")

    normalized_x_field_coord: float | None = Field(alias="Normalized X Field Coord (Hx)", default=None)
    normalized_y_field_coord: float | None = Field(alias="Normalized Y Field Coord (Hy)", default=None)
    normalized_x_pupil_coord: float | None = Field(alias="Normalized X Pupil Coord (Px)", default=None)
    normalized_y_pupil_coord: float | None = Field(alias="Normalized Y Pupil Coord (Py)", default=None)

    real_ray_trace_data: pd.DataFrame | None = Field(alias="Real Ray Trace Data", default=None)
    paraxial_ray_trace_data: pd.DataFrame | None = Field(alias="Paraxial Ray Trace Data", default=None)
    ym_um_yc_uc_ray_trace_data: pd.DataFrame | None = Field(
        alias="Trace of Paraxial Y marginal, U marginal, Y chief, U chief only.",
        default=None,
    )

    @model_validator(mode="after")
    def validate_ray_trace_data(self):
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


@dataclass(config=ConfigDict(validate_assignment=True))
class SingleRayTraceSettings:
    hx: float = Field(ge=-1, le=1, default=0, description="Normalized X field coordinate")
    hy: float = Field(ge=-1, le=1, default=0, description="Normalized Y field coordinate")
    px: float = Field(ge=-1, le=1, default=0, description="Normalized X pupil coordinate")
    py: float = Field(ge=-1, le=1, default=0, description="Normalized Y pupil coordinate")
    wavelength: Literal["All"] | int = Field(gt=0, default=1, description="Wavelength number or 'All'")
    field: Literal["All"] | int = Field(gt=0, default=1, description="Field number or 'All'")
    raytrace_type: (Literal["DirectionCosines", "TangentAngle", "YmUmYcUc"]) = Field(default="DirectionCosines")
    global_coordinates: bool = Field(default=False, description="Use global coordinates")


class SingleRayTrace(AnalysisWrapper[SingleRayTraceResult, SingleRayTraceSettings]):
    TYPE = "RayTrace"

    _needs_text_output_file = True

    def __init__(
        self,
        hx: float = 0,
        hy: float = 0,
        px: float = 0,
        py: float = 0,
        wavelength: int = 1,
        field: int = 1,
        raytrace_type: constants.Analysis.Settings.Aberrations.RayTraceType | str = "DirectionCosines",
        global_coordinates: bool = False,
        settings: SingleRayTraceSettings | None = None,
    ):
        super().__init__(settings or SingleRayTraceSettings(), locals())

    @property
    def settings(self) -> SingleRayTraceSettings:
        return self._settings

    @settings.setter
    def settings(self, settings: SingleRayTraceSettings):
        self._settings = settings

    def run_analysis(self, *args, **kwargs) -> SingleRayTraceResult:
        self.analysis.Settings.Hx = self.settings.hx
        self.analysis.Settings.Hy = self.settings.hy
        self.analysis.Settings.Px = self.settings.px
        self.analysis.Settings.Py = self.settings.py
        self.analysis.wavelength = self.settings.wavelength
        self.analysis.field = self.settings.field
        self.analysis.Settings.Type = constants.process_constant(
            constants.Analysis.Settings.Aberrations.RayTraceType, self.settings.raytrace_type
        )
        self.analysis.Settings.UseGlobal = self.settings.global_coordinates

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        result = self.parse_output(
            "single_ray_trace", transformer=SingleRayTraceTransformer, result_type=SingleRayTraceResult
        )

        return result
