from __future__ import annotations

from typing import Annotated, Literal

from pandas import DataFrame
from pydantic import Field

from zospy.analyses.new.base import BaseAnalysisWrapper
from zospy.analyses.new.decorators import analysis_settings
from zospy.analyses.new.parsers.types import ZOSAPIConstant
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling


@analysis_settings
class WavefrontMapSettings:
    """Settings for the Wavefront Map analysis.

    Attributes
    ----------
    field : int
        The field that is to be analyzed. Defaults to 1.
    surface  str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    wavelength : int
        The wavelength number to use for the analysis. Defaults to 1.
    show_as : constants.Analysis.ShowAs | str
        Defines the output plot format. Defaults to 'Surface'.
    rotation : constants.Analysis.Settings.Rotations | str
        The rotation or surface plots for viewing. Defaults to 'Rotate_0'.
    sampling : str
        The sampling. Defaults to '64x64'.
    polarization : constants.Analysis.Settings.Polarizations | str | None
        The polarization that is accounted for. When set to None, polarization is ignored. Defaults to None.
    reference_to_primary : bool
        Defines whether the aberrations are referenced to the reference sphere for the used wavelength or for the
        primary wavelength. If True, the reference sphere for the primary wavelength is used. Defaults to False.
    use_exit_pupil : bool
        Defines whether the exit pupil shape is used. Defaults to True.
    remove_tilt : bool
        Defines whether linear x- and y-tilt is removed from the data. Defaults to False.
    scale : float
        The scale factor for surface plots. Defaults to False.
    sub_aperture_x : float
        The sub-aperture x coordinate. Defaults to 0.0
    sub_aperture_y : float
        The sub-aperture y coordinate. Defaults to 0.0
    sub_aperture_r : float
        The sub-aperture radius. Defaults to 1.0
    contour_format : str
        The contour format. Only used when show-As is set to 'Contour'. If set to an empty string, OpticStdio ignores
        it. Defaults to ''.
    """

    field: int = Field(default=1, ge=1, description="Field number")
    surface: Literal["Object", "Image"] | Annotated[int, Field(ge=1)] = Field(
        default="Image", description="Surface number"
    )
    wavelength: int = Field(default=1, ge=1, description="Wavelength number")
    show_as: ZOSAPIConstant("Analysis.ShowAs") = Field(default="Surface", description="Show as")
    rotation: ZOSAPIConstant("Analysis.Settings.Rotations") = Field(default="Rotate_0", description="Rotation")
    sampling: str = Field(default="64x64", description="Sampling grid")
    polarization: ZOSAPIConstant("Analysis.Settings.Polarizations") | None = Field(
        default=None, description="Polarization"
    )
    reference_to_primary: bool = Field(default=False, description="Reference to primary wavelength")
    use_exit_pupil: bool = Field(default=True, description="Use exit pupil shape")
    remove_tilt: bool = Field(default=False, description="Remove linear tilt from the data")
    scale: float = Field(default=1.0, description="Scale factor for the surface plots")
    sub_aperture_x: float = Field(default=0.0, description="Sub aperture X coordinate")
    sub_aperture_y: float = Field(default=0.0, description="Sub aperture Y coordinate")
    sub_aperture_r: float = Field(default=1.0, description="Sub aperture radius")
    contour_format: str = Field(default="", description="Contour format")


class WavefrontMap(BaseAnalysisWrapper[DataFrame, WavefrontMapSettings]):
    """Wavefront Map analysis."""

    TYPE = "WavefrontMap"

    _needs_config_file = False
    _needs_text_output_file = False

    def __init__(
        self,
        *,
        field: int = 1,
        surface: Literal["Object", "Image"] | int = "Image",
        wavelength: int = 1,
        show_as: constants.Analysis.ShowAs = "Surface",
        rotation: constants.Analysis.Settings.Rotations = "Rotate_0",
        sampling: constants.Analysis.SampleSizes = "64x64",
        polarization: constants.Analysis.Settings.Polarizations | None = None,
        reference_to_primary: bool = False,
        use_exit_pupil: bool = True,
        remove_tilt: bool = False,
        scale: float = 1.0,
        sub_aperture_x: float = 0.0,
        sub_aperture_y: float = 0.0,
        sub_aperture_r: float = 1.0,
        contour_format: str = "",
        settings: WavefrontMapSettings | None = None,
    ):
        super().__init__(settings or WavefrontMapSettings(), locals())

    def run_analysis(self) -> DataFrame:
        """Run the Wavefront Map analysis.

        See Also
        --------
        WavefrontMapSettings : Settings for the Wavefront Map analysis.
        """
        self.analysis.field = self.settings.field
        self.analysis.surface = self.settings.surface
        self.analysis.wavelength = self.settings.wavelength
        self.analysis.ShowAs = constants.process_constant(constants.Analysis.ShowAs, self.settings.show_as)
        self.analysis.Rotation = constants.process_constant(
            constants.Analysis.Settings.Rotations, self.settings.rotation
        )
        self.analysis.Sampling = constants.process_constant(
            constants.Analysis.SampleSizes, standardize_sampling(self.settings.sampling)
        )
        self.analysis.Polarization = constants.process_constant(
            constants.Analysis.Settings.Polarizations, self.settings.polarization
        )
        self.analysis.ReferenceToPrimary = self.settings.reference_to_primary
        self.analysis.UseExitPupil = self.settings.use_exit_pupil
        self.analysis.RemoveTilt = self.settings.remove_tilt
        self.analysis.Scale = self.settings.scale
        self.analysis.Subaperture_X = self.settings.sub_aperture_x
        self.analysis.Subaperture_Y = self.settings.sub_aperture_y
        self.analysis.Subaperture_R = self.settings.sub_aperture_r
        self.analysis.ContourFormat = self.settings.contour_format

        self.analysis.ApplyAndWaitForCompletion()

        return self.get_data_grid()