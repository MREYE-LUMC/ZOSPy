"""
Helper functions that are used in the ray tracing notebook.

- `zernike_coefficients_vs_field`: Perform a Zernike Coefficients vs Fields analysis.
- `_structure_zernike_coefficients_vs_field_result`: Obtain data from the Zernike Coefficients vs Fields text output.
- `get_ray_output_angle`: Calculate the output angle of a ray with respect to the optical axis and a reference point.
- `InputOutputAngles`: NamedTuple to store the input and output angles of a ray.
- `get_retina_locations`: Get the retina locations for a given row in the input-output angles DataFrame.
- `euclidean_distance`: Convert two series of tuples to NumPy arrays and calculate the element-wise euclidean distance.
- `find_ellipse_intersection`: Find the intersection between a straight line (light ray) and an ellipse.
- `ellipse_arc_length`: Calculate the arc length of an ellipse between two points.
"""
from __future__ import annotations

import os
import re
from io import StringIO
from tempfile import mkstemp

import pandas as pd

import zospy.api.config as _config
from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def _structure_zernike_coefficients_vs_field_result(line_list: list[str], coefficients):
    """Structures the result of a zernike coefficients vs field analysis.

    Parameters
    ----------
    line_list: list of str
        The line list obtained by reading in the results

    Returns
    -------
    AttrDict
        The results embedded in a AttrDict
    """
    # Create output dict
    res = AttrDict()

    # Replace \ufeff
    line_list[0] = line_list[0].strip().replace("\ufeff", "")

    # Register landmarks
    landmarks = ["wavelength:", "field:"]
    comp = re.compile(rf'^({"|".join(landmarks)})', re.IGNORECASE)
    inds = {
        comp.match(line).group().lower(): {"rnum": rnum, "name": comp.match(line).group()}
        for rnum, line in enumerate(line_list)
        if comp.match(line)
    }

    # if ('field:' not in inds) and ('wavelength:' in inds):  # fields are not printed, happens with higher order
    # Zernikes

    # Add full text header
    res["Header"] = "".join(line_list[: inds["wavelength:"]["rnum"] + 1])

    valuepat_start = re.compile(r"^((-)?\d+\.\d+)")
    valuepat_any = re.compile(r"((-)?\d+(\.\d+)?)")
    res["HeaderData"] = pd.DataFrame(columns=["Value", "Unit"])
    for line in line_list[: inds["wavelength:"]["rnum"] + 1]:
        if ":" in line:
            spl = line.split(":", 1)
            ind = "".join([item.title() for item in spl[0].split()])
            nvals = len(valuepat_any.findall(spl[1].replace(",", ".")))
            dat = spl[1].strip().split(maxsplit=nvals)
            if len(dat) == 0:
                val = ""
                unit = ""
                res["HeaderData"].loc[ind] = [val, unit]
            elif len(dat) == 1:
                if valuepat_start.search(dat[0].replace(",", ".")):  # value is number
                    val = float(dat[0].replace(",", "."))
                else:
                    val = dat[0]
                unit = ""
                res["HeaderData"].loc[ind] = [val, unit]
            elif len(dat) == 2:
                if valuepat_start.search(dat[0].replace(",", ".")):  # value is number
                    val = float(dat[0].replace(",", "."))
                else:
                    val = dat[0]
                unit = dat[1]
                res["HeaderData"].loc[ind] = [val, unit]
            else:
                for ii in range(len(dat) - 1):
                    if valuepat_start.search(dat[ii].replace(",", ".")):  # value is number
                        val = float(valuepat_start.search(dat[ii].replace(",", ".")).group())
                    else:
                        val = dat[ii]
                    unit = dat[-1]
                    res["HeaderData"].loc["{}_{}".format(ind, ii)] = [val, unit]

    if line_list[inds["wavelength:"]["rnum"] + 1].startswith("Field:"):  # field collumn contains zernike numbers
        res["ZernikeVsField"] = pd.read_csv(
            StringIO("".join([line.rstrip("\t\n") + "\n" for line in line_list[inds["wavelength:"]["rnum"] + 1 :]])),
            # Remove trailing \t to prevent empty unnamed column
            delimiter="\t",
            decimal=_config.DECIMAL_POINT,
            index_col=0,
        )

        res["ZernikeVsField"].columns = [int(ii.strip()) for ii in res["ZernikeVsField"].columns]
    else:
        res["ZernikeVsField"] = pd.read_csv(
            StringIO("".join([line.rstrip("\t\n") + "\n" for line in line_list[inds["wavelength:"]["rnum"] + 1 :]])),
            # Remove trailing \t to prevent empty unnamed column
            delimiter="\t",
            decimal=_config.DECIMAL_POINT,
            index_col=0,
            header=None,
        )
        if coefficients == "0":
            if "Zernike Fringe Polynomial" in res.Header:
                df_hdr = list(range(1, 38, 1))
            else:
                df_hdr = list(range(1, 232, 1))
        else:
            df_hdr = []
            for item in coefficients.replace(",", " ").split(" "):
                if item == "":
                    continue
                elif re.match(r"\d+-\d+", item):
                    df_hdr += list(range(int(item.split("-")[0]), int(item.split("-")[1]) + 1, 1))
                else:
                    df_hdr += [int(item)]
        res["ZernikeVsField"].columns = df_hdr

    return res


def zernike_coefficients_vs_field(
    oss: OpticStudioSystem,
    coefficients: str = "1-6",
    wavelength: int = 1,
    coefficients_type: str | constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes = "Fringe",
    field_scan: str | constants.Analysis.Settings.Aberrations.FieldScanDirections = "+y",
    field_density: int = 20,
    sampling: str | constants.Analysis.SampleSizes = "64x64",
    obscuration: float = 0.5,
    minimum_plot_scale: float = 0,
    maximum_plot_scale: int = 0,
    oncomplete: OnComplete = OnComplete.Close,
    txtoutfile: str = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Zernike Coefficients vs Field Analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    coefficients: str
        The Zernike coefficients that are calculated, e.g. '1-6'. See OpticStuio documentation for further info.
        Defaults to '1-6'.
    wavelength: int
        The wavelength number that is to be used. Defaults to 1.
    coefficients_type: str | constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes
        Determines which Zernike coefficients are to be calculated. Shoud be one of ['Fringe', 'Standard', 'Annular'].
        Defaults to 'Fringe'.
    field_scan: str | constants.Analysis.Settings.Aberrations.FieldScanDirections
        The field scan direction. Should be one of ['+y', '-y', '+x', '-x']. Defaults to '+y'.
    field_density: int
        The field density. Defaults to 20.
    sampling: str | constants.Analysis.SampleSizes
        The sampling, formatted as '...x...' where the dots represent numbers (e.g. '64x64'). Defaults to '64x64'.
    obscuration: float
        The obscuration factor. Is only used when coefficient_type == 'Annular'. Defaults to 0.5.
    minimum_plot_scale: float
        The minimum plot scale. When 0, OpticStudio will choose the value. Defaults to 0.
    maximum_plot_scale: float
        The maximum plot scale. When 0, OpticStudio will choose the value. Defaults to 0.
    oncomplete: OnComplete
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    txtoutfile: str | None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.


    Returns
    -------
    AnalysisResult
        A ZernikeCoefficientsVsField analysis result
    """
    analysis_type = constants.Analysis.AnalysisIDM.ZernikeCoefficientsVsField

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    # Apply settings
    analysis.Settings.Coefficients = coefficients
    analysis.set_wavelength(wavelength)
    analysis.Settings.ZernikeCoefficientType = constants.process_constant(
        constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes, coefficients_type
    )
    if isinstance(field_scan, str):
        field_scan = (
            f"{field_scan[0]}_{field_scan[-1]}".replace("+", "Plus").replace("-", "Minus").title()
        )  # convert to e.g. 'Plus_y'
    analysis.Settings.FieldScanDirection = constants.process_constant(
        constants.Analysis.Settings.Aberrations.FieldScanDirections, field_scan
    )
    analysis.Settings.FieldDensity = field_density
    analysis.Settings.SampleSize = constants.process_constant(
        constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(sampling)
    )
    if (
        analysis.Settings.ZernikeCoefficientType
        == constants.Analysis.Settings.Aberrations.ZernikeCoefficientTypes.Annular
    ):  # only set when possible
        analysis.Settings.ObscurationFactor = obscuration
    analysis.Settings.ScaleMinimum = minimum_plot_scale
    analysis.Settings.ScaleMaximum = maximum_plot_scale

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding="utf-16-le")]

    if "Insufficient Memory Available!" in line_list[0]:
        data = None  # analysis failed
    else:
        data = _structure_zernike_coefficients_vs_field_result(line_list, coefficients)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Retrieve settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["Coefficients"] = str(analysis.Settings.Coefficients)
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["ZernikeCoefficientType"] = str(analysis.Settings.ZernikeCoefficientType)
    settings.loc["FieldScanDirection"] = str(analysis.Settings.FieldScanDirection)
    settings.loc["FieldDensity"] = str(analysis.Settings.FieldDensity)
    settings.loc["SampleSize"] = str(analysis.Settings.SampleSize)
    if str(analysis_type) == "Annular":  # only set when possible
        settings.loc["ObscurationFactor"] = str(analysis.Settings.ObscurationFactor)
    settings.loc["MinimumPlotScale"] = analysis.Settings.ScaleMinimum
    settings.loc["MaximumPlotScale"] = analysis.Settings.ScaleMaximum
    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        RawTextData=line_list,
        TxtOutFile=txtoutfile,
    )  # Set additional params

    # cleanup
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)
