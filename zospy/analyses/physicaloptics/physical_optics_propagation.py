"""Physical Optics Propagation analysis."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal, Union
from warnings import warn

from pandas import DataFrame
from pydantic import Field, model_validator

from zospy.analyses.base import BaseAnalysisWrapper, new_analysis
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import WavelengthNumber, ZOSAPIConstant  # noqa: TCH001
from zospy.api import constants
from zospy.utils.zputils import standardize_sampling

if TYPE_CHECKING:
    from zospy.zpcore import OpticStudioSystem

__all__ = (
    "PhysicalOpticsPropagation",
    "PhysicalOpticsPropagationSettings",
    "create_beam_parameter_dict",
    "create_fiber_parameter_dict",
)


@analysis_settings
class PhysicalOpticsPropagationSettings:
    """Settings for Physical Optics Propagation analysis.

    See the OpticStudio documentation for a more in depth description of most parameters.

    Attributes
    ----------
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
        The original width of the region represented by the array in OpticStudio lens units. Defaults to 1.0.
    y_width : float
        The original width of the region represented by the array in OpticStudio lens units. Defaults to 1.0.
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
    ignore_fiber_polarization :
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
    """

    wavelength: WavelengthNumber = Field(default="All", description="Wavelength number")
    field: int = Field(default=1, ge=1, description="Field number")
    start_surface: Literal["Ent. Pupil"] | Annotated[int, Field(ge=1)] = Field(default=1, description="Start surface")
    end_surface: Literal["Image"] | Annotated[int, Field(ge=1)] = Field(default="Image", description="End surface")
    surface_to_beam: float = Field(default=0, description="Surface to beam")
    use_polarization: bool = Field(default=False, description="Use polarization")
    separate_xy: bool = Field(default=False, description="Separate propagation in X Y direction")
    use_disk_storage: bool = Field(default=False, description="Use disk storage")

    # Beam definition
    beam_type: ZOSAPIConstant("Analysis.PhysicalOptics.POPBeamTypes") = Field(
        default="GaussianWaist", description="Beam type"
    )
    beam_file: str = Field(default="", description="Beam file")
    beam_parameters: dict | None = Field(default=None, description="Beam parameters dictionary")
    x_sampling: str | Annotated[int, Field(ge=1)] = Field(default=32, description="Beam sampling in X direction")
    y_sampling: str | Annotated[int, Field(ge=1)] = Field(default=32, description="Beam sampling in Y direction")
    x_width: float = Field(default=1, description="Beam width in X direction")
    y_width: float = Field(default=1, description="Beam width in Y direction")
    use_total_power: bool = Field(default=False, description="Use total power")
    total_power: float = Field(default=1, description="Total power")
    use_peak_irradiance: bool = Field(default=True, description="Use peak irradiance")
    peak_irradiance: float = Field(default=1, description="Peak irradiance")

    # Display
    show_as: ZOSAPIConstant("Analysis.PhysicalOptics.POPShowAsTypes") = Field(
        default="FalseColor", description="Show as"
    )
    data_type: ZOSAPIConstant("Analysis.PhysicalOptics.POPDataTypes") = Field(
        default="Irradiance", description="Data type"
    )
    project: ZOSAPIConstant("Analysis.PhysicalOptics.POPProjectionTypes") = Field(
        default="AlongBeam", description="Projection types"
    )
    contour_format: str = Field(default="", description="Contour format")
    plot_scale: float = Field(default=0, description="Plot scale")
    scale_type: ZOSAPIConstant("Analysis.PhysicalOptics.POPScaleTypes") = Field(
        default="Linear", description="Scale type"
    )
    zoom_in: ZOSAPIConstant("Analysis.PhysicalOptics.POPZoomTypes") = Field(default="NoZoom", description="Zoom in")
    row_or_column: int | Literal["Center"] = Field(default="Center", description="Row or column")
    zero_phase_level: float = Field(default=0.001, description="Zero phase level")
    save_output_beam: bool = Field(default=False, description="Save output beam")
    output_beam_file: str = Field(default="", description="Output beam file")
    save_beam_at_all_surfaces: bool = Field(default=False, description="Save beam at all surfaces")

    # Fiber definition
    compute_fiber_coupling_integral: bool = Field(default=False, description="Compute fiber coupling integral")
    ignore_fiber_polarization: bool = Field(default=True, description="Ignore fibre polarization")
    fiber_type: ZOSAPIConstant("Analysis.PhysicalOptics.POPFiberTypes") = Field(
        default="GaussianWaist", description="Fiber type"
    )
    fiber_position: ZOSAPIConstant("Analysis.PhysicalOptics.POPFiberPositions") = Field(
        default="ChiefRay", description="Fiber position"
    )
    tilt_about_x: float = Field(default=0, description="Tilt about X")
    tilt_about_y: float = Field(default=0, description="Tilt about Y")
    fiber_type_file: str = Field(default="", description="Fiber type file")
    fiber_parameters: dict | None = Field(default=None, description="Fiber parameters dictionary")

    auto_calculate_beam_sampling: bool = Field(default=False, description="Automatically calculate beam sampling")

    @model_validator(mode="after")
    def _validate_total_power_peak_irradiance(self):
        if not (self.use_total_power ^ self.use_peak_irradiance):
            raise ValueError(
                "Either use_total_power or use_peak_irradiance should be True, they cannot both be True or False."
            )

        return self

    @model_validator(mode="after")
    def _validate_beam_file(self):
        if str(self.beam_type) not in ("File", "DLL", "Multimode") and self.beam_file != "":
            raise ValueError(f"Beam type {self.beam_type!s} does not allow specification of beam_file.")

        return self

    @model_validator(mode="after")
    def _validate_output_beam_file(self):
        if self.save_output_beam and self.output_beam_file == "":
            raise ValueError("output_beam_file should be specified when save_output_beam is True.")
        if not self.save_output_beam:
            if self.output_beam_file != "":
                warn("output_beam_file is ignored when save_output_beam is False.")
            if self.save_beam_at_all_surfaces:
                warn("save_beam_at_all_surfaces is ignored when save_output_beam is False.")

        return self

    @model_validator(mode="after")
    def _validate_fiber_type_file(self):
        if str(self.fiber_type) not in ("File", "DLL") and self.fiber_type_file != "":
            raise ValueError(f"Fiber type {self.fiber_type!s} does not allow specification of fiber_type_file.")

        return self


class PhysicalOpticsPropagation(
    BaseAnalysisWrapper[Union[DataFrame, None], PhysicalOpticsPropagationSettings],
    analysis_type="PhysicalOpticsPropagation",
    mode="Sequential",
):
    """Physical Optics Propagation analysis."""

    def __init__(
        self,
        *,
        wavelength: WavelengthNumber = "All",
        field: int = 1,
        start_surface: Literal["Ent. Pupil"] | int = 1,
        end_surface: Literal["Image"] | int = "Image",
        surface_to_beam: float = 0,
        use_polarization: bool = False,
        separate_xy: bool = False,
        use_disk_storage: bool = False,
        beam_type: constants.Analysis.PhysicalOptics.POPBeamTypes | str = "GaussianWaist",
        beam_file: str = "",
        beam_parameters: dict | None = None,
        x_sampling: constants.Analysis.SampleSizes | str | int = 32,
        y_sampling: constants.Analysis.SampleSizes | str | int = 32,
        x_width: float = 1,
        y_width: float = 1,
        use_total_power: bool = False,
        total_power: float = 1,
        use_peak_irradiance: bool = True,
        peak_irradiance: float = 1,
        show_as: constants.Analysis.PhysicalOptics.POPShowAsTypes | str = "FalseColor",
        data_type: constants.Analysis.PhysicalOptics.POPDataTypes | str = "Irradiance",
        project: constants.Analysis.PhysicalOptics.POPProjectionTypes | str = "AlongBeam",
        contour_format: str = "",
        plot_scale: float = 0,
        scale_type: constants.Analysis.PhysicalOptics.POPScaleTypes | str = "Linear",
        zoom_in: constants.Analysis.PhysicalOptics.POPZoomTypes | str = "NoZoom",
        row_or_column: int | str = "Center",
        zero_phase_level: float = 0.001,
        save_output_beam: bool = False,
        output_beam_file: str = "",
        save_beam_at_all_surfaces: bool = False,
        compute_fiber_coupling_integral: bool = False,
        ignore_fiber_polarization: bool = True,
        fiber_type: constants.Analysis.PhysicalOptics.POPFiberTypes | str = "GaussianWaist",
        fiber_position: constants.Analysis.PhysicalOptics.POPFiberPositions | str = "ChiefRay",
        tilt_about_x: float = 0,
        tilt_about_y: float = 0,
        fiber_type_file: str = "",
        fiber_parameters: dict | None = None,
        auto_calculate_beam_sampling: bool = False,
        settings: PhysicalOpticsPropagationSettings | None = None,
    ):
        """Create a Physical Optics Propagation analysis.

        See Also
        --------
        PhysicalOpticsPropagationSettings : Settings for the Physical Optics Propagation analysis.
        """
        super().__init__(settings_kws=locals())

    def run_analysis(self) -> DataFrame:
        """Run the Physical Optics Propagation analysis."""
        if self.settings.start_surface == "Ent. Pupil":
            self.analysis.Settings.StartSurface.SetSurfaceNumber(0)
        elif isinstance(self.settings.start_surface, int):
            self.analysis.Settings.StartSurface.SetSurfaceNumber(self.settings.start_surface)
        else:
            raise ValueError(
                f'start_surface value should be "Ent. Pupil" or an integer, got {self.settings.start_surface}'
            )

        if self.settings.end_surface == "Image":
            self.analysis.Settings.EndSurface.UseImageSurface()
        elif isinstance(self.settings.end_surface, int):
            self.analysis.Settings.EndSurface.SetSurfaceNumber(self.settings.end_surface)
        else:
            raise ValueError(f'end_surface value should be "Image" or an integer, got {self.settings.end_surface}')

        self.analysis.set_wavelength(self.settings.wavelength)
        self.analysis.set_field(self.settings.field)
        self.analysis.Settings.SurfaceToBeam = self.settings.surface_to_beam
        self.analysis.Settings.UsePolarization = self.settings.use_polarization
        self.analysis.Settings.SeparateXY = self.settings.separate_xy
        self.analysis.Settings.UseDiskStorage = self.settings.use_disk_storage

        # Beam settings
        self.analysis.Settings.BeamType = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPBeamTypes, self.settings.beam_type
        )

        x_sampling = (
            f"{self.settings.x_sampling}x{self.settings.y_sampling}"
            if isinstance(self.settings.x_sampling, int)
            else self.settings.x_sampling
        )
        y_sampling = (
            f"{self.settings.x_sampling}x{self.settings.y_sampling}"
            if isinstance(self.settings.y_sampling, int)
            else self.settings.y_sampling
        )

        self.analysis.Settings.XSampling = constants.process_constant(
            constants.Analysis.SampleSizes, standardize_sampling(x_sampling)
        )
        self.analysis.Settings.YSampling = constants.process_constant(
            constants.Analysis.SampleSizes, standardize_sampling(y_sampling)
        )
        self.analysis.Settings.XWidth = self.settings.x_width
        self.analysis.Settings.YWidth = self.settings.y_width

        if self.settings.use_total_power:
            self.analysis.Settings.UseTotalPower = True
            self.analysis.Settings.TotalPower = self.settings.total_power
        else:
            self.analysis.Settings.UsePeakIrradiance = True
            self.analysis.Settings.PeakIrradiance = self.settings.peak_irradiance

        if self.settings.beam_file != "":
            self.analysis.Settings.BeamTypeFilename = self.settings.beam_file

        self._set_pop_parameters("beam", self.settings.beam_parameters)

        # Display settings
        self.analysis.Settings.ShowAs = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPShowAsTypes, self.settings.show_as
        )
        self.analysis.Settings.DataType = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPDataTypes, self.settings.data_type
        )
        self.analysis.Settings.Project = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPProjectionTypes, self.settings.project
        )

        if self.settings.show_as == "Contour":
            self.analysis.Settings.ContourFormat = self.settings.contour_format
        elif self.settings.show_as in ("CrossX", "CrossY"):
            self.analysis.Settings.RowOrColumn = (
                0 if self.settings.row_or_column == "Center" else self.settings.row_or_column
            )

        self.analysis.Settings.PlotScale = self.settings.plot_scale
        self.analysis.Settings.LogScale = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPScaleTypes, self.settings.scale_type
        )
        self.analysis.Settings.ZoomIn = constants.process_constant(
            constants.Analysis.PhysicalOptics.POPZoomTypes, self.settings.zoom_in
        )
        self.analysis.Settings.ZeroPhaseLevel = self.settings.zero_phase_level

        self.analysis.Settings.SaveOutputBeam = self.settings.save_output_beam
        if self.settings.save_output_beam:
            self.analysis.Settings.OutputBeamFile = self.settings.output_beam_file
            self.analysis.Settings.SaveBeamAtAllSurfaces = self.settings.save_beam_at_all_surfaces

        # Fiber settings
        self.analysis.Settings.ComputeFiberCouplingIntegral = self.settings.compute_fiber_coupling_integral

        if self.settings.compute_fiber_coupling_integral:
            self.analysis.Settings.IgnoreFiberPolarization = self.settings.ignore_fiber_polarization
            self.analysis.Settings.FiberType = constants.process_constant(
                constants.Analysis.PhysicalOptics.POPFiberTypes, self.settings.fiber_type
            )
            self.analysis.Settings.FiberPosition = constants.process_constant(
                constants.Analysis.PhysicalOptics.POPFiberPositions, self.settings.fiber_position
            )
            self.analysis.Settings.TiltAboutX = self.settings.tilt_about_x
            self.analysis.Settings.TiltAboutY = self.settings.tilt_about_y

            if self.settings.fiber_type_file != "":
                self.analysis.Settings.FiberTypeFilename = self.settings.fiber_type_file

            self._set_pop_parameters("fiber", self.settings.fiber_parameters)

        # Auto calculate beam sampling
        if self.settings.auto_calculate_beam_sampling and str(self.settings.beam_type) not in (
            "File",
            "DLL",
            "Multimode",
        ):
            self.analysis.Settings.AutoCalculateBeamSampling()

        # Run analysis
        self.analysis.ApplyAndWaitForCompletion()

        return self.get_data_grid(cell_origin="bottom_left")

    def _set_pop_parameters(self, which: Literal["beam", "fiber"], parameters: dict) -> None:
        """Set beam or fiber parameters using the provided dictionary.

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
                number_of_parameters = self.analysis.Settings.NumberOfParameters
                get_parameter_name = self.analysis.Settings.GetParameterName
                set_parameter_value = self.analysis.Settings.SetParameterValue
            elif which == "fiber":
                number_of_parameters = self.analysis.Settings.NumberOfFiberParameters
                get_parameter_name = self.analysis.Settings.GetFiberParameterName
                set_parameter_value = self.analysis.Settings.SetFiberParameterValue
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


def create_beam_parameter_dict(
    oss: OpticStudioSystem, beam_type: constants.Analysis.PhysicalOptics.POPBeamTypes | str = "GaussianWaist"
) -> dict:
    """Create a dictionary containing the parameters for a certain Physical Optics beam type and their default values.

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


def create_fiber_parameter_dict(
    oss: OpticStudioSystem, fiber_type: constants.Analysis.PhysicalOptics.POPFiberTypes | str = "GaussianWaist"
) -> dict:
    """Create a dictionary containing the parameters for a certain Physical Optics fiber type and their default values.

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
