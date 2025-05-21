"""FFT MTF analysis."""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import FieldNumber, WavelengthNumber, ZOSAPIConstant  # noqa: TCH001
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling

__all__ = ("FFTMTF", "FFTMTFSettings")


@analysis_settings
class FFTMTFSettings:
    """Settings for the FFT MTF analysis.

    For an in depth explanation of the parameters, see the OpticStudio user manual.

    Attributes
    ----------
    sampling : str | int
        The size of the ray grid used to sample the pupil, either string (e.g. '32x32') or int (e.g. 32).
    surface : str | int
        The surface at which the MTF is calculated. Either 'Image' or an integer specifying the surface number.
    wavelength : str | int
        The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
    field : str | int
        The field to use in the MTF. Either 'All' or an integer specifying the field number.
    mtf_type : ZOSAPI.Analysis.Settings.Mtf.MtfTypes.Modulation
        The MTF type (e.g. `Modulation`) that is calculated.
    maximum_frequency : float
        The maximum frequency at which the MTF is calculated. Units are either cycles/mm or cycles/mr, depending on
        system settings. Defaults to 0, which means OpticStudio's default limit is used.
    use_polarization : bool
        Use polarization. Defaults to False.
    use_dashes : bool
        Use dashes. Defaults to False.
    show_diffraction_limit : bool
        Show the diffraction limit. Defaults to False.
    """

    sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Pupil sampling")
    surface: Literal["Image"] | Annotated[int, Field(ge=0)] = Field(default="Image", description="MTF surface")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number or 'All'")
    field: FieldNumber = Field(default="All", description="Field number or 'All'")
    mtf_type: ZOSAPIConstant("Analysis.Settings.Mtf.MtfTypes") = Field(default="Modulation", description="MTF type")
    maximum_frequency: float = Field(default=0.0, description="Maximum frequency")
    use_polarization: bool = Field(default=False, description="Use polarization")
    use_dashes: bool = Field(default=False, description="Use dashes")
    show_diffraction_limit: bool = Field(default=False, description="Show diffraction limit")


class FFTMTF(BaseAnalysisWrapper[Union[DataFrame, None], FFTMTFSettings], analysis_type="FftMtf"):
    """FFT Modulation Transfer Function (MTF) analysis."""

    def __init__(
        self,
        *,
        sampling: str | int = "32x32",
        surface: Literal["Image"] | int = "Image",
        wavelength: int | Literal["All"] = "All",
        field: int | Literal["All"] = "All",
        mtf_type: str | constants.Analysis.Settings.Mtf.MtfTypes = "Modulation",
        maximum_frequency: float = 0.0,
        use_polarization: bool = False,
        use_dashes: bool = False,
        show_diffraction_limit: bool = False,
    ):
        """Create a new FFT MTF analysis.

        See Also
        --------
        FFTMTFSettings : Settings for the FFT MTF analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> DataFrame | None:
        """Run the FFT MTF analysis."""
        self.analysis.Settings.SampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.sampling)
        )
        self.analysis.set_surface(self.settings.surface)
        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.set_field(self.settings.field)
        self.analysis.Settings.Type = constants.process_constant(
            constants.Analysis.Settings.Mtf.MtfTypes, self.settings.mtf_type
        )
        self.analysis.Settings.MaximumFrequency = self.settings.maximum_frequency
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.UseDashes = self.settings.use_dashes
        self.analysis.Settings.ShowDiffractionLimit = self.settings.show_diffraction_limit

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        # Get results
        return self.get_data_series()
