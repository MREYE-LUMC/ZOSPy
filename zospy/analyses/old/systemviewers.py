"""Zemax OpticStudio System Viewers."""

from __future__ import annotations

from inspect import signature
from os import PathLike
from typing import Any, Callable
from warnings import warn

import numpy as np
from System import Array

from zospy.analyses.old.base import AnalysisResult, OnComplete, new_analysis
from zospy.api import _ZOSAPI, constants
from zospy.utils.pyutils import abspath
from zospy.zpcore import OpticStudioSystem


def _warn_specified_parameters(
    oss: OpticStudioSystem,
    variables: dict,
    function: Callable[[Any], Any],
    ignore: tuple[str, ...] = ("oss", "oncomplete"),
) -> None:
    """Check if unsupported parameters are specified and warn the user.

    For OpticStudio versions below 24R1, compare the values of a dictionary with the default values of a function,
    and warn if any are different.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance.
    variables : dict
        A dictionary of variables to compare with the default values of the function. Can be obtained using `locals()`.
    function : Callable[[Any], Any]
        The function to compare the variables with.
    ignore : tuple[str], optional
        A tuple of parameter names to ignore. Defaults to ("oss", "oncomplete").

    Examples
    --------
    >>> def test_func(a=1, b=2, c=3):
    ...     _warn_specified_parameters(oss, locals(), test_func)
    """
    if oss.ZOS.version >= (24, 1, 0):
        return

    changed_parameters = []

    for key, value in signature(function).parameters.items():
        if key in ignore:
            continue

        if variables[key] != value.default:
            changed_parameters.append(key)

    if len(changed_parameters) > 0:
        warn(
            f"Some parameters were specified but ignored, because viewer exports are only supported from OpticStudio"
            f"24R1: {', '.join(changed_parameters)}"
        )


def _close_current_tool(oss: OpticStudioSystem) -> None:
    """Close the current tool in OpticStudio."""
    if oss.Tools.CurrentTool is not None:
        oss.Tools.CurrentTool.Close()


def _validate_wavelength(oss: OpticStudioSystem, wavelength: int | str) -> int:
    if isinstance(wavelength, str):
        if wavelength == "all":
            return -1

        raise ValueError("wavelength must be an integer or 'all'.")

    if wavelength < -1 or wavelength > oss.SystemData.Wavelengths.NumberOfWavelengths:
        raise ValueError("wavelength must be -1 or between 1 and the number of wavelengths.")

    return wavelength


def _validate_field(oss: OpticStudioSystem, field: int | str) -> int:
    if isinstance(field, str):
        if field == "all":
            return -1

        raise ValueError("field must be an integer or 'all'.")

    if field < 1 or field > oss.SystemData.Fields.NumberOfFields:
        raise ValueError("field must be -1 or between 1 and the number of fields.")

    return field


ALLOWED_IMAGE_EXTENSIONS: tuple[str, ...] = ("bmp", "jpeg", "png")


def _validate_path(path: PathLike | str) -> str:
    str_path = abspath(path, check_directory_only=True)

    if str_path.split(".")[-1] in ALLOWED_IMAGE_EXTENSIONS:
        return str_path

    raise ValueError(f"Image file must have one of the following extensions: {ALLOWED_IMAGE_EXTENSIONS}")


def _get_image_data(image_data: _ZOSAPI.Tools.Layouts.IImageExportData | None) -> np.ndarray | None:
    if image_data is None:
        return image_data

    image_size = image_data.Width * image_data.Height

    # In-place updating arrays works only with dotnet arrays
    r_values = Array[int](image_size)  # [0] * image_size
    g_values = Array[int](image_size)  # [0] * image_size
    b_values = Array[int](image_size)  # [0] * image_size

    image_data.FillValues(image_data.Width * image_data.Height, r_values, g_values, b_values)

    return np.stack((r_values, g_values, b_values), axis=-1).reshape(image_data.Height, image_data.Width, 3)


def cross_section(
    oss: OpticStudioSystem,
    start_surface: int = 1,
    end_surface: int = -1,
    number_of_rays: int = 3,
    y_stretch: float = 1.0,
    fletch_rays: bool = False,
    wavelength: int | str = "all",
    field: int | str = "all",
    color_rays_by: constants.Tools.Layouts.ColorRaysByCrossSectionOptions | str = "Fields",
    upper_pupil: float = 1,
    lower_pupil: float = -1,
    delete_vignetted: bool = False,
    marginal_and_chief_only: bool = False,
    image_size: tuple[int, int] = (800, 600),
    line_thickness: constants.Tools.Layouts.LineThicknessOptions | str = "Standard",
    imgoutfile: PathLike | str | None = None,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Cross-Section viewer.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
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
    line_thickness : constants.Tools.Layouts.LineThicknessOptions | str, optional
        The thickness of the lines in the output visualization. Defaults to "Standard".
    imgoutfile : PathLike | str | None, optional
        The path to save the output image file. If None, no image is saved. Defaults to None.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A Cross-Section analysis result. If `imgoutfile` is `None`, the result will contain the image data as a numpy
        array. If `imgoutfile` is not `None`, the results `Data` attribute will be empty.
    """
    _warn_specified_parameters(oss, locals(), cross_section)

    if start_surface < -1:
        raise ValueError("start_surface must be greater than or equal to -1.")

    if end_surface != -1 and end_surface <= start_surface or end_surface > oss.LDE.NumberOfSurfaces - 1:
        raise ValueError("end_surface must be -1 or greater than start_surface and less than the number of surfaces.")

    if end_surface == -1:
        # According to the documentation the ZOS-API should interpret -1 as the last surface,
        # but instead it interprets it as the first surface after the start surface.
        end_surface = oss.LDE.NumberOfSurfaces - 1

    if number_of_rays < 1:
        raise ValueError("number_of_rays must be greater than 0.")

    if y_stretch < 0:
        raise ValueError("y_stretch must be greater than or equal to 0.")

    wavelength = _validate_wavelength(oss, wavelength)
    field = _validate_field(oss, field)

    analysis_type = constants.Analysis.AnalysisIDM.Draw2D

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    if oss.ZOS.version >= (24, 1, 0):
        _close_current_tool(oss)

        layout_tool = oss.Tools.Layouts.OpenCrossSectionExport()
        layout_tool.StartSurface = start_surface
        layout_tool.EndSurface = end_surface
        layout_tool.NumberOfRays = number_of_rays
        layout_tool.YStretch = y_stretch
        layout_tool.FletchRays = fletch_rays
        layout_tool.Wavelength = wavelength
        layout_tool.Field = field
        layout_tool.ColorRaysBy = constants.process_constant(
            constants.Tools.Layouts.ColorRaysByCrossSectionOptions, color_rays_by
        )
        layout_tool.UpperPupil = upper_pupil
        layout_tool.LowerPupil = lower_pupil
        layout_tool.DeleteVignetted = delete_vignetted
        layout_tool.MarginalAndChiefOnly = marginal_and_chief_only
        layout_tool.OutputPixelWidth, layout_tool.OutputPixelHeight = image_size
        layout_tool.RaysLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, line_thickness
        )

        if imgoutfile is not None:
            layout_tool.SaveImageAsFile = True
            layout_tool.OutputFileName = _validate_path(imgoutfile)
        else:
            layout_tool.SaveImageAsFile = False

        layout_tool.RunAndWaitForCompletion()

        if not layout_tool.Succeeded:
            raise RuntimeError("The cross-section export tool failed to run.")

        image_data = _get_image_data(layout_tool.ImageExportData) if imgoutfile is None else None
    else:
        image_data = None

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=image_data,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def viewer_3d(
    oss: OpticStudioSystem,
    start_surface: int = 1,
    end_surface: int = -1,
    number_of_rays: int = 3,
    wavelength: int | str = "all",
    field: int | str = "all",
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
    ray_line_thickness: constants.Tools.Layouts.LineThicknessOptions | str = "Standard",
    configuration_all: bool = False,
    configuration_current: bool = False,
    configuration_offset_x: float = 0,
    configuration_offset_y: float = 0,
    configuration_offset_z: float = 0,
    camera_viewpoint_angle_x: float = 0,
    camera_viewpoint_angle_y: float = 0,
    camera_viewpoint_angle_z: float = 0,
    imgoutfile: PathLike | str | None = None,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio 3D Viewer.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    start_surface : int, optional
        The starting surface index for the 3D viewer. Defaults to 1.
    end_surface : int, optional
        The ending surface index for the 3D viewer. A value of -1 indicates the last surface. Defaults to -1.
    number_of_rays : int, optional
        The number of rays to be used in the analysis. Defaults to 3.
    wavelength : int | str, optional
        The wavelength index to be used. Can be an integer or "all" for all wavelengths. Defaults to "all".
    field : int | str, optional
        The field index to be used. Can be an integer or "all" for all fields. Defaults to "all".
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
    ray_line_thickness : constants.Tools.Layouts.LineThicknessOptions | str, optional
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
    imgoutfile : PathLike | str | None, optional
        The path to save the output image file. If None, no image is saved. Defaults to None.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A Viewer 3D analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    _warn_specified_parameters(oss, locals(), viewer_3d)

    if start_surface < -1:
        raise ValueError("start_surface must be greater than or equal to -1.")

    if end_surface != -1 and end_surface <= start_surface or end_surface > oss.LDE.NumberOfSurfaces - 1:
        raise ValueError("end_surface must be -1 or greater than start_surface and less than the number of surfaces.")

    if end_surface == -1:
        # According to the documentation the ZOS-API should interpret -1 as the last surface,
        # but instead it interprets it as the first surface after the start surface.
        end_surface = oss.LDE.NumberOfSurfaces - 1

    if number_of_rays < 1:
        raise ValueError("number_of_rays must be greater than 0.")

    analysis_type = constants.Analysis.AnalysisIDM.Draw3D

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    if oss.ZOS.version >= (24, 1, 0):
        _close_current_tool(oss)

        layout_tool = oss.Tools.Layouts.Open3DViewerExport()

        layout_tool.StartSurface = start_surface
        layout_tool.EndSurface = end_surface
        layout_tool.NumberOfRays = number_of_rays
        layout_tool.Wavelength = _validate_wavelength(oss, wavelength)
        layout_tool.Field = _validate_field(oss, field)
        layout_tool.RayPattern = constants.process_constant(constants.Tools.General.RayPatternType, ray_pattern)
        layout_tool.ColorRaysBy = constants.process_constant(constants.Tools.Layouts.ColorRaysByOptions, color_rays_by)
        layout_tool.DeleteVignetted = delete_vignetted
        layout_tool.HideLensFaces = hide_lens_faces
        layout_tool.HideLensEdges = hide_lens_edges
        layout_tool.HideXBars = hide_x_bars
        layout_tool.DrawParaxialPupils = draw_paraxial_pupils
        layout_tool.FletchRays = fletch_rays
        layout_tool.SplitNSCRays = split_nsc_rays
        layout_tool.ScatterNSCRays = scatter_nsc_rays
        layout_tool.DrawRealEntrancePupils = constants.process_constant(
            constants.Tools.Layouts.RealPupilOptions, draw_real_entrance_pupils
        )
        layout_tool.DrawRealExitPupils = constants.process_constant(
            constants.Tools.Layouts.RealPupilOptions, draw_real_exit_pupils
        )
        layout_tool.SurfaceLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, surface_line_thickness
        )
        layout_tool.RaysLineThickness = constants.process_constant(
            constants.Tools.Layouts.LineThicknessOptions, ray_line_thickness
        )
        layout_tool.ConfigurationAll = configuration_all
        layout_tool.ConfigurationCurrent = configuration_current
        layout_tool.ConfigurationOffsetX = configuration_offset_x
        layout_tool.ConfigurationOffsetY = configuration_offset_y
        layout_tool.ConfigurationOffsetZ = configuration_offset_z
        layout_tool.CameraViewpointAngleX = camera_viewpoint_angle_x
        layout_tool.CameraViewpointAngleY = camera_viewpoint_angle_y
        layout_tool.CameraViewpointAngleZ = camera_viewpoint_angle_z

        if imgoutfile is not None:
            layout_tool.SaveImageAsFile = True
            layout_tool.OutputFileName = _validate_path(imgoutfile)
        else:
            layout_tool.SaveImageAsFile = False

        layout_tool.RunAndWaitForCompletion()

        if not layout_tool.Succeeded:
            raise RuntimeError("The 3D viewer export tool failed to run.")

        image_data = _get_image_data(layout_tool.ImageExportData) if imgoutfile is None else None
    else:
        image_data = None

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=image_data,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def shaded_model(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Shaded Model Viewer.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A Shaded Model analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.ShadedModel

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def nsc_3d_layout(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio NSC 3D Layout viewer.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be non-sequential.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A NSC 3D Layout analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.NSC3DLayout

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def nsc_shaded_model(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio NSC Shaded Model Viewer.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be non-sequential.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A NSC Shaded Model analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.NSCShadedModel

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)
