from __future__ import annotations

from typing import Annotated, Literal

import numpy as np
from pydantic.dataclasses import Field

from zospy.analyses.new.decorators import analysis_settings
from zospy.analyses.new.parsers.types import FieldNumber, WavelengthNumber
from zospy.analyses.new.systemviewers.base import SystemViewerWrapper
from zospy.api import constants

__all__ = ("CrossSection", "CrossSectionSettings")


@analysis_settings
class CrossSectionSettings:
    """Settings for the cross section viewer."""

    start_surface: int = Field(default=1, ge=1, description="Starting surface number")
    end_surface: Literal[-1] | Annotated[int, Field(ge=1)] = Field(default=-1, description="Ending surface number")
    number_of_rays: int = Field(default=3, ge=1, description="Number of rays")
    y_stretch: float = Field(default=1.0, ge=0, description="Y stretch factor")
    fletch_rays: bool = Field(default=False, description="Fletch rays")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number")
    field: FieldNumber = Field(default="All", description="Field number")
    color_rays_by: str = Field(default="Fields", description="Color rays by")
    upper_pupil: float = Field(default=1.0, gt=-1, le=1, description="Upper pupil limit")
    lower_pupil: float = Field(default=-1.0, ge=-1, lt=1, description="Lower pupil limit")
    delete_vignetted: bool = Field(default=False, description="Delete vignetted rays")
    marginal_and_chief_only: bool = Field(default=False, description="Draw marginal and chief rays only")
    image_size: tuple[int, int] = Field(default=(800, 600), description="Image size")
    rays_line_thickness: str = Field(default="Standard", description="Rays line thickness")
    surface_line_thickness: str = Field(default="Standard", description="Surface line thickness")


class CrossSection(SystemViewerWrapper[CrossSectionSettings]):
    """Cross section viewer."""

    TYPE = "Draw2D"
    MODE = "Sequential"

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
        settings: CrossSectionSettings | None = None,
    ):
        """Initialize the cross section viewer."""
        super().__init__(settings or CrossSectionSettings(), locals())

    def configure_layout_tool(self) -> np.ndarray | None:
        """Run the cross section viewer."""
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
