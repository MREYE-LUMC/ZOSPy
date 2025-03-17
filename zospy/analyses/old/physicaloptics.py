"""Zemax OpticStudio analyses from the Physical Optics category."""

from __future__ import annotations

import warnings
from typing import Literal

import pandas as pd

from zospy import utils
from zospy.analyses.old.base import Analysis, AnalysisResult, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def pop_create_beam_parameter_dict(
    oss: OpticStudioSystem, beam_type: constants.Analysis.PhysicalOptics.POPBeamTypes | str = "GaussianWaist"
) -> dict:
    """Creates a dictionary containing the parameters for a certain Physical Optics beam type and their default values.

    The dictionary can be adjusted and supplied to the beam_parameters argument of physical_optics_propagation()

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    beam_type : constants.Analysis.PhysicalOptics.POPBeamTypes | str
        The beam type. Defaults to 'GaussianWaist'.

    Returns
    -------
    dict
        A dictionary containing the parameters for a certain Physical Optics beam type and their default values.
    """
    analysis_type = constants.Analysis.AnalysisIDM.PhysicalOpticsPropagation

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    analysis.Settings.BeamType = constants.process_constant(constants.Analysis.PhysicalOptics.POPBeamTypes, beam_type)

    beam_params = {}
    for i in range(analysis.Settings.NumberOfParameters):
        beam_params[analysis.Settings.GetParameterName(i)] = analysis.Settings.GetParameterValue(i)

    analysis.Close()

    return beam_params


def pop_create_fiber_parameter_dict(
    oss: OpticStudioSystem, fiber_type: constants.Analysis.PhysicalOptics.POPFiberTypes | str = "GaussianWaist"
) -> dict:
    """Creates a dictionary containing the parameters for a certain Physical Optics fiber type and their default values.

     The dictionary can be adjusted and supplied to the fiber_parameters argument of physical_optics_propagation()

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    fiber_type : constants.Analysis.PhysicalOptics.POPFiberTypes | str
         The fiber type. Defaults to 'GaussianWaist'.

    Returns
    -------
    dict
        A dictionary containing the parameters for a certain Physical Optics fiber type and their default values.
    """
    analysis_type = constants.Analysis.AnalysisIDM.PhysicalOpticsPropagation

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    analysis.Settings.FiberType = constants.process_constant(
        constants.Analysis.PhysicalOptics.POPFiberTypes, fiber_type
    )

    fiber_params = {}
    for i in range(analysis.Settings.NumberOfFiberParameters):
        fiber_params[analysis.Settings.GetFiberParameterName(i)] = analysis.Settings.GetFiberParameterValue(i)

    analysis.Close()

    return fiber_params


def _set_pop_parameters(analysis: Analysis, which: Literal["beam", "fiber"], parameters: dict) -> None:
    """Sets beam or fiber parameters using the provided dictionary.

    Only parameters present in the dictionary are set. After setting, the function checks if all provided parameters
    were used and raises an error if any are left unused.

    Parameters
    ----------
    analysis : Analysis
        The analysis object containing settings for either beam or fiber parameters.
    which : Literal['beam', 'fiber']
        Specifies whether to set 'beam' or 'fiber' parameters. Determines which set of methods to use within the
        `analysis` object.
    parameters : dict | None
        A dictionary containing parameter names and their desired values. See also pop_create_beam_parameter_dict() and
        pop_create_fiber_parameter_dict(). Parameters not accepted by the current beam or fiber type will raise an
        error.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `which` is not 'beam' or 'fiber', or if any parameters in `parameters` do not match those expected for the
        specified `which` type in `analysis`.
    """
    if parameters is not None:
        parameters = parameters.copy()  # Create copy to preserve the original dictionary

        if which == "beam":
            number_of_parameters = analysis.Settings.NumberOfParameters
            get_parameter_name = analysis.Settings.GetParameterName
            set_parameter_value = analysis.Settings.SetParameterValue
        elif which == "fiber":
            number_of_parameters = analysis.Settings.NumberOfFiberParameters
            get_parameter_name = analysis.Settings.GetFiberParameterName
            set_parameter_value = analysis.Settings.SetFiberParameterValue
        else:
            raise ValueError("Invalid parameter type. Choose 'fiber' or 'beam'.")

        for i in range(number_of_parameters):
            param_name = get_parameter_name(i)
            param_value = parameters.pop(param_name, None)
            if param_value is not None:  # Only set parameters that are present in the dictionary
                set_parameter_value(i, param_value)

        if parameters:
            raise ValueError(
                f"The following {which} parameters are specified but not accepted: {parameters.keys()}. "
                f"The accepted {which} parameters for this {which}_type are: "
                f"{','.join([get_parameter_name(i) for i in range(number_of_parameters)])}"
            )


def physical_optics_propagation(
    oss: OpticStudioSystem,
    # General
    wavelength: Literal["All"] | int = "All",
    field: int = 1,
    start_surface: Literal["Ent. Pupil"] | int = 1,
    end_surface: Literal["Image"] | int = "Image",
    surface_to_beam: float = 0.0,
    use_polarization: bool = False,
    separate_xy: bool = False,
    use_disk_storage: bool = False,
    # Beam definition
    beam_type: constants.Analysis.PhysicalOptics.POPBeamTypes | str = "GaussianWaist",
    beam_file: str = "",
    beam_parameters: dict | None = None,
    x_sampling: constants.Analysis.SampleSizes | str | int = 32,
    y_sampling: constants.Analysis.SampleSizes | str | int = 32,
    x_width: float = 1.0,
    y_width: float = 1.0,
    use_total_power: bool = False,
    total_power: float = 1.0,
    use_peak_irradiance: bool = True,
    peak_irradiance: float = 1.0,
    # Display
    show_as: constants.Analysis.PhysicalOptics.POPShowAsTypes | str = "FalseColor",
    data_type: constants.Analysis.PhysicalOptics.POPDataTypes | str = "Irradiance",
    project: constants.Analysis.PhysicalOptics.POPProjectionTypes | str = "AlongBeam",
    contour_format: str = "",
    plot_scale: float = 0,
    scale_type: constants.Analysis.PhysicalOptics.POPScaleTypes | str = "Linear",
    zoom_in: constants.Analysis.PhysicalOptics.POPZoomTypes | str = "NoZoom",
    row_or_column: int | Literal["Center"] = "Center",
    zero_phase_level: float = 0.001,
    save_output_beam: bool = False,
    output_beam_file: str = "",
    save_beam_at_all_surfaces: bool = False,
    compute_fiber_coupling_integral: bool = False,
    ignore_fibre_polarization: bool = True,
    fiber_type: constants.Analysis.PhysicalOptics.POPFiberTypes | str = "GaussianWaist",
    fiber_position: constants.Analysis.PhysicalOptics.POPFiberPositions | str = "ChiefRay",
    tilt_about_x: float = 0.0,
    tilt_about_y: float = 0.0,
    fiber_type_file: str = "",
    fiber_parameters: dict | None = None,
    auto_calculate_beam_sampling: bool = False,
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Physical Optics Propagation analysis.

    See the OpticStudio documentation for a more in depth description of most parameters.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    wavelength : str | int
        The wavelength to use in the analysis. Either 'All' or an integer specifying the wavelength number. Defaults to
        'All'.
    field : int
        The field number of the chief ray used to align the beam for the analysis. Should be an integer specifying the
        field number. Defaults to 1.
    start_surface : str | int
        The surface that is to be analyzed. Either 'Ent. Pupil' or an integer specifying the surface number. Defaults to
         1.
    end_surface : str | int
        The surface that is to be analyzed. Either 'Image' or an integer specifying the surface number. Defaults to
        'Image'.
    surface_to_beam : float
        Distance from starting surface to starting beam position. Defaults to 0.0.
    use_polarization : bool
        Use polarization. Defaults to False.
    separate_xy : bool
        Separate propagation in X Y direction. Defaults to False.
    use_disk_storage : bool
        Use disk storage. Defaults to False.
    beam_type : constants.Analysis.PhysicalOptics.POPBeamTypes | str
        The beam type. Defaults to 'GaussianWaist'.
    beam_file:
        The beam file used for the beam definition. Should include the .ZBF extension. The beam files have to be located
        in the OpticStudio <pop> folder. Only used when beam_type is set to 'File', 'DLL' or 'Multimode'. Defaults to
        ''.
    beam_parameters : dict | None
        The beam parameters. Either a dictionary containing the beam parameters settings or None. Only the parameters
        that are defined in the dictionary will be set, the other parameters will remain their default value. Note that
        the accepted beam parameters vary per beam type. The accepted parameters for a specific beam type and their
        default values can be obtained through zospy.analysis.physicaloptics.pop_create_beam_parameter_dict(), which can
        then be adjusted and parsed to beam_parameters. When set to None, the default beam parameters will be used.
        Defaults to None.
    x_sampling : constants.Analysis.SampleSizes | str | int
        The number of points used to sample the beam in the x direction. Either specified using
        constants.Analysis.SampleSizes, a string (e.g. '32x32') or integer (e.g. 32). Note that the string or integer
        should match one of the sample sizes in constants.Analysis.SampleSizes (32 or '32x32' for 'S_32x32' etc.).
        Defaults to 32.
    y_sampling : constants.Analysis.SampleSizes | str | int
        The number of points used to sample the beam in the y direction. Either specified using
        constants.Analysis.SampleSizes, a string (e.g. '32x32') or integer (e.g. 32). Note that the string or integer
        should match one of the sample sizes in constants.Analysis.SampleSizes (32 or '32x32' for 'S_32x32' etc.).
        Defaults to 32.
    x_width : float
        The original with of the region represented by the array in OpticStudio lens units. Defaults to 1.0.
    y_width : float
        The original with of the region represented by the array in OpticStudio lens units. Defaults to 1.0.
    use_total_power : bool
        Use total power. Note that either use_total_power or use_peak_irradiance has to be True. Defaults to False.
    total_power : float
        The total power. Only used when use_total_power is True. Defaults to 1.0.
    use_peak_irradiance : bool
        Use peak irradiance. Note that either use_total_power or use_peak_irradiance has to be True. Defaults to True.
    peak_irradiance : float
        The peak irradiance. Only used when use_peak_irradiance is True. Defaults to 1.0.
    show_as : constants.Analysis.PhysicalOptics.POPShowAsTypes | str
        Defines the default graph in OpticStudio. Defaults to 'FalseColor'.
    data_type : constants.Analysis.PhysicalOptics.POPDataTypes | str
        Defines the type of output data. Defaults to 'Irradiance'.
    project : constants.Analysis.PhysicalOptics.POPProjectionTypes | str
        Defines the perspective from which the beam is viewed. Defaults to 'AlongBeam'.
    contour_format : str
        The contour format string. An empty string means no formatting. Only used when show_as is set to 'Contour'.
        Defaults to ''.
    plot_scale : float
        The plot scale. Defaults to 0.
    scale_type : constants.Analysis.PhysicalOptics.POPScaleTypes | str
        The scale type for the plot. Defaults to 'Linear'.
    zoom_in : constants.Analysis.PhysicalOptics.POPZoomTypes | str
        The zoom factor for the plot. Defaults to 'NoZoom'.
    row_or_column : int | str
        An integer defining the row or column number used when show_as is either 'CrossX' or 'CrossY'. Also accepts
        'Center'. Defaults to 'Center'.
    zero_phase_level : float
        The lower limit on the relative irradiance. Data points below this threshold have a phase value of 0. Defaults
        to 0.001.
    save_output_beam : bool
        Defines whether the output beam should be saved. Defaults to False.
    output_beam_file : str
        The filename to which the output beam should be saved. Should NOT include the .ZBF extension. The file will be
        saved in the OpticStudio <pop> folder.
    save_beam_at_all_surfaces : bool
        Defines whether the beam should be saved at all surfaces. Only used when save_output_beam is set to True.
        Defaults to False.
    compute_fiber_coupling_integral : bool
        Defines whether the fibre coupling is computed. Defaults to False.
    ignore_fibre_polarization :
        Defines whether polarization is considered. Defaults to True.
    fiber_type : constants.Analysis.PhysicalOptics.POPFiberTypes | str
        The fiber type. Defaults to 'GaussianWaist'.
    fiber_position : constants.Analysis.PhysicalOptics.POPFiberPositions | str
        The reference for the center of the receiving fiber. Defaults t 'ChiefRay'.
    tilt_about_x :
        The tilt of the fiber around the x-axis in degrees with respect to the beam. Defaults to 0.0.
    tilt_about_y :
        The tilt of the fiber around the y-axis in degrees with respect to the beam. Defaults to 0.0.
    fiber_type_file :
        The file containing the fiber description. Only used is fiber_type is set to 'File' or 'DLL'.
    fiber_parameters : dict | None
        The fiber parameters. Either a dictionary containing the fiber parameters settings or None. Only the parameters
        that are defined in the dictionary will be set, the other parameters will remain their default value. Note that
        the accepted beam parameters vary per fiber type. The accepted parameters for a specific fiber type and their
        default values can be obtained through zospy.analysis.physicaloptics.pop_create_fiber_parameter_dict(), which
        can then be adjusted and parsed to fiber_parameters. When set to None, the default fiber parameters will be
        used. Defaults to None.
    auto_calculate_beam_sampling : bool
        Defines whether the beam sampling should be automatically calculated. Will adjust x_width and y_width. This
        calculation is done just before the analysis is run. Only used when beam_type is not one of ('File', 'DLL',
        'Multimode'). Defaults to False.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A Physical Optics Propagation analysis result.
    """
    # TODO: evaluate what happens when output_beam_file includes either a filepath or the .ZBF extension.
    analysis_type = constants.Analysis.AnalysisIDM.PhysicalOpticsPropagation

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    # Adjust settings
    analysis.set_wavelength(wavelength)
    analysis.set_field(field)

    # Start surface
    if start_surface == "Ent. Pupil":
        analysis.Settings.StartSurface.SetSurfaceNumber(0)
    elif isinstance(start_surface, int):
        analysis.Settings.StartSurface.SetSurfaceNumber(start_surface)
    else:
        raise ValueError(f'start_surface value should be "Ent. Pupil" or an integer, got {start_surface}')

    # End surface
    if end_surface == "Image":
        analysis.Settings.EndSurface.UseImageSurface()
    elif isinstance(end_surface, int):
        analysis.Settings.EndSurface.SetSurfaceNumber(end_surface)
    else:
        raise ValueError(f'end_surface value should be "Image" or an integer, got {end_surface}')

    analysis.Settings.SurfaceToBeam = surface_to_beam
    analysis.Settings.UsePolarization = use_polarization
    analysis.Settings.SeparateXY = separate_xy
    analysis.Settings.UseDiskStorage = use_disk_storage

    # Beam settings
    analysis.Settings.BeamType = constants.process_constant(constants.Analysis.PhysicalOptics.POPBeamTypes, beam_type)
    if isinstance(x_sampling, int):
        x_sampling = f"{x_sampling}x{x_sampling}"
    analysis.Settings.XSampling = constants.process_constant(
        constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(x_sampling)
    )
    if isinstance(y_sampling, int):
        y_sampling = f"{y_sampling}x{y_sampling}"
    analysis.Settings.YSampling = constants.process_constant(
        constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(y_sampling)
    )

    analysis.Settings.XWidth = x_width
    analysis.Settings.YWidth = y_width

    if not (use_total_power ^ use_peak_irradiance):
        raise ValueError(
            "Either use_total_power or use_peak_irradiance should be True, they cannot both be True or False."
        )
    if use_total_power:
        analysis.Settings.UseTotalPower = use_total_power
        analysis.Settings.TotalPower = total_power
    else:
        analysis.Settings.UsePeakIrradiance = use_peak_irradiance
        analysis.Settings.PeakIrradiance = peak_irradiance

    if beam_file != "":
        if str(analysis.Settings.BeamType) in ("File", "DLL", "Multimode"):
            analysis.Settings.BeamTypeFilename = beam_file
        else:
            raise ValueError(f"Beam type {beam_type!s} does not allow specification of beam_file.")

    _set_pop_parameters(analysis, which="beam", parameters=beam_parameters)

    # Display settings
    analysis.Settings.ShowAs = constants.process_constant(constants.Analysis.PhysicalOptics.POPShowAsTypes, show_as)
    analysis.Settings.DataType = constants.process_constant(constants.Analysis.PhysicalOptics.POPDataTypes, data_type)
    analysis.Settings.Project = constants.process_constant(
        constants.Analysis.PhysicalOptics.POPProjectionTypes, project
    )

    if str(analysis.Settings.ShowAs) == "Contour":
        analysis.Settings.ContourFormat = contour_format
    elif str(analysis.Settings.ShowAs) in ("CrossX", "CrossY"):
        analysis.Settings.RowOrColumn = 0 if row_or_column == "Center" else row_or_column

    analysis.Settings.PlotScale = plot_scale
    analysis.Settings.ScaleType = constants.process_constant(
        constants.Analysis.PhysicalOptics.POPScaleTypes, scale_type
    )
    analysis.Settings.ZoomIn = constants.process_constant(constants.Analysis.PhysicalOptics.POPZoomTypes, zoom_in)
    analysis.Settings.ZeroPhaseLevel = zero_phase_level

    analysis.Settings.SaveOutputBeam = save_output_beam
    if analysis.Settings.SaveOutputBeam:
        if output_beam_file == "":
            raise ValueError("output_beam_file should be a valid filepath if save_output_beam is True.")
        analysis.Settings.OutputBeamFile = output_beam_file
    else:
        if output_beam_file != "":
            raise warnings.warn("save_output_beam is False but output_beam_file is specified.")

        analysis.Settings.SaveBeamAtAllSurfaces = save_beam_at_all_surfaces

    analysis.Settings.ComputeFiberCouplingIntegral = compute_fiber_coupling_integral

    # Fiber settings
    if analysis.Settings.ComputeFiberCouplingIntegral:
        analysis.Settings.IgnoreFiberPolarization = ignore_fibre_polarization
        analysis.Settings.FiberType = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPFiberTypes, fiber_type
        )
        analysis.Settings.FiberPosition = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPFiberPositions, fiber_position
        )
        analysis.Settings.TiltAboutX = tilt_about_x
        analysis.Settings.TiltAboutY = tilt_about_y

        if fiber_type_file != "":
            if str(analysis.Settings.FiberType) in ("File", "DLL"):
                analysis.Settings.FiberTypeFilename = fiber_type_file
            else:
                raise ValueError(
                    f"Beam type {analysis.Settings.FiberTypeFilename!s} does not allow specification of fiber_type_file."
                )

        _set_pop_parameters(analysis, which="fiber", parameters=fiber_parameters)

    # Auto calculate beam sampling
    if auto_calculate_beam_sampling and str(analysis.Settings.BeamType) not in ("File", "DLL", "Multimode"):
        analysis.Settings.AutoCalculateBeamSampling()

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["Field"] = analysis.get_field()
    if analysis.Settings.StartSurface.GetSurfaceNumber() == 0:
        settings.loc["StartSurface"] = "Ent. Pupil"
    else:
        settings.loc["StartSurface"] = analysis.Settings.StartSurface.GetSurfaceNumber()

    if analysis.Settings.EndSurface.GetSurfaceNumber() == 0:
        settings.loc["EndSurface"] = "Image"
    else:
        settings.loc["EndSurface"] = analysis.Settings.EndSurface.GetSurfaceNumber()

    settings.loc["SurfaceToBeam"] = analysis.Settings.SurfaceToBeam
    settings.loc["UsePolarization"] = analysis.Settings.UsePolarization
    settings.loc["SeparateXY"] = analysis.Settings.SeparateXY
    settings.loc["UseDiskStorage"] = analysis.Settings.UseDiskStorage
    settings.loc["BeamType"] = str(analysis.Settings.BeamType)
    settings.loc["XSampling"] = str(analysis.Settings.XSampling)
    settings.loc["YSampling"] = str(analysis.Settings.YSampling)
    settings.loc["XWidth"] = analysis.Settings.XWidth
    settings.loc["YWidth"] = analysis.Settings.YWidth
    settings.loc["UseTotalPower"] = analysis.Settings.UseTotalPower
    if analysis.Settings.UseTotalPower:
        settings.loc["TotalPower"] = analysis.Settings.TotalPower

    settings.loc["UsePeakIrradiance"] = analysis.Settings.UsePeakIrradiance
    if analysis.Settings.UsePeakIrradiance:
        settings.loc["PeakIrradiance"] = analysis.Settings.PeakIrradiance

    if str(analysis.Settings.BeamType) in ("File", "DLL", "Multimode"):
        settings.loc["BeamTypeFilename"] = analysis.Settings.BeamTypeFilename

    for i in range(analysis.Settings.NumberOfParameters):
        key = "Beam" + "".join(analysis.Settings.GetParameterName(i).split(" "))
        settings.loc[key] = analysis.Settings.GetParameterValue(i)

    settings.loc["ShowAs"] = str(analysis.Settings.ShowAs)
    settings.loc["DataType"] = str(analysis.Settings.DataType)
    settings.loc["Project"] = str(analysis.Settings.Project)

    if str(analysis.Settings.ShowAs) == "Contour":
        settings.loc["ContourFormat"] = analysis.Settings.ContourFormat
    elif str(analysis.Settings.ShowAs) in ("CrossX", "CrossY"):
        if analysis.Settings.RowOrColumn == 0:
            settings.loc["RowOrColumn"] = "Center"
        else:
            settings.loc["RowOrColumn"] = analysis.Settings.RowOrColumn

    settings.loc["PlotScale"] = analysis.Settings.PlotScale
    settings.loc["ScaleType"] = str(analysis.Settings.LogScale)
    settings.loc["ZoomIn"] = str(analysis.Settings.ZoomIn)
    settings.loc["ZeroPhaseLevel"] = analysis.Settings.ZeroPhaseLevel

    settings.loc["SaveOutputBeam"] = analysis.Settings.SaveOutputBeam
    if analysis.Settings.SaveOutputBeam:
        settings.loc["OutputBeamFile"] = analysis.Settings.OutputBeamFile
        settings.loc["SaveBeamAtAllSurfaces"] = analysis.Settings.SaveBeamAtAllSurfaces

    settings.loc["ComputeFiberCouplingIntegral"] = analysis.Settings.ComputeFiberCouplingIntegral

    if analysis.Settings.ComputeFiberCouplingIntegral:
        settings.loc["ComputeFiberCouplingIntegral"] = analysis.Settings.ComputeFiberCouplingIntegral
        settings.loc["IgnoreFiberPolarization"] = analysis.Settings.IgnoreFiberPolarization
        settings.loc["FiberType"] = str(analysis.Settings.FiberType)
        settings.loc["FiberPosition"] = str(analysis.Settings.FiberPosition)
        settings.loc["TiltAboutX"] = analysis.Settings.TiltAboutX
        settings.loc["TiltAboutY"] = analysis.Settings.TiltAboutY

        if str(analysis.Settings.FiberType) in ("File", "DLL"):
            settings.loc["FiberTypeFilename"] = analysis.Settings.FiberTypeFilename

        for i in range(analysis.Settings.NumberOfFiberParameters):
            key = "Fiber" + "".join(analysis.Settings.GetFiberParameterName(i).split(" "))
            settings.loc[key] = analysis.Settings.GetFiberParameterValue(i)

    if str(analysis.Settings.BeamType) not in ("File", "DLL", "Multimode"):
        settings.loc["AutoCalculateBeamSampling"] = auto_calculate_beam_sampling

    # Get data and unpack
    data = []
    for i in range(analysis.Results.NumberOfDataGrids):
        data.append(utils.zputils.unpack_datagrid(analysis.Results.DataGrids[i],
                                                  # pass "center" and None for consistency with older ZOSPy versions
                                                  cell_origin="center", label_rounding=None))

    if len(data) == 0:
        data = pd.DataFrame()
    elif len(data) == 1:
        data = data[0]
    else:
        data = pd.concat(data, axis=1)

    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)
