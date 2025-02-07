"""Cross section (2D) viewer."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal

from pydantic.dataclasses import Field

from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import FieldNumber, WavelengthNumber, ZOSAPIConstant  # noqa: TCH001
from zospy.analyses.systemviewers.base import ImageSize, SystemViewerWrapper
from zospy.api import constants

if TYPE_CHECKING:
    from zospy.api import _ZOSAPI

__all__ = ("CrossSection", "CrossSectionSettings")


@analysis_settings
class CrossSectionSettings:
    """Settings for the cross section viewer.

    Attributes
    ----------
    start_surface : int, optional
        The starting surface index for the cross-section analysis. Defaults to 1.
    end_surface : int, optional
        The ending surface index for the cross-section analysis. A value of -1 indicates the last surface.
        Defaults to -1.
    number_of_rays : int, optional
        The number of rays to be used in the analysis. Defaults to 3.
    y_stretch : float, optional
        The stretch factor in the Y-axis for the analysis visualization. Defaults to 1.0.
    fletch_rays : bool, optional
        Flag indicating whether to fletch rays. Defaults to False.
    wavelength : int | str, optional
        The wavelength index to be used. Can be an integer or "all" for all wavelengths. Defaults to "all".
    field : int | str, optional
        The field index to be used. Can be an integer or "all" for all fields. Defaults to "all".
    color_rays_by : constants.Tools.Layouts.ColorRaysByCrossSectionOptions | str, optional
        The criterion for coloring rays in the analysis. Defaults to "Fields".
    upper_pupil : float, optional
        The upper pupil limit for the analysis. Defaults to 1.
    lower_pupil : float, optional
        The lower pupil limit for the analysis. Defaults to -1.
    delete_vignetted : bool, optional
        Flag indicating whether to delete vignetted rays. Defaults to False.
    marginal_and_chief_only : bool, optional
        Flag indicating whether to include only marginal and chief rays in the analysis. Defaults to False.
    image_size : tuple[int, int], optional
        The size of the output image in pixels (width, height). Defaults to (800, 600).
    rays_line_thickness : constants.Tools.Layouts.LineThicknessOptions | str, optional
        The thickness of the lines in the output visualization. Defaults to "Standard".
    surface_line_thickness : constants.Tools.Layouts.LineThicknessOptions | str, optional
        The thickness of the surface lines in the output visualization. Defaults to "Standard".
    """

    start_surface: int = Field(default=1, ge=1, description="Starting surface number")
    end_surface: Literal[-1] | Annotated[int, Field(ge=1)] = Field(default=-1, description="Ending surface number")
    number_of_rays: int = Field(default=3, ge=1, description="Number of rays")
    y_stretch: float = Field(default=1.0, ge=0, description="Y stretch factor")
    fletch_rays: bool = Field(default=False, description="Fletch rays")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number")
    field: FieldNumber = Field(default="All", description="Field number")
    color_rays_by: ZOSAPIConstant("Tools.Layouts.ColorRaysByCrossSectionOptions") = Field(
        default="Fields", description="Color rays by"
    )
    upper_pupil: float = Field(default=1.0, gt=-1, le=1, description="Upper pupil limit")
    lower_pupil: float = Field(default=-1.0, ge=-1, lt=1, description="Lower pupil limit")
    delete_vignetted: bool = Field(default=False, description="Delete vignetted rays")
    marginal_and_chief_only: bool = Field(default=False, description="Draw marginal and chief rays only")
    image_size: ImageSize = Field(default=(800, 600), description="Image size")
    rays_line_thickness: ZOSAPIConstant("Tools.Layouts.LineThicknessOptions") = Field(
        default="Standard", description="Rays line thickness"
    )
    surface_line_thickness: ZOSAPIConstant("Tools.Layouts.LineThicknessOptions") = Field(
        default="Standard", description="Surface line thickness"
    )


class CrossSection(SystemViewerWrapper[CrossSectionSettings], analysis_type="Draw2D", mode="Sequential"):
    """Cross section viewer."""

    def __init__(
        self,
        *,
        start_surface: int = 1,
        end_surface: int = -1,
        number_of_rays: int = 3,
        y_stretch: float = 1.0,
        fletch_rays: bool = False,
        wavelength: int | Literal["All"] = "All",
        field: int | Literal["All"] = "All",
        color_rays_by: constants.Tools.Layouts.ColorRaysByCrossSectionOptions | str = "Fields",
        upper_pupil: float = 1.0,
        lower_pupil: float = -1.0,
        delete_vignetted: bool = False,
        marginal_and_chief_only: bool = False,
        image_size: tuple[int, int] = (800, 600),
        rays_line_thickness: constants.Tools.Layouts.LineThicknessOptions | str = "Standard",
        surface_line_thickness: constants.Tools.Layouts.LineThicknessOptions | str = "Standard",
    ):
        """Create a new cross section viewer.

        See Also
        --------
        CrossSectionSettings : Settings for the cross section viewer.
        """
        super().__init__(settings_kws=locals())

    def configure_layout_tool(self) -> _ZOSAPI.Tools.Layouts.ICrossSectionExport:
        """Configure the cross section viewer."""
        layout_tool = self.oss.Tools.Layouts.OpenCrossSectionExport()
        layout_tool.StartSurface = self.settings.start_surface
        layout_tool.EndSurface = self._validate_end_surface(self.settings.start_surface, self.settings.end_surface)
        layout_tool.NumberOfRays = self.settings.number_of_rays
        layout_tool.YStretch = self.settings.y_stretch
        layout_tool.FletchRays = self.settings.fletch_rays
        layout_tool.Wavelength = self._validate_wavelength(self.settings.wavelength)
        layout_tool.Field = self._validate_field(self.settings.field)
        layout_tool.ColorRaysBy = constants.process_constant(
            constants.Tools.Layouts.ColorRaysByCrossSectionOptions, self.settings.color_rays_by
        )
        layout_tool.UpperPupil = self.settings.upper_pupil
        layout_tool.LowerPupil = self.settings.lower_pupil
        layout_tool.DeleteVignetted = self.settings.delete_vignetted
        layout_tool.MarginalAndChiefOnly = self.settings.marginal_and_chief_only
        layout_tool.OutputPixelHeight, layout_tool.OutputPixelWidth = self.settings.image_size
        layout_tool.RaysLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, self.settings.rays_line_thickness
        )
        layout_tool.SurfaceLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, self.settings.surface_line_thickness
        )

        return layout_tool
