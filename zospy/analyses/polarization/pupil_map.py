"""Polarization pupil map analysis."""

from __future__ import annotations

from typing import Literal, Union

import pandas as pd
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result, analysis_settings
from zospy.analyses.parsers import ZospyTransformer
from zospy.analyses.parsers.transformers import SimpleField
from zospy.analyses.parsers.types import UnitField, ValidatedDataFrame  # noqa: TCH001
from zospy.api import constants
from zospy.utils.pyutils import xtoa
from zospy.utils.zputils import standardize_sampling

__all__ = ("PolarizationPupilMap", "PolarizationPupilMapSettings")


class PolarizationPupilMapTransformer(ZospyTransformer):
    def pupil_map_table(self, args):
        header, rows = args[0]
        table = pd.DataFrame(columns=header, data=rows)

        return SimpleField("Pupil Map", table)


@analysis_result
class PolarizationPupilMapResult:
    wavelength: float = Field(alias="Wavelength")
    field_pos: UnitField[float] = Field(alias="Field Pos")
    x_field: float = Field(alias="X-Field")
    y_field: float = Field(alias="Y-Field")
    x_phase: float = Field(alias="X-Phase")
    y_phase: float = Field(alias="Y-Phase")
    configs: int = Field(alias="Configs")
    surface: int = Field(alias="Surface")
    transmission: UnitField[float] = Field(alias="Transmission")
    pupil_map: ValidatedDataFrame = Field(alias="Pupil Map")


@analysis_settings
class PolarizationPupilMapSettings:
    """Settings for the polarization pupil map analysis.

    Attributes
    ----------
    jx : float
        Jones x electric field. Defaults to 1.
    jy : float
        Jones y electric field. Defaults to 0.
    x_phase : float
        Phase of the X component of the Jones electric field in degrees. Defaults to 0.
    y_phase : float
        Phase of the Y component of the Jones electric field in degrees. Defaults to 0.
    wavelength : int
        The wavelength number that is to be used. Should be an integer specifying the wavelength number.
        Defaults to 1.
    field : int | str
        The field number that is to be used. Must be an integer specifying the field number. Defaults
        to 1.
    surface : str or int
        The surface that is to be analyzed. Either 'Image', or an integer. Defaults to 'Image'.
    sampling : str or int
        The size of the used grid, either string (e.g. '65x65') or int. The integer will be treated as if obtained from
        zospy.constants.Analysis.SampleSizes_ContrastLoss. Defaults to '11x11'.
    add_configs : str
        The add configs string.
    sub_configs : str
        The subtract configs string.
    """

    jx: float = Field(default=1.0, description="Jones electric field vector X component")
    jy: float = Field(default=0.0, description="Jones electric field vector Y component")
    x_phase: float = Field(default=0.0, description="Jones electric field vector X phase in degrees")
    y_phase: float = Field(default=0.0, description="Jones electric field vector Y phase in degrees")
    wavelength: int = Field(default=1, ge=1, description="Wavelength number")
    field: int = Field(default=1, ge=1, description="Field number")
    surface: Literal["Image"] | int = Field(default="Image", description="Surface to analyze")
    sampling: str | int = Field(default="11x11", description="Sampling grid size")
    add_configs: str = Field(default="", description="Add configurations")
    sub_configs: str = Field(default="", description="Subtract configurations")


class PolarizationPupilMap(
    BaseAnalysisWrapper[Union[PolarizationPupilMapResult, None], PolarizationPupilMapSettings],
    analysis_type="PolarizationPupilMap",
    needs_config_file=True,
    needs_text_output_file=True,
):
    """Polarization pupil map analysis."""

    def __init__(
        self,
        *,
        jx: float = 1.0,
        jy: float = 0.0,
        x_phase: float = 0.0,
        y_phase: float = 0.0,
        wavelength: int = 1,
        field: int = 1,
        surface: Literal["Image"] | int = "Image",
        sampling: str | int = "11x11",
        add_configs: str = "",
        sub_configs: str = "",
    ):
        """Create a new polarization pupil map analysis.

        See Also
        --------
        PolarizationPupilMapSettings : Settings for the polarization pupil map analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> PolarizationPupilMapResult:
        """Run the polarization pupil map analysis."""
        settings = self.analysis.Settings
        config_file = str(self.config_file)

        # MODIFYSETTINGS are defined in the ZPL help files: The Programming Tab > About the ZPL > Keywords
        settings.SaveTo(config_file)
        settings.ModifySettings(config_file, "PPM_JX", xtoa(self.settings.jx, thousands_separator=None))
        settings.ModifySettings(config_file, "PPM_JY", xtoa(self.settings.jy, thousands_separator=None))
        settings.ModifySettings(config_file, "PPM_PX", xtoa(self.settings.x_phase, thousands_separator=None))
        settings.ModifySettings(config_file, "PPM_PY", xtoa(self.settings.y_phase, thousands_separator=None))
        settings.ModifySettings(config_file, "PPM_WAVE", xtoa(int(self.settings.wavelength), thousands_separator=None))
        settings.ModifySettings(config_file, "PPM_FIELD", xtoa(int(self.settings.field), thousands_separator=None))

        if isinstance(self.settings.surface, str):
            settings.ModifySettings(config_file, "PPM_SURFACE", self.settings.surface)
        else:
            settings.ModifySettings(config_file, "PPM_SURFACE", xtoa(self.settings.surface, thousands_separator=None))

        sampling_value = getattr(
            constants.Analysis.SampleSizes_ContrastLoss, standardize_sampling(self.settings.sampling)
        ).value__
        settings.ModifySettings(config_file, "PPM_SAMP", xtoa(sampling_value - 1, thousands_separator=None))
        settings.ModifySettings(config_file, "PPM_ADDCONFIG", self.settings.add_configs)
        settings.ModifySettings(config_file, "PPM_SUBCONFIG", self.settings.sub_configs)

        settings.LoadFrom(config_file)

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        return self.parse_output(
            "polarization_pupil_map",
            transformer=PolarizationPupilMapTransformer,
            result_type=PolarizationPupilMapResult,
        )
