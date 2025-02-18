"""3D system viewer."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import Field

from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import FieldNumber, WavelengthNumber, ZOSAPIConstant  # noqa: TCH001
from zospy.analyses.systemviewers.base import ImageSize, SystemViewerWrapper
from zospy.api import constants

if TYPE_CHECKING:
    from zospy.api import _ZOSAPI

__all__ = ("Viewer3D", "Viewer3DSettings")


@analysis_settings
class Viewer3DSettings:
    """Settings for the 3D system viewer.

    Attributes
    ----------
    start_surface : int, optional
        The starting surface index for the 3D viewer. Defaults to 1.
    end_surface : int, optional
        The ending surface index for the 3D viewer. A value of -1 indicates the last surface. Defaults to -1.
    number_of_rays : int, optional
        The number of rays to be used in the analysis. Defaults to 3.
    wavelength : int | str, optional
        The wavelength index to be used. Can be an integer or "All" for all wavelengths. Defaults to "All".
    field : int | str, optional
        The field index to be used. Can be an integer or "All" for all fields. Defaults to "All".
    ray_pattern : constants.Tools.General.RayPatternType | str, optional
        The ray pattern to be used in the analysis. Defaults to "XYFan".
    color_rays_by : constants.Tools.Layouts.ColorRaysByOptions | str, optional
        The criterion for coloring rays in the analysis. Defaults to "Fields".
    delete_vignetted : bool, optional
        Flag indicating whether to delete vignetted rays. Defaults to False.
    hide_lens_faces : bool, optional
        Flag indicating whether to hide lens faces. Defaults to False.
    hide_lens_edges : bool, optional
        Flag indicating whether to hide lens edges. Defaults to False.
    hide_x_bars : bool, optional
        Flag indicating whether to hide the x-component of lens faces. Defaults to False.
    draw_paraxial_pupils : bool, optional
        Flag indicating whether to draw paraxial entrance and exit pupils. Defaults to False.
    fletch_rays : bool, optional
        Flag indicating whether to draw small arrows indicating the direction of the rays. Defaults to False.
    split_nsc_rays : bool, optional
        Flag indicating whether to split rays from non-sequential sources at ray-surface intercepts. Defaults to False.
    scatter_nsc_rays : bool, optional
        Flag indicating whether to scatter rays from non-sequential sources at ray-surface intercepts.
        Defaults to False.
    draw_real_entrance_pupils : constants.Tools.Layouts.RealPupilOptions | str, optional
        How to draw real entrance pupils. Defaults to "Pupils_Off". Can be one of ['Pupils_Off', 'Pupils_4',
        'Pupils_8', 'Pupils_16', 'Pupils_32'].
    draw_real_exit_pupils : constants.Tools.Layouts.RealPupilOptions | str, optional
        How to draw real exit pupils. Defaults to "Pupils_Off". Can be one of ['Pupils_Off', 'Pupils_4', 'Pupils_8',
        'Pupils_16', 'Pupils_32'].
    surface_line_thickness : constants.Tools.Layouts.LineThicknessOptions | str, optional
        The thickness of the lines for the surfaces. Defaults to "Standard".
    rays_line_thickness : constants.Tools.Layouts.LineThicknessOptions | str, optional
        The thickness of the lines for the rays. Defaults to "Standard".
    configuration_all : bool, optional
        Flag indicating whether to use all configurations, if multiple configurations are present. Defaults to False.
        If multiple configurations are displayed, the `configuration_offset_*` parameters can be used to add offsets
        between the different configurations.
    configuration_current : bool, optional
        Flag indicating whether to only display the current configuration, when multiple configurations are present.
        Defaults to False.
    configuration_offset_x : float, optional
        The offset along the X-axis between configurations, if multiple configurations are present. Defaults to 0.
    configuration_offset_y : float, optional
        The offset along the Y-axis between configurations, if multiple configurations are present. Defaults to 0.
    configuration_offset_z : float, optional
        The offset along the Z-axis between configurations, if multiple configurations are present. Defaults to 0.
    camera_viewpoint_angle_x : float, optional
        Rotation of the system around the X-axis, in degrees. Defaults to 0.
    camera_viewpoint_angle_y : float, optional
        Rotation of the system around the Y-axis, in degrees. Defaults to 0.
    camera_viewpoint_angle_z : float, optional
        Rotation of the system around the Z-axis, in degrees. Defaults to 0.
    image_size : tuple[int, int], optional
        The size of the output image in pixels (width, height). Defaults to (800, 600).
    """

    start_surface: int = Field(default=1, ge=1, description="Starting surface number")
    end_surface: Literal[-1] | Annotated[int, Field(ge=1)] = Field(default=-1, description="Ending surface number")
    number_of_rays: int = Field(default=3, ge=1, description="Number of rays")
    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number")
    field: FieldNumber = Field(default="All", description="Field number")
    # ray_pattern: str = Field(default="XYFan", description="Ray pattern")
    ray_pattern: ZOSAPIConstant("Tools.General.RayPatternType") = Field(default="XYFan", description="Ray pattern")
    # color_rays_by: str = Field(default="Fields", description="Color rays by")
    color_rays_by: ZOSAPIConstant("Tools.Layouts.ColorRaysByOptions") = Field(
        default="Fields", description="Color rays by"
    )
    delete_vignetted: bool = Field(default=False, description="Delete vignetted rays")
    hide_lens_faces: bool = Field(default=False, description="Hide lens faces")
    hide_lens_edges: bool = Field(default=False, description="Hide lens edges")
    hide_x_bars: bool = Field(default=False, description="Hide X bars")
    draw_paraxial_pupils: bool = Field(default=False, description="Draw paraxial pupils")
    fletch_rays: bool = Field(default=False, description="Fletch rays")
    split_nsc_rays: bool = Field(default=False, description="Split NSC rays")
    scatter_nsc_rays: bool = Field(default=False, description="Scatter NSC rays")
    # draw_real_entrance_pupils: str = Field(default="Pupils_Off", description="Draw real entrance pupils")
    draw_real_entrance_pupils: ZOSAPIConstant("Tools.Layouts.RealPupilOptions") = Field(
        default="Pupils_Off", description="Draw real entrance pupils"
    )
    # draw_real_exit_pupils: str = Field(default="Pupils_Off", description="Draw real exit pupils")
    draw_real_exit_pupils: ZOSAPIConstant("Tools.Layouts.RealPupilOptions") = Field(
        default="Pupils_Off", description="Draw real exit pupils"
    )
    # surface_line_thickness: str = Field(default="Standard", description="Surface line thickness")
    surface_line_thickness: ZOSAPIConstant("Tools.Layouts.LineThicknessOptions") = Field(
        default="Standard", description="Surface line thickness"
    )
    # rays_line_thickness: str = Field(default="Standard", description="Rays line thickness")
    rays_line_thickness: ZOSAPIConstant("Tools.Layouts.LineThicknessOptions") = Field(
        default="Standard", description="Rays line thickness"
    )
    configuration_all: bool = Field(default=False, description="Draw all configurations")
    configuration_current: bool = Field(default=False, description="Draw only current configuration")
    configuration_offset_x: float = Field(default=0, description="Configuration X offset")
    configuration_offset_y: float = Field(default=0, description="Configuration Y offset")
    configuration_offset_z: float = Field(default=0, description="Configuration Z offset")
    camera_viewpoint_angle_x: float = Field(default=0, description="Camera viewpoint X angle")
    camera_viewpoint_angle_y: float = Field(default=0, description="Camera viewpoint Y angle")
    camera_viewpoint_angle_z: float = Field(default=0, description="Camera viewpoint Z angle")
    image_size: ImageSize = Field(default=(800, 600), description="Image size")


class Viewer3D(SystemViewerWrapper[Viewer3DSettings], analysis_type="Draw3D", mode="Sequential"):
    """3D system viewer."""

    def __init__(
        self,
        *,
        start_surface: int = 1,
        end_surface: int = -1,
        number_of_rays: int = 3,
        wavelength: int | Literal["All"] = "All",
        field: int | Literal["All"] = "All",
        ray_pattern: constants.Tools.General.RayPatternType | str = "XYFan",
        color_rays_by: constants.Tools.Layouts.ColorRaysByOptions | str = "Fields",
        delete_vignetted: bool = False,
        hide_lens_faces: bool = False,
        hide_lens_edges: bool = False,
        hide_x_bars: bool = False,
        draw_paraxial_pupils: bool = False,
        fletch_rays: bool = False,
        split_nsc_rays: bool = False,
        scatter_nsc_rays: bool = False,
        draw_real_entrance_pupils: constants.Tools.Layouts.RealPupilOptions | str = "Pupils_Off",
        draw_real_exit_pupils: constants.Tools.Layouts.RealPupilOptions | str = "Pupils_Off",
        surface_line_thickness: constants.Tools.Layouts.LineThicknessOptions | str = "Standard",
        rays_line_thickness: constants.Tools.Layouts.LineThicknessOptions | str = "Standard",
        configuration_all: bool = False,
        configuration_current: bool = False,
        configuration_offset_x: float = 0,
        configuration_offset_y: float = 0,
        configuration_offset_z: float = 0,
        camera_viewpoint_angle_x: float = 0,
        camera_viewpoint_angle_y: float = 0,
        camera_viewpoint_angle_z: float = 0,
        image_size: tuple[int, int] = (800, 600),
    ):
        """Create a new 3D system viewer.

        See Also
        --------
        Viewer3DSettings : Settings for the 3D system viewer.
        """
        super().__init__(settings_kws=locals())

    def configure_layout_tool(
        self,
    ) -> _ZOSAPI.Tools.Layouts.I3DViewerExport:
        """Configure the  3D viewer."""
        layout_tool = self.oss.Tools.Layouts.Open3DViewerExport()

        layout_tool.StartSurface = self.settings.start_surface
        layout_tool.EndSurface = self._validate_end_surface(self.settings.start_surface, self.settings.end_surface)
        layout_tool.NumberOfRays = self.settings.number_of_rays
        layout_tool.Wavelength = self._validate_wavelength(self.settings.wavelength)
        layout_tool.Field = self._validate_field(self.settings.field)
        layout_tool.RayPattern = constants.process_constant(
            constants.Tools.General.RayPatternType, self.settings.ray_pattern
        )
        layout_tool.ColorRaysBy = constants.process_constant(
            constants.Tools.Layouts.ColorRaysByOptions, self.settings.color_rays_by
        )
        layout_tool.DeleteVignetted = self.settings.delete_vignetted
        layout_tool.HideLensFaces = self.settings.hide_lens_faces
        layout_tool.HideLensEdges = self.settings.hide_lens_edges
        layout_tool.HideXBars = self.settings.hide_x_bars
        layout_tool.DrawParaxialPupils = self.settings.draw_paraxial_pupils
        layout_tool.FletchRays = self.settings.fletch_rays
        layout_tool.SplitNSCRays = self.settings.split_nsc_rays
        layout_tool.ScatterNSCRays = self.settings.scatter_nsc_rays
        layout_tool.DrawRealEntrancePupils = constants.process_constant(
            constants.Tools.Layouts.RealPupilOptions, self.settings.draw_real_entrance_pupils
        )
        layout_tool.DrawRealExitPupils = constants.process_constant(
            constants.Tools.Layouts.RealPupilOptions, self.settings.draw_real_exit_pupils
        )
        layout_tool.SurfaceLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, self.settings.surface_line_thickness
        )
        layout_tool.RaysLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, self.settings.rays_line_thickness
        )
        layout_tool.ConfigurationAll = self.settings.configuration_all
        layout_tool.ConfigurationCurrent = self.settings.configuration_current
        layout_tool.ConfigurationOffsetX = self.settings.configuration_offset_x
        layout_tool.ConfigurationOffsetY = self.settings.configuration_offset_y
        layout_tool.ConfigurationOffsetZ = self.settings.configuration_offset_z
        layout_tool.CameraViewpointAngleX = self.settings.camera_viewpoint_angle_x
        layout_tool.CameraViewpointAngleY = self.settings.camera_viewpoint_angle_y
        layout_tool.CameraViewpointAngleZ = self.settings.camera_viewpoint_angle_z
        layout_tool.OutputPixelWidth, layout_tool.OutputPixelHeight = self.settings.image_size

        return layout_tool
