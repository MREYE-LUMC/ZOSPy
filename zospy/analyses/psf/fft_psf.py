"""FFT PSF analysis."""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import WavelengthNumber, ZOSAPIConstant  # noqa: TCH001
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling

__all__ = ("FFTPSF", "FFTPSFSettings")


@analysis_settings
class FFTPSFSettings:
    """Settings for the FFT PSF analysis.

    Attributes
    ----------
    sampling : str | int
        The size of the ray grid used to sample the pupil, either string (e.g. '32x32') or int (e.g. 32).
    display : str | int
        Size of the display grid, either string (e.g. '32x32') or int (e.g. 32). This can be up to twice the size of the
        sampling grid.
    rotation : int
        Plot rotation in degrees, should be one of [0, 90, 180, 270].
    wavelength : str | int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number.
        Defaults to 'All'.
    field : str | int
        The field number that is to be used. Defaults to 1.
    psf_type : str
        The PSF type (e.g. 'Linear') that is calculated. Defaults to 'Linear'.
    use_polarization : bool
        Defines if polarization is used. Defaults to `False`.
    image_delta : float | int
        The delta distance between points in image space, in μm. Defaults to 0.
    normalize : bool
        Defines if normalization is used. Defaults to `False`.
    surface : str | int
        Surface at which the PSF is calculated. Either 'Image' or an integer specifying the surface number.
    """

    sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Pupil Sampling")
    display: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Display size")
    rotation: Literal[0, 90, 180, 270] = Field(default=0, description="Plot rotation angle")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number or 'All'")
    field: int = Field(default=1, ge=1, description="Field number")
    psf_type: ZOSAPIConstant("Analysis.Settings.Psf.FftPsfType") = Field(default="Linear", description="PSF type")
    use_polarization: bool = Field(default=False, description="Use polarization")
    image_delta: float = Field(default=0, description="Image Delta")
    normalize: bool = Field(default=False, description="Normalize")
    surface: Literal["Image"] | Annotated[int, Field(ge=0)] = Field(default="Image", description="PSF surface")


class FFTPSF(BaseAnalysisWrapper[Union[DataFrame, None], FFTPSFSettings], analysis_type="FftPsf"):
    """FFT Point Spread Function (PSF) analysis."""

    def __init__(
        self,
        *,
        sampling: str | int = "32x32",
        display: str | int = "32x32",
        rotation: Literal[0, 90, 180, 270] = 0,
        wavelength: WavelengthNumber = "All",
        field: int = 1,
        psf_type: str | constants.Analysis.Settings.Psf.FftPsfType = "Linear",
        use_polarization: bool = False,
        image_delta: float = 0,
        normalize: bool = False,
        surface: Literal["Image"] | int = "Image",
    ):
        """Create a new FFT PSF analysis.

        See Also
        --------
        FFTPSFSettings : Settings for the FFT PSF analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> DataFrame | None:
        """Run the FFT PSF analysis."""
        self.analysis.Settings.SampleSize = getattr(
            constants.Analysis.Settings.Psf.PsfSampling, standardize_sampling(self.settings.sampling, prefix="PsfS")
        )
        self.analysis.Settings.OutputSize = getattr(
            constants.Analysis.Settings.Psf.PsfSampling, standardize_sampling(self.settings.display, prefix="PsfS")
        )
        self.analysis.Settings.Rotation = getattr(
            constants.Analysis.Settings.Psf.PsfRotation, "CW" + str(self.settings.rotation)
        )
        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.set_field(self.settings.field)
        self.analysis.Settings.Type = constants.process_constant(
            constants.Analysis.Settings.Psf.FftPsfType, self.settings.psf_type
        )
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.ImageDelta = self.settings.image_delta
        self.analysis.Settings.Normalize = self.settings.normalize
        self.analysis.set_surface(self.settings.surface)

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        return self.get_data_grid(cell_origin="bottom_left")
