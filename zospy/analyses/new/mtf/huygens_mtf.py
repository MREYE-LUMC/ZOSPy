"""Huygens MTF analysis."""

from __future__ import annotations

from typing import Annotated

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.new.base import BaseAnalysisWrapper
from zospy.analyses.new.decorators import analysis_settings
from zospy.analyses.new.parsers.types import FieldNumber, WavelengthNumber  # noqa: TCH001
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling

__all__ = ("HuygensMtfSettings", "HuygensMTF")


@analysis_settings
class HuygensMtfSettings:
    """Settings for the Huygens MTF analysis.

    For an in depth explanation of the parameters, see the OpticStudio user manual.

    Attributes
    ----------
    pupil_sampling : str | int
        The pupil sampling, either string (e.g. '64x64') or int.
        The integer will be treated as a ZOSAPI Constants integer.
    image_sampling : str | int
        The image sampling, either string (e.g., '64x64') or int.
        The integer will be treated as a ZOSAPI Constants integer.
    image_delta : float
        The Image Delta, defaults to 0.0.
    wavelength : str | int
        The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
    field : str | int
        The field to use in the MTF. Either 'All' or an integer specifying the field number.
    mtf_type : ZOSAPI.Analysis.Settings.Mtf.MtfTypes.Modulation
        The MTF type (e.g. `Modulation`) that is calculated.
    maximum_frequency : float
        The maximum frequency at which the MTF is calculated.
        Units are either cycles/mm or cycles/mr, depending on system setting.
        Defaults to 150.0, which is more appropriate when units are set to cycles/mm.
    use_polarization : bool
        Use polarization. Defaults to False.
    use_dashes : bool
        Use dashes. Defaults to False.
    """

    pupil_sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Pupil sampling grid size")
    image_sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Image sampling grid size")
    image_delta: float = Field(default=0.0, description="Image delta")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number or 'All'")
    field: FieldNumber = Field(default="All", description="Field number or 'All'")
    mtf_type: str = Field(default="Modulation", description="MTF type")
    maximum_frequency: float = Field(default=150.0, description="Maximum frequency")
    use_polarization: bool = Field(default=False, description="Use polarization")
    use_dashes: bool = Field(default=False, description="Use dashes")


class HuygensMTF(BaseAnalysisWrapper[DataFrame, HuygensMtfSettings]):
    """Huygens Modulation Transfer Function (MTF) analysis."""

    TYPE = "HuygensMtf"

    _needs_config_file = False
    _needs_text_output_file = False

    def __init__(
        self,
        *,
        pupil_sampling: str | int = "32x32",
        image_sampling: str | int = "32x32",
        image_delta: float = 0.0,
        wavelength: int | str = "All",
        field: int | str = "All",
        mtf_type: str = "Modulation",
        maximum_frequency: float = 150.0,
        use_polarization: bool = False,
        use_dashes: bool = False,
        settings: HuygensMtfSettings | None = None,
    ):
        """Create a new Huygens MTF analysis."""
        super().__init__(settings or HuygensMtfSettings(), locals())

    def run_analysis(self) -> DataFrame | None:
        """Run the Huygens MTF analysis."""
        self.analysis.Settings.PupilSampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.pupil_sampling)
        )
        self.analysis.Settings.ImageSampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.image_sampling)
        )
        self.analysis.Settings.ImageDelta = self.settings.image_delta
        self.analysis.wavelength = self.settings.wavelength
        self.analysis.field = self.settings.field
        self.analysis.Settings.Type = self.settings.mtf_type
        self.analysis.Settings.MaximumFrequency = self.settings.maximum_frequency
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.UseDashes = self.settings.use_dashes

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        return self.get_data_series()