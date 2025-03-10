"""Huygens PSF analysis."""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import FieldNumber, WavelengthNumber  # noqa: TCH001
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling

__all__ = ("HuygensPSF", "HuygensPSFSettings")


@analysis_settings
class HuygensPSFSettings:
    """Settings for the Huygens PSF analysis.

    Attributes
    ----------
    pupil_sampling : str | int
        The pupil sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
        integer.
    image_sampling : str | int
        The image sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
        integer.
    image_delta : float | int
        The image delta
    rotation : int
        The rotation, should be one of [0, 90, 180, 270].
    wavelength : str | int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number.
        Defaults to 'All'.
    field : str | int
        The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 1.
    psf_type : str
        The PSF type (e.g. 'Linear') that is calculated. Defaults to 'Linear'.
    show_as : str
        Defines how the data is shown within OpticStudio. Defaults to 'Surface'
    use_polarization : bool
        Defines if polarization is used. Defaults to `False`.
    use_centroid : bool
        Defines if centroid is used. Defaults to `False`.
    normalize : bool
        Defines if normalization is used. Defaults to `False`.
    """

    pupil_sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Pupil Sampling")
    image_sampling: str | Annotated[int, Field(ge=0)] = Field(default="32x32", description="Image Sampling")
    image_delta: float = Field(default=0, description="Image Delta")
    rotation: Literal[0, 90, 180, 270] = Field(default=0, description="Rotation")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number or 'All'")
    field: FieldNumber = Field(default=1, description="Field number or 'All'")
    psf_type: str = Field(default="Linear", description="PSF type")
    show_as: str = Field(default="Surface", description="Show as")
    use_polarization: bool = Field(default=False, description="Use polarization")
    use_centroid: bool = Field(default=False, description="Use centroid")
    normalize: bool = Field(default=False, description="Normalize")


class HuygensPSF(BaseAnalysisWrapper[Union[DataFrame, None], HuygensPSFSettings], analysis_type="HuygensPsf"):
    """Huygens Point Spread Function (PSF) analysis."""

    def __init__(
        self,
        *,
        pupil_sampling: str | int = "32x32",
        image_sampling: str | int = "32x32",
        image_delta: float = 0,
        rotation: int = 0,
        wavelength: str | int = "All",
        field: str | int = 1,
        psf_type: str | constants.Analysis.Settings.HuygensPsfTypes = "Linear",
        show_as: str | constants.Analysis.HuygensShowAsTypes = "Surface",
        use_polarization: bool = False,
        use_centroid: bool = False,
        normalize: bool = False,
    ):
        """Create a new Huygens PSF analysis.

        See Also
        --------
        HuygensPSFSettings : Settings for the Huygens PSF analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> DataFrame | None:
        """Run the Huygens PSF analysis."""
        self.analysis.Settings.PupilSampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.pupil_sampling)
        )
        self.analysis.Settings.ImageSampleSize = getattr(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.image_sampling)
        )
        self.analysis.Settings.ImageDelta = self.settings.image_delta
        self.analysis.Settings.Rotation = getattr(
            constants.Analysis.Settings.Rotations, f"Rotate_{self.settings.rotation}"
        )
        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.set_field(self.settings.field)
        self.analysis.Settings.Type = constants.process_constant(
            constants.Analysis.Settings.HuygensPsfTypes, self.settings.psf_type
        )
        self.analysis.Settings.ShowAsType = constants.process_constant(
            constants.Analysis.HuygensShowAsTypes, self.settings.show_as
        )
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.UseCentroid = self.settings.use_centroid
        self.analysis.Settings.Normalize = self.settings.normalize

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        return self.get_data_grid(cell_origin="bottom_left")
