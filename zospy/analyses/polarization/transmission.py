"""Polarization transmission analysis."""

from __future__ import annotations

import struct
from typing import Annotated

import pandas as pd
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers.transformers import SimpleField, ZospyTransformer
from zospy.analyses.parsers.types import UnitField, ValidatedDataFrame  # noqa: TCH001
from zospy.api import constants
from zospy.utils import zputils

__all__ = ("PolarizationTransmission", "PolarizationTransmissionSettings")


class PolarizationTransmissionTransformer(ZospyTransformer):
    """Transformer for the output of the Polarization Transmission analysis."""

    def chief_ray_transmissions(self, args) -> SimpleField:
        """Transform the chief ray transmission data to a SimpleField."""
        return SimpleField("Chief ray transmission", list(args))

    def field_transmissions(self, args) -> SimpleField:
        """Transform the field transmission data to a SimpleField."""
        return SimpleField("Field transmission", list(args))

    def transmission_table(self, args) -> SimpleField:
        """Transform the transmission table data to a SimpleField."""
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
    """Data for the Polarization Transmission analysis."""

    # x_field, y_field, x_phase, y_phase are only defined if the system is polarized
    x_field: float | None = Field(default=None, alias="X-Field")
    y_field: float | None = Field(default=None, alias="Y-Field")
    x_phase: float | None = Field(default=None, alias="X-Phase")
    y_phase: float | None = Field(default=None, alias="Y-Phase")

    grid_size: str = Field(alias="Grid Size")

    field_transmissions: list[FieldTransmission] = Field(alias="Field transmission")
    chief_ray_transmissions: list[ChiefRayTransmission] = Field(alias="Chief ray transmission")


@analysis_settings
class PolarizationTransmissionSettings:
    """Settings for the polarization transmission analysis.

    Attributes
    ----------
    sampling : str | int
        Sampling grid size. Defaults to "32x32".
    unpolarized : bool
        Use unpolarized light. Defaults to `False`.
    jx : float
        Jones x electric field. Defaults to 1.
    jy : float
        Jones y electric field. Defaults to 0.
    x_phase : float
        Phase of the X component of the Jones electric field in degrees. Defaults to 0.
    y_phase : float
        Phase of the Y component of the Jones electric field in degrees. Defaults to 0.
    """

    sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Sampling grid size")
    unpolarized: bool = Field(default=False, description="Use unpolarized light")
    jx: float = Field(default=1, description="Jones electric field vector X component")
    jy: float = Field(default=0, description="Jones electric field vector Y component")
    x_phase: float = Field(default=0, description="Jones electric field vector X phase in degrees")
    y_phase: float = Field(default=0, description="Jones electric field vector Y phase in degrees")


class PolarizationTransmission(
    BaseAnalysisWrapper[PolarizationTransmissionResult, PolarizationTransmissionSettings],
    analysis_type="Transmission",
    needs_config_file=True,
    needs_text_output_file=True,
):
    """Polarization transmission analysis."""

    def __init__(
        self,
        *,
        sampling: str | int = "32x32",
        unpolarized: bool = False,
        jx: float = 1,
        jy: float = 0,
        x_phase: float = 0,
        y_phase: float = 0,
    ):
        """Create a new polarization transmission analysis.

        See Also
        --------
        PolarizationTransmissionSettings : Settings for the polarization transmission analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> PolarizationTransmissionResult:
        """Run the polarization transmission analysis."""
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
        return self.parse_output(
            "polarization_transmission",
            transformer=PolarizationTransmissionTransformer,
            result_type=PolarizationTransmissionResult,
        )
