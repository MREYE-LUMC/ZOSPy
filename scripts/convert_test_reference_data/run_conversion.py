# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonata-python",
#   "pydantic",
#   "zospy @ file://${PROJECT_ROOT}",
# ]
# ///

import json
from math import isnan
from pathlib import Path

from converter import AnalysisDataConverter
from pydantic_core import ValidationError

from zospy import ZOS
from zospy.analyses.base import AnalysisResult

INPUT_FOLDER = Path("tests/data/reference/old")
OUTPUT_FOLDER = Path("tests/data/reference")


def _list_replace_values(data: list, old_values, new_values):
    for old_value, new_value in zip(old_values, new_values):
        if old_value in data:
            data[data.index(old_value)] = new_value


def postprocess_fft_through_focus_mtf(data: dict):
    # Old analyses store enum indices with an offset of 5
    index_to_string = {
        "5": "Modulation",
        "6": "Real",
        "7": "Imaginary",
        "8": "Phase",
        "9": "SquareWave",
    }

    data["settings"]["mtf_type"] = index_to_string[data["settings"]["mtf_type"]]


def postprocess_polarization_pupil_map(data: dict):
    _list_replace_values(data["data"]["pupil_map"]["columns"], ["Phase(Deg)"], ["Phase (Deg)"])


def postprocess_polarization_transmission(data: dict):
    # Remove fields that are not present in the unpolarized case
    if data["settings"]["unpolarized"]:
        data["data"].pop("x_field")
        data["data"].pop("y_field")
        data["data"].pop("x_phase")
        data["data"].pop("y_phase")


def postprocess_single_ray_trace(data: dict):
    for ray_trace_type in ("real_ray_trace_data", "paraxial_ray_trace_data"):
        ray_trace_data = data["data"][ray_trace_type]

        # Rename columns
        _list_replace_values(ray_trace_data["columns"], ("Anglein", "Pathlength"), ("Angle in", "Path length"))

        # Remove last column, which is empty
        ray_trace_data["columns"].pop()
        for row in ray_trace_data["data"]:
            row.pop()
            _list_replace_values(row, ("lensfront", "lensback"), ("lens front", "lens back"))

    # Move the comment for paraxial ray trace data to the last column
    max_row_length = max(len(row) for row in data["data"]["paraxial_ray_trace_data"]["data"])

    # Convert the X-normal column to floats
    if len(data["data"]["real_ray_trace_data"]["columns"]) > 8:
        for row in data["data"]["real_ray_trace_data"]["data"]:
            row[7] = float(row[7].replace(",", ".")) if set(row[7]) != {"-"} else float("nan")

    for row in data["data"]["paraxial_ray_trace_data"]["data"]:
        row.extend([float("nan")] * (max_row_length - len(row)))

        # Get the index of the value before a tail of NaNs
        *_, (last_value_index, last_value) = (
            (i, value) for i, value in enumerate(row) if not (isinstance(value, float) and isnan(value))
        )

        if isinstance(last_value, str) and last_value_index < len(row) - 1:
            row.append(row.pop(last_value_index))


CONVERTERS: list[AnalysisDataConverter] = [
    AnalysisDataConverter(
        old_analysis="geometric_image_analysis",
        new_analysis="GeometricImageAnalysis",
        settings_class="GeometricImageSettings",
        module="zospy.analyses.extendedscene.geometric_image_analysis",
        data_type="dataframe",
    ),
    AnalysisDataConverter(
        old_analysis="fft_through_focus_mtf",
        new_analysis="FFTThroughFocusMTF",
        settings_class="FFTThroughFocusMTFSettings",
        module="zospy.analyses.mtf.fft_through_focus_mtf",
        data_type="dataframe",
        settings_replace_keys={"sample_size": "sampling", "type": "mtf_type"},
        settings_convert_constants={"mtf_type": "Analysis.Settings.Mtf.MtfTypes"},
        postprocess=postprocess_fft_through_focus_mtf,
    ),
    AnalysisDataConverter(
        old_analysis="huygens_mtf",
        new_analysis="HuygensMTF",
        settings_class="HuygensMTFSettings",
        module="zospy.analyses.mtf.huygens_mtf",
        data_type="dataframe",
        settings_replace_keys={"type": "mtf_type"},
    ),
    AnalysisDataConverter(
        old_analysis="physical_optics_propagation",
        new_analysis="PhysicalOpticsPropagation",
        settings_class="PhysicalOpticsPropagationSettings",
        module="zospy.analyses.physicaloptics.physical_optics_propagation",
        data_type="dataframe",
    ),
    AnalysisDataConverter(
        old_analysis="polarization_pupil_map",
        new_analysis="PolarizationPupilMap",
        settings_class="PolarizationPupilMapSettings",
        module="zospy.analyses.polarization.pupil_map",
        data_type="dataclass",
        data_class="PolarizationPupilMapResult",
        data_conversion=r"""
$.data.Data.data{
    "wavelength": Wavelength,
    "field_pos": { "value": FieldPos, "unit": "deg" },
    "x_field": XField,
    "y_field": YField,
    "x_phase": XPhase,
    "y_phase": YPhase,
    "configs": Configs,
    "surface": Surface,
    "transmission": { "value": Transmission, "unit": "%" },
    "pupil_map": Table.data
}""",
        postprocess=postprocess_polarization_pupil_map,
    ),
    AnalysisDataConverter(
        old_analysis="transmission",
        new_analysis="PolarizationTransmission",
        settings_class="PolarizationTransmissionSettings",
        module="zospy.analyses.polarization.transmission",
        data_type="dataclass",
        data_class="PolarizationTransmissionResult",
        data_conversion=r"""
[
    $.data.Settings.data {
        "x_field": Jx,
        "y_field": Jy,
        "x_phase": `X-Phase`,
        "y_phase": `Y-Phase`,
        "grid_size": $replace(Sampling, "x", " x ")
    },
    $.data.Data.data{
        "field_transmissions": [
            {
                "field_pos": {
                    "value": FieldPos,
                    "unit": "deg"
                },
                "total_transmission": TotalTransmission,
                "transmissions": { $string(Wavelength): TotalTransmission }
            }
        ],
        "chief_ray_transmissions": [{
            "field_pos": {
                "value": FieldPos,
                "unit": "deg"
            },
            "wavelength": {
                "1": {
                    "value": Wavelength,
                    "unit": "µm"
                }
            },
            "transmissions": Table.data
        }]
    }
] ~> $merge
""",
        postprocess=postprocess_polarization_transmission,
    ),
    AnalysisDataConverter(
        old_analysis="huygens_psf",
        new_analysis="HuygensPSF",
        settings_class="HuygensPSFSettings",
        module="zospy.analyses.psf.huygens_psf",
        data_type="dataframe",
        settings_replace_keys={
            "pupil_sample_size": "pupil_sampling",
            "image_sample_size": "image_sampling",
            "type": "psf_type",
            "show_as_type": "show_as",
        },
    ),
    AnalysisDataConverter(
        old_analysis="ray_fan",
        new_analysis="RayFan",
        settings_class="RayFanSettings",
        module="zospy.analyses.raysandspots.ray_fan",
        data_type="dataclass",
        data_class="RayFanResult",
        data_conversion=r"""
$map(["Tangential", "Sagittal"], function($d) {
    { $lowercase($d): [$.data.Data.data.$sift(function ($v, $k) { $contains($k, $d) })
        .$each(function($v, $k) {
            {
                "field_number": $number($match($k, /field number (\d+)/).groups[0]),
                "field_coordinate": $match($k, /= (\d+[\.,]\d+) \((\w+)\)/){
                    "value": $number($replace(groups[0], ",", ".")),
                    "unit": groups[1]
                },
                "data": $v.data{
                    "index": data.($[0]),
                    "columns": [$filter(columns, function($v, $i) { $i != 0 }).($replace($, ",", ".").$number())],
                    "data": $map(data, function($v){ $filter($v, function($vv, $i) { $i != 0}) }),
                    "index_names": [columns[0]],
                    "column_names": column_names
                }
            }
        })]
    }
}) ~> $merge
""",
    ),
    AnalysisDataConverter(
        old_analysis="single_ray_trace",
        new_analysis="SingleRayTrace",
        settings_class="SingleRayTraceSettings",
        module="zospy.analyses.raysandspots.single_ray_trace",
        data_type="dataclass",
        data_class="SingleRayTraceResult",
        data_conversion=r"""
[
    {
        "units": "Millimeters",
        "wavelength": $match($.data.RawTextData[$contains($, "Wavelength")], /(\d+[\.,]\d+)\s+([\w\u00B5]+)\s+/){
            "value": groups[0].$replace(",", ".").$number(),
            "unit": groups[1]
        }
    },
    $.data.Settings.data{
        "coordinates": GlobalCoordinates ? "Global coordinates relative to surface 1" : "Local",
        "normalized_x_field_coord": Hx,
        "normalized_y_field_coord": Hy,
        "normalized_x_pupil_coord": Px,
        "normalized_y_pupil_coord": Py
    },
    $.data.Data.data{
        "real_ray_trace_data": RealRayTraceData.data,
        "paraxial_ray_trace_data": ParaxialRayTraceData.data,
        "ym_um_yc_uc_ray_trace_data": null
    }
] ~> $merge
""",
        settings_conversion='$each($.data.Settings.data, function($v, $k) {{ $camelToSnake($k): $v}}) ~> $merge ~> | $ | { "field": $.field = "All" ? 0 } |',
        postprocess=postprocess_single_ray_trace,
    ),
    AnalysisDataConverter(
        old_analysis="cardinal_points",
        new_analysis="CardinalPoints",
        settings_class="CardinalPointsSettings",
        module="zospy.analyses.reports.cardinal_points",
        data_type="dataclass",
        data_class="CardinalPointsResult",
        data_conversion=r"""
(
    $series := $.data.Data.data.$map($zip(index, data), function($v, $i) {{"group": $v[0][0], "property": $v[0][1], "value": $v[1][0]}}){group: {property: value}};
    $series{
        "starting_surface": Surface.`Starting surface`,
        "ending_surface": Surface.`Ending surface`,
        "wavelength": General.Wavelength,
        "orientation": General.Orientation,
        "lens_units": General.`Lens units`,
        "cardinal_points": $merge($each(`Object Space`, function($v, $k){
            {$camelToSnake($k): {
                "object": $v,
                "image": $lookup(`Image Space`, $k)
            }}
        }))
    }
)
""",
        settings_replace_keys={
            "surface1": "surface_1",
            "surface2": "surface_2",
        },
    ),
    AnalysisDataConverter(
        old_analysis="surface_data",
        new_analysis="SurfaceData",
        settings_class="SurfaceDataSettings",
        module="zospy.analyses.reports.surface_data",
        data_type="dataclass",
        data_class="SurfaceDataResult",
        data_conversion=r"""
(
    $series := $.data.Data.data.$map($zip(index, data), function($v, $i) {{"group": $v[0][0], "property": $v[0][1], "value": $v[1][0]}}){group: {$string(property): value}};
    $series.$merge([
        $each(General, function($v, $k) {{ $camelToSnake($k): $v}}) ~> |$|{}, "title"|,
        Surface{"thickness": Thickness, "diameter": Diameter, "edge_thickness": {"x": `X Edge Thick`, "y": `Y Edge Thick`}},
        {
            "material": {
                "indices": [
                    {
                        "number": 1,
                        "wavelength": 0.543,
                        "index": 1.5
                    }
                ],
                "best_fit_glass": IndexOfRefraction.`Best Fit Glass`,
                "glass": null
            },
            "surface_powers": $map($zip(["as_situated", "in_air"], [SurfacePowerAsSituated, SurfacePowerInAir]), function($v){
                {
                    $v[0]: $v[1]{
                        "surf": {"2": `Surf 2`, "3": `Surf 3`},
                        "power": {"2.0,3.0": `Power 2 3`},
                        "efl": {"2.0,3.0": `EFL 2 3`},
                        "f_number": {"2.0,3.0": `F/# 2 3`}
                    }
                }
            }) ~> $merge,
            "shape_factor": Other.`Shape Factor`
        }
    ])
)
""",
    ),
    AnalysisDataConverter(
        old_analysis="system_data",
        new_analysis="SystemData",
        settings_class="SystemDataSettings",
        module="zospy.analyses.reports.system_data",
        data_type="dataclass",
        data_class="SystemDataResult",
        data_conversion=r"""
(
    $replaceKeys := {
        "Effective Focal Length": "effective_focal_length_air",
        "Effective Focal Length 1": "effective_focal_length_image",
        "Primary Wavelength [\u00b5m]": "primary_wavelength",
        "Temperature (C)": "temperature",
        "Pressure (ATM)": "pressure"
    };
    $preprocessKey := function($k){ $k in $replaceKeys.$keys() ? $lookup($replaceKeys, $k) : $camelToSnake($k).$replace("j/e", "j_e").$replace("f/#", "f_number") };
    $preprocessValue := function($v){ $v in ["On", "Off"] ? $v = "On" : $v};
    $.data.Data.data{
        "general_lens_data": GeneralLensData.data.$each(function($v, $k){{ $preprocessKey($k): $preprocessValue($v) }}) ~> $merge
            ~> | $ | $merge([{
                "system_aperture": system_aperture.$split(" = "){ "type": $[0], "value": $[1] },
                "glass_catalogs": glass_catalogs[],
                "apodization": apodization.$match(/(\w+), factor = (\d+[.,]\d+(?:E[+-]\d+))/){ "type": groups[0], "factor": groups[1].$number() },
                "effective_focal_length_air": effective_focal_length_air.$match(/\d+\.\d+/).match.$number(),
                "effective_focal_length_image": effective_focal_length_image.$match(/\d+\.\d+/).match.$number()
            }]), ["include_calculated_data_in_session_file_1"] |,
        "fields": Fields.data{
            "number_of_fields": Info.data.Fields,
            "field_type": Info.data.`Field Type 1`,
            "fields": [$map(Data.data.data, function($v){{"number": $v[0], "x_value": $v[1], "y_value": $v[2], "weight": $v[3] }})]
        },
        "vignetting": [$map(VignettingFactors.data.data, function($v){{"number": $v[0], "vdx": $v[1], "vdy": $v[2], "vcx": $v[3], "vcy": $v[4], "van": $v[5]}})],
        "wavelengths": Wavelengths.data{
            "number_of_wavelengths": Info.data.Wavelengths,
            "units": Info.data.Units,
            "wavelengths": [$map(Data.data.data, function($v){{"number": $v[0], "value": $v[1], "weight": $v[2]}})]
        },
        "abcd_matrix": PredictedCoordinateABCDMatrix.data
})
""",
        settings_conversion="$.data.Settings",
    ),
    AnalysisDataConverter(
        old_analysis="curvature",
        new_analysis="Curvature",
        settings_class="CurvatureSettings",
        module="zospy.analyses.surface.curvature",
        data_type="dataclass",
        data_class="CurvatureResult",
        data_conversion=r"""
{
    "width": 0,
    "decenter_x": 0,
    "decenter_y": 0,
    "decenter_unit": "Millimeters",
    "data": $.data.Data.data
}
""",
        settings_replace_keys={
            "remove_option": "remove",
            "consider_off_axis_aperture": "off_axis_coordinates",
            "best_fit_sphere_options": "bfs_criterion",
            "reverse_direction": "bfs_reverse_direction",
        },
    ),
    AnalysisDataConverter(
        old_analysis="wavefront_map",
        new_analysis="WavefrontMap",
        settings_class="WavefrontMapSettings",
        module="zospy.analyses.wavefront.wavefront_map",
        data_type="dataframe",
        settings_conversion=r'$each($.data.Settings.data, function($v, $k) {{ $camelToSnake($k): $v}}) ~> | $ | {"surface": surface = 0 ? "Image" } | ~> $merge',
    ),
    AnalysisDataConverter(
        old_analysis="zernike_standard_coefficients",
        new_analysis="ZernikeStandardCoefficients",
        settings_class="ZernikeStandardCoefficientsSettings",
        module="zospy.analyses.wavefront.zernike_standard_coefficients",
        data_type="dataclass",
        data_class="ZernikeStandardCoefficientsResult",
        data_conversion=r"""
[
    $.data.Settings.data{
        "subaperture_decenter_sx": Sx,
        "subaperture_decenter_sy": Sy,
        "subaperture_radius_sr": Sr
    },
    $.data.Data.data.GeneralData.data.$map($zip(index, data), function($v, $i) {{$camelToSnake($v[0]):  {"value": $v[1][0], "unit": $v[1][1]}}}){
        "surface": surface.value,
        "field": field{"value": value, "unit": unit.$replace(/[\(\)]/, "")},
        "wavelength": wavelength,
        "peak_to_valley_to_chief": peak_to_valley_to_chief,
        "peak_to_valley_to_centroid": peak_to_valley_to_centroid,
        "from_integration_of_the_fitted_coefficients": $merge([
            $map(["rms_to_chief", "rms_to_centroid", "variance"], function($v){ {$v: $lookup($, $v)} }),
            {"strehl_ratio": $.strehl_ratio_est.value }
        ]),
        "from_integration_of_the_rays": $merge([
            $map(["rms_to_chief", "rms_to_centroid", "variance"], function($v){ {$v: $lookup($, $v)} }),
            {"strehl_ratio": $.strehl_ratio_est.value }
        ]),
        "rms_fit_error": rms_fit_error,
        "maximum_fit_error": maximum_fit_error
    },
    $.data.Data.data.Coefficients.data{
        "coefficients": $map(data, function($v, $i){ {($i + 1).$string(): {"value": $v[0], "formula": $v[2] }}}) ~>
        $merge
    }
] ~> $merge
""",
        settings_replace_keys={
            "sample_size": "sampling",
            "maximum_number_of_terms": "maximum_terms",
        },
    ),
]


def convert_reference_data_files(converter: AnalysisDataConverter):
    for file in INPUT_FOLDER.glob(f"*{converter.old_analysis}*.json"):
        reference_data = json.loads(file.read_text())

        converted_data = converter.convert_data(reference_data)

        # Attempt to load the data as an AnalysisResult to ensure it is valid
        try:
            AnalysisResult.from_json(json.dumps(converted_data, indent=4))
        except ValidationError as e:
            print(f"Error converting {file.name}: {e}")

        output_file = OUTPUT_FOLDER / file.name
        output_file.write_text(json.dumps(converted_data, indent=4))


if __name__ == "__main__":
    # Initialize ZOS instance, to check constants existence
    zos = ZOS()

    for converter in CONVERTERS:
        convert_reference_data_files(converter)
