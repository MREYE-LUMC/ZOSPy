"""System Data analysis."""

from pydantic import Field

from zospy.analyses.base import BaseAnalysisWrapper
from zospy.analyses.decorators import analysis_result
from zospy.analyses.parsers import ZospyTransformer

__all__ = ("SystemData",)

from zospy.analyses.parsers.transformers import SimpleField


class SystemDataTransformer(ZospyTransformer):
    def general_lens_data(self, args):
        return SimpleField("General Lens Data", self.dict(args[1:]))

    def system_aperture(self, args):
        name, aperture_type, value = args

        return SimpleField(str(name), {"type": aperture_type, "value": value})

    def apodization(self, args):
        name, apodization_type, factor = args

        return SimpleField(str(name), {"type": apodization_type, "factor": factor})

    def efl_air(self, args):
        name, value = args

        return SimpleField("Effective Focal Length (air)", value)

    def efl_image(self, args):
        name, value = args

        return SimpleField("Effective Focal Length (image)", value)

    def field_data(self, args):
        return SimpleField("Fields", self.dict(args))

    def fields_table(self, args):
        header, rows = args[0]

        return SimpleField("Table", [dict(zip(header, row)) for row in rows])

    def vignetting_table(self, args):
        header, rows = args[0]

        return SimpleField("Vignetting Factors", [dict(zip(header, row)) for row in rows])

    def wavelength_data(self, args):
        return SimpleField("Wavelengths", self.dict(args))

    def wavelength_table(self, args):
        header, rows = args[0]

        return SimpleField("Table", [dict(zip(header, row)) for row in rows])

    def abcd_matrix(self, args):
        return SimpleField("Predicted coordinate ABCD matrix", self.dict(args))


@analysis_result
class SystemAperture:
    type: str
    value: float


@analysis_result
class Apodization:
    type: str
    factor: float


@analysis_result
class GeneralLensData:
    surfaces: int = Field(alias="Surfaces")
    stop: int = Field(alias="Stop")
    system_aperture: SystemAperture = Field(alias="System Aperture")
    fast_semi_diameters: bool = Field(alias="Fast Semi-Diameters")
    field_unpolarized: bool = Field(alias="Field Unpolarized")
    convert_thin_film_phase_to_ray_equivalent: bool = Field(alias="Convert thin film phase to ray equivalent")
    j_e_conversion_method: str = Field(alias="J/E Conversion Method")
    glass_catalogs: list[str] = Field(alias="Glass Catalogs")
    ray_aiming: bool = Field(alias="Ray Aiming")
    apodization: Apodization = Field(alias="Apodization")
    reference_opd: str = Field(alias="Reference OPD")
    paraxial_rays_setting: str = Field(alias="Paraxial Rays Setting")
    method_to_compute_f_number: str = Field(alias="Method to Compute F/#")
    method_to_compute_huygens_integral: str = Field(alias="Method to Compute Huygens Integral")
    print_coordinate_breaks: bool = Field(alias="Print Coordinate Breaks")
    multi_threading: bool = Field(alias="Multi-Threading")
    opd_modulo_2_pi: bool = Field(alias="OPD Modulo 2 Pi")
    temperature: float = Field(alias="Temperature (C)")
    pressure: float = Field(alias="Pressure (ATM)")
    adjust_index_data_to_environment: bool = Field(alias="Adjust Index Data To Environment")
    effective_focal_length_air: float = Field(alias="Effective Focal Length (air)")
    effective_focal_length_image: float = Field(alias="Effective Focal Length (image)")
    back_focal_length: float = Field(alias="Back Focal Length")
    total_track: float = Field(alias="Total Track")
    image_space_f_number: float = Field(alias="Image Space F/#")
    paraxial_working_f_number: float = Field(alias="Paraxial Working F/#")
    working_f_number: float = Field(alias="Working F/#")
    image_space_na: float = Field(alias="Image Space NA")
    object_space_na: float = Field(alias="Object Space NA")
    stop_radius: float = Field(alias="Stop Radius")
    paraxial_image_height: float = Field(alias="Paraxial Image Height")
    paraxial_magnification: float = Field(alias="Paraxial Magnification")
    entrance_pupil_diameter: float = Field(alias="Entrance Pupil Diameter")
    entrance_pupil_position: float = Field(alias="Entrance Pupil Position")
    exit_pupil_diameter: float = Field(alias="Exit Pupil Diameter")
    exit_pupil_position: float = Field(alias="Exit Pupil Position")
    field_type: str = Field(alias="Field Type")
    maximum_radial_field: float = Field(alias="Maximum Radial Field")
    primary_wavelength: float = Field(alias="Primary Wavelength")
    angular_magnification: float = Field(alias="Angular Magnification")
    lens_units: str = Field(alias="Lens Units")
    source_units: str = Field(alias="Source Units")
    analysis_units: str = Field(alias="Analysis Units")
    afocal_mode_units: str = Field(alias="Afocal Mode Units")
    mtf_units: str = Field(alias="MTF Units")
    include_calculated_data_in_session_file: bool = Field(alias="Include Calculated Data in Session File")


@analysis_result
class FieldData:
    number: int = Field(alias="#")
    x_value: float = Field(alias="X-Value")
    y_value: float = Field(alias="Y-Value")
    weight: float = Field(alias="Weight")


@analysis_result
class Fields:
    number_of_fields: int = Field(alias="Fields")
    field_type: str = Field(alias="Field Type")
    fields: list[FieldData] = Field(alias="Table")


@analysis_result
class VignettingData:
    number: int = Field(alias="#")
    vdx: float = Field(alias="VDX")
    vdy: float = Field(alias="VDY")
    vcx: float = Field(alias="VCX")
    vcy: float = Field(alias="VCY")
    van: float = Field(alias="VAN")


@analysis_result
class WavelengthData:
    number: int = Field(alias="#")
    value: float = Field(alias="Value")
    weight: float = Field(alias="Weight")


@analysis_result
class Wavelengths:
    number_of_wavelengths: int = Field(alias="Wavelengths")
    units: str = Field(alias="Units")
    wavelengths: list[WavelengthData] = Field(alias="Table")


@analysis_result
class ABCDMatrix:
    A: float
    B: float
    C: float
    D: float


@analysis_result
class SystemDataResult:
    """Data for the System Data analysis."""

    general_lens_data: GeneralLensData = Field(alias="General Lens Data")
    fields: Fields = Field(alias="Fields")
    vignetting: list[VignettingData] = Field(alias="Vignetting Factors")
    wavelengths: Wavelengths = Field(alias="Wavelengths")
    abcd_matrix: ABCDMatrix = Field(alias="Predicted coordinate ABCD matrix")


class SystemData(BaseAnalysisWrapper[SystemDataResult, None], analysis_type="SystemData", needs_text_output_file=True):
    """System Data analysis."""

    def __init__(self):
        """Create a new System Data analysis.

        This analysis does not require any settings.
        """
        super().__init__()

    def run_analysis(self) -> SystemDataResult:
        """Run the System Data analysis."""
        self.analysis.ApplyAndWaitForCompletion()

        return self.parse_output("system_data", transformer=SystemDataTransformer, result_type=SystemDataResult)
