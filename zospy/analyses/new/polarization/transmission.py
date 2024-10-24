from __future__ import annotations

import struct
from typing import Annotated

import pandas as pd
from pydantic import Field

from zospy.analyses.new.base import AnalysisWrapper
from zospy.analyses.new.decorators import analysis_result, analysis_settings
from zospy.analyses.new.parsers.transformers import SimpleField, ZospyTransformer
from zospy.analyses.new.parsers.types import UnitField, ValidatedDataFrame
from zospy.api import constants
from zospy.utils import zputils
from zospy.zpcore import OpticStudioSystem


class PolarizationTransmissionTransformer(ZospyTransformer):
    def chief_ray_transmissions(self, args) -> SimpleField:
        return SimpleField("Chief ray transmission", list(args))

    def field_transmissions(self, args) -> SimpleField:
        return SimpleField("Field transmission", list(args))

    def transmission_table(self, args) -> SimpleField:
        header, rows = args[0]
        return SimpleField("Transmissions", pd.DataFrame(columns=header, data=rows))


@analysis_result
class FieldTransmission:
    field_pos: UnitField = Field(alias="Field Pos")
    total_transmission: float = Field(alias="Total Transmission")
    transmissions: dict[float, float] = Field(alias="Transmission at")


@analysis_result
class ChiefRayTransmission:
    field_pos: UnitField = Field(alias="Field Pos")
    wavelength: dict[int, UnitField] = Field(alias="Wavelength")
    transmissions: ValidatedDataFrame = Field(alias="Transmissions")


@analysis_result
class PolarizationTransmissionResult:
    x_field: float = Field(alias="X-Field")
    y_field: float = Field(alias="Y-Field")
    x_phase: float = Field(alias="X-Phase")
    y_phase: float = Field(alias="Y-Phase")

    grid_size: str = Field(alias="Grid Size")

    field_transmissions: list[FieldTransmission] = Field(alias="Field transmission")
    chief_ray_transmissions: list[ChiefRayTransmission] = Field(alias="Chief ray transmission")


@analysis_settings
class PolarizationTransmissionSettings:
    sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Sampling grid size")
    unpolarized: bool = Field(default=False, description="Use unpolarized light")
    jx: float = Field(default=1, description="Jones electric field vector X component")
    jy: float = Field(default=0, description="Jones electric field vector Y component")
    x_phase: float = Field(default=0, description="Jones electric field vector X phase in degrees")
    y_phase: float = Field(default=0, description="Jones electric field vector Y phase in degrees")


class PolarizationTransmission(AnalysisWrapper[PolarizationTransmissionResult, PolarizationTransmissionSettings]):
    TYPE = "Transmission"

    _needs_config_file = True
    _needs_text_output_file = True

    def __init__(
        self,
        sampling: str | int = "32x32",
        unpolarized: bool = False,
        jx: float = 1,
        jy: float = 0,
        x_phase: float = 0,
        y_phase: float = 0,
        settings: PolarizationTransmissionSettings | None = None,
    ):
        super().__init__(settings or PolarizationTransmissionSettings(), locals())

    @property
    def settings(self) -> PolarizationTransmissionSettings:
        return self._settings

    def run_analysis(self, oss: OpticStudioSystem, *args, **kwargs) -> PolarizationTransmissionResult:
        settings = self.analysis.Settings
        settings.SaveTo(str(self.config_file))

        settings_bytestring = self.config_file.read_bytes()

        settings_bytearray = bytearray(settings_bytestring)

        sampling_value = constants.process_constant(
            constants.Analysis.SampleSizes, zputils.standardize_sampling(self.settings.sampling)
        ).value__

        # Change settings - all byte indices could only be found via reverse engineering :(
        settings_bytearray[56] = sampling_value
        settings_bytearray[60] = int(self.settings.unpolarized)
        settings_bytearray[24:32] = struct.pack("<d", self.settings.jx)
        settings_bytearray[32:40] = struct.pack("<d", self.settings.jy)
        settings_bytearray[40:48] = struct.pack("<d", self.settings.x_phase)
        settings_bytearray[48:56] = struct.pack("<d", self.settings.y_phase)

        self.config_file.write_bytes(settings_bytearray)

        settings.LoadFrom(str(self.config_file))

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Parse results
        result = self.parse_output(
            "polarization_transmission",
            transformer=PolarizationTransmissionTransformer,
            result_type=PolarizationTransmissionResult,
        )

        return result
