"""FFT Through Focus MTF analysis."""

from __future__ import annotations

from typing import Annotated, Literal

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.new.base import BaseAnalysisWrapper
from zospy.analyses.new.decorators import analysis_settings
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling


@analysis_settings
class FFTThroughFocusMTFSettings:
    """Settings for the FFT Through Focus MTF analysis.

    For an in depth explanation of the parameters, see the OpticStudio user manual.

    Attributes
    ----------
    sampling : str | int
        The pupil sampling, either string (e.g. "64x64") or int. Integers will be treated as a ZOSAPI Constants
        integer and must be greater than or equal to 0. Defaults to "64x64".
    delta_focus : float
        The Z-axis range or optical power range, depending on the optical system. Defaults to 0.1.
    frequency : float
        The spatial frequency for which the MTF is calculated. Defaults to 0.
    number_of_steps : int
        The number of steps in the focus range. Defaults to 5.
    wavelength : int | str
        The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
    field : str | int
        The field to use in the MTF. Either 'All' or an integer specifying the field number.
    mtf_type : zospy.constants.Analysis.Settings.Mtf.MtfTypes.Modulation
        The MTF type (e.g. `Modulation`) that is calculated.
    use_polarization : bool
        Use polarization. Defaults to False.
    use_dashes : bool
        Use dashes. Defaults to False.
    """

    sampling: str | Annotated[int, Field(ge=0)] = Field(default="64x64", description="Sampling grid size")
    delta_focus: float = Field(default=0.1, description="Focus step size")
    frequency: float = Field(default=0, description="Frequency")
    number_of_steps: int = Field(default=5, ge=0, description="Number of steps")
    wavelength: Literal["All"] | Annotated[int, Field(gt=0)] = Field(
        default="All", description="Wavelength number or 'All'"
    )
    field: Literal["All"] | Annotated[int, Field(gt=0)] = Field(default="All", description="Field number or 'All'")
    mtf_type: str = Field(default="Modulation", description="MTF type")
    use_polarization: bool = Field(default=False, description="Use polarization")
    use_dashes: bool = Field(default=False, description="Use dashes")


class FFTThroughFocusMTF(BaseAnalysisWrapper[DataFrame | None, FFTThroughFocusMTFSettings]):
    """FFT Through Focus MTF analysis."""

    TYPE = "FftThroughFocusMtf"

    _needs_config_file = True
    _needs_text_output_file = False

    def __init__(
        self,
        *,
        sampling: str | int = "64x64",
        delta_focus: float = 0.1,
        frequency: float = 0,
        number_of_steps: int = 5,
        wavelength: int | Literal["All"] = "All",
        field: int | Literal["All"] = "All",
        mtf_type: constants.Analysis.Settings.Mtf.MtfTypes | str = "Modulation",
        use_polarization: bool = False,
        use_dashes: bool = False,
        settings: FFTThroughFocusMTFSettings | None = None,
    ):
        """Create a new FFT Through Focus MTF analysis.

        See Also
        --------
        FFTThroughFocusMTFSettings : Settings for the FFT Through Focus MTF analysis.
        """
        super().__init__(settings or FFTThroughFocusMTFSettings(), locals())

    def run_analysis(self) -> DataFrame | None:
        """Run the FFT Through Focus MTF analysis."""
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
        if self.oss._ZOS.version < "21.2.0":  # noqa: SLF001
            config_file = str(self.config_file)

            self.analysis.Settings.SaveTo(config_file)

            self.analysis.Settings.ModifySettings(
                config_file,
                "TFM_TYPE",
                str(int(constants.process_constant(constants.Analysis.Settings.Mtf.MtfTypes, self.settings.mtf_type))),
            )
            self.analysis.Settings.LoadFrom(config_file)
