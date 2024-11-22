from __future__ import annotations

from typing import Annotated, Literal

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.new.base import AnalysisWrapper
from zospy.analyses.new.decorators import analysis_settings
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling


@analysis_settings
class FFTThroughFocusMTFSettings:
    sampling: str | Annotated[int, Field(ge=0)] = Field(default="64x64", description="Sampling grid size")
    delta_focus: float = Field(default=0.1, description="Focus step size")
    frequency: float = Field(default=0, description="Frequency")
    number_of_steps: int = Field(default=10, ge=0, description="Number of steps")
    wavelength: Literal["All"] | Annotated[int, Field(gt=0)] = Field(
        default="All", description="Wavelength number or 'All'"
    )
    field: Literal["All"] | Annotated[int, Field(gt=0)] = Field(default="All", description="Field number or 'All'")
    mtf_type: str = Field(default="Modulation", description="MTF type")
    use_polarization: bool = Field(default=False, description="Use polarization")
    use_dashes: bool = Field(default=False, description="Use dashes")


class FFTThroughFocusMTF(AnalysisWrapper[DataFrame | None, FFTThroughFocusMTFSettings]):
    TYPE = "FftThroughFocusMtf"

    _needs_config_file = True
    _needs_text_output_file = False

    def __init__(
        self,
        sampling: str | int = "64x64",
        delta_focus: float = 0.1,
        frequency: float = 0,
        number_of_steps: int = 10,
        wavelength: int | Literal["All"] = "All",
        field: int | Literal["All"] = "All",
        mtf_type: constants.Analysis.Settings.Mtf.MtfTypes | str = "Modulation",
        use_polarization: bool = False,
        use_dashes: bool = False,
        settings: FFTThroughFocusMTFSettings | None = None,
    ):
        super().__init__(settings or FFTThroughFocusMTFSettings(), locals())

    def run_analysis(self, *args, **kwargs) -> DataFrame | None:
        self.analysis.Settings.SampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.sampling)
        )
        self.analysis.Settings.DeltaFocus = self.settings.delta_focus
        self.analysis.Settings.Frequency = self.settings.frequency
        self.analysis.Settings.NumberOfSteps = self.settings.number_of_steps
        self.analysis.wavelength = self.settings.wavelength
        self.analysis.field = self.settings.field
        self.analysis.Settings.MtfType = constants.process_constant(
            constants.Analysis.Settings.Mtf.MtfTypes, self.settings.mtf_type
        )
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.UseDashes = self.settings.use_dashes

        self._correct_mtf_type_api_bug()

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        return self.get_data_series()

    def _correct_mtf_type_api_bug(self) -> None:
        """Correction for an API bug in OpticStudio versions < 21.2.

        In these versions, the MTF Type cannot be set through the ZOS-API for the FFT Through Focus MTF
        See also: https://community.zemax.com/zos-api-12/zos-api-setting-mtf-property-type-not-working-730

        Returns
        -------
        None
        """
        if self.oss._ZOS.version < "21.2.0":
            config_file = str(self.config_file)

            self.analysis.Settings.SaveTo(config_file)

            self.analysis.Settings.ModifySettings(
                config_file,
                "TFM_TYPE",
                str(int(constants.process_constant(constants.Analysis.Settings.Mtf.MtfTypes, self.settings.mtf_type))),
            )
            self.analysis.Settings.LoadFrom(config_file)
