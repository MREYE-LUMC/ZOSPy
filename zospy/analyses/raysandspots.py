"""Zemax OpticStudio analyses from the Rays and Spots category."""

from __future__ import annotations

import os
import re
from io import StringIO
from tempfile import mkstemp
from typing import Any

import numpy as np
import pandas as pd

import zospy.api.config as _config
from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def _structure_ray_trace_data_result(line_list: list[str]) -> dict[str, Any]:
    """Structures the result of a ray trace data report.

    Parameters
    ----------
    line_list: list[str]
        The line list obtained by reading in the results

    Returns
    -------
    dict
        The results structured in a dictionary
    """
    # Create output dict
    res = AttrDict()

    # Add header
    hdr = line_list[0].strip().replace("\ufeff", "")
    res["Header"] = hdr

    # Register landmarks
    landmarks = [
        "Real Ray Trace Data",
        "Paraxial Ray Trace Data",
        "Trace of Paraxial Y marginal, U marginal, Y chief, U chief only",
    ]
    comp = re.compile(rf'^({"|".join(landmarks)})', re.IGNORECASE)
    inds = {
        comp.match(line).group().lower(): {"rnum": rnum, "name": comp.match(line).group()}
        for rnum, line in enumerate(line_list)
        if comp.match(line)
    }

    order_of_appearance = [item[0] for item in sorted(inds.items(), key=lambda x: x[1]["rnum"])]

    # Add general lens data
    for target in inds.keys():
        section_start = inds[target]["rnum"] + 1  # + 1 to ignore section title

        # Get endpoint
        if order_of_appearance.index(target) == len(inds) - 1:
            section_end = len(line_list)
        else:
            target2 = order_of_appearance[order_of_appearance.index(target) + 1]
            section_end = inds[target2]["rnum"]

        # Read as dataframe
        df = pd.read_csv(
            StringIO("".join(line_list[section_start:section_end]).replace(" ", "")),
            delimiter="\t",
            decimal=_config.DECIMAL_POINT,
        )

        # Recover case of target
        keyname = inds[target]["name"].replace(" ", "")

        # Add to result dictionary
        res[keyname] = df

    return res


def single_ray_trace(
    oss: OpticStudioSystem,
    hx: float = 0,
    hy: float = 0,
    px: float = 0,
    py: float = 1,
    wavelength: str | int = 1,
    field: str | int = 0,
    raytrace_type: constants.Analysis.Settings.Aberrations.RayTraceType | str = "DirectionCosines",
    global_coordinates: bool = False,
    oncomplete: OnComplete | str = OnComplete.Close,
    txtoutfile: str | None = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Single Ray Trace Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    hx: float
        Normalized X Field Coord. Defaults to 0.
    hy: float
        Normalized Y Field Coord. Defaults to 0.
    px: float
        Normalized X Pupil Coord. Defaults to 0.
    py: float
        Normalized Y Pupil Coord. Defaults to 1.
    raytrace_type: zospy.api.constants.Analysis.Settings.Aberrations.RayTraceType
        The Ray Trace type (e.g. 'DirectionCosines') that is calculated. Defaults to 'DirectionCosines'.
    wavelength: int
        The wavelength number that is to be used. Must be an integer specifying the wavelength number.
        Defaults to 1.
    field: int
        The field number that is to be used. Must be an integer specifying the field number. "Arbitrary" is 0. Defaults
        to 0.
    global_coordinates: bool
        Defines if global coordinates are used. Defaults to False.
    oncomplete: OnComplete | str
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
        A Single Ray Trace result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.RayTrace

    # Temp file
    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    analysis.Settings.Hx = hx
    analysis.Settings.Hy = hy
    analysis.Settings.Px = px
    analysis.Settings.Py = py
    analysis.set_wavelength(wavelength)
    analysis.set_field(field)
    analysis.Settings.Type = constants.process_constant(
        constants.Analysis.Settings.Aberrations.RayTraceType, raytrace_type
    )
    analysis.Settings.UseGlobal = global_coordinates

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]
    data = _structure_ray_trace_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["Hx"] = analysis.Settings.Hx
    settings.loc["Hy"] = analysis.Settings.Hy
    settings.loc["Px"] = analysis.Settings.Px
    settings.loc["Py"] = analysis.Settings.Py
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["Field"] = analysis.get_field()
    settings.loc["Type"] = str(analysis.Settings.Type)
    settings.loc["GlobalCoordinates"] = analysis.Settings.UseGlobal

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

    # cleanup if needed
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)


def ray_fan(
    oss: OpticStudioSystem,
    plot_scale: float = 0,
    number_of_rays: int = 20,
    field: str | int = "All",
    wavelength: str | int = "All",
    tangential: constants.Analysis.Settings.Fans.TangentialAberrationComponent | str = "Aberration_Y",
    sagittal: constants.Analysis.Settings.Fans.SagittalAberrationComponent | str = "Aberration_X",
    surface: str | int = "Image",
    use_dashes: bool = False,
    vignetted_pupil: bool = True,
    check_apertures: bool = True,
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Ray Fan Analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    plot_scale: int | float
        Sets the maximum vertical scale for the plots. When 0, automatic scaling is used. Defaults to 0.
    number_of_rays: int
        This is the number of rays traced on each side of the origin of the plot.
    field: str or int
        The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 'All'.
    wavelength: str | int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number.
        Defaults to 'All'.
    tangential: str | int
        The aberration component that is plotted for the tangential fan. Accepts sting ('Aberration_Y' or
        'Aberration_X') or int (respectively 0 and 1). Defaults to 'Aberration_Y'.
    sagittal: str | int
        The aberration component that is plotted for the sagittal fan. Accepts sting ('Aberration_X' or
        'Aberration_Y') or int (respectively 0 and 1). Defaults to 'Aberration_X'.
    surface: str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    use_dashes: bool
        Defines whether solid lines or dashes are used to differentiate curves. Defaults to False.
    vignetted_pupil: bool
        Defines whether the pupil axis is scaled to the unvignetted pupil or not. Defaults to True.
    check_apertures: bool
        Defines whether only rays that pass all surface apertures are drawn or not. Defaults to True.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A Ray Fan result.
    """
    # Set up analysis type
    analysis_type = constants.Analysis.AnalysisIDM.RayFan
    analysis = new_analysis(oss, analysis_type)

    # Settings for ray fan
    analysis.set_field(field)
    analysis.set_surface(surface)
    analysis.set_wavelength(wavelength)
    analysis.Settings.NumberOfRays = number_of_rays
    analysis.Settings.PlotScale = plot_scale
    analysis.Settings.CheckApertures = check_apertures
    analysis.Settings.VignettedPupil = vignetted_pupil
    analysis.Settings.UseDashes = use_dashes
    analysis.Settings.Sagittal = constants.process_constant(
        constants.Analysis.Settings.Fans.SagittalAberrationComponent, sagittal
    )
    analysis.Settings.Tangential = constants.process_constant(
        constants.Analysis.Settings.Fans.TangentialAberrationComponent, tangential
    )

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Parse results
    results = analysis.GetResults()
    data = AttrDict()
    data["Header"] = "Ray Fan Data"
    for ii in range(results.DataSeries.Length):
        # get raw .NET data into numpy array
        ds = results.GetDataSeries(ii)
        xRaw = np.asarray(tuple(ds.XData.Data))
        yRaw = np.asarray(tuple(ds.YData.Data))

        # Reshape data
        x = xRaw
        y = yRaw.reshape(ds.YData.Data.GetLength(0), ds.YData.Data.GetLength(1))

        # Make data frame
        df = {ds.XLabel: x}
        for jj, label in enumerate(ds.SeriesLabels):
            df[label] = y[:, jj]
        df = pd.DataFrame(data=df)

        # Add data to dictionary
        data[ds.Description] = df

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)
    settings.loc["Field"] = analysis.get_field()
    settings.loc["Surface"] = analysis.Settings.Surface.GetSurfaceNumber()
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["NumberOfRays"] = analysis.Settings.NumberOfRays
    settings.loc["PlotScale"] = analysis.Settings.PlotScale
    settings.loc["CheckApertures"] = analysis.Settings.CheckApertures
    settings.loc["VignettedPupil"] = analysis.Settings.VignettedPupil
    settings.loc["UseDashes"] = analysis.Settings.UseDashes
    settings.loc["Sagittal"] = str(analysis.Settings.Sagittal)
    settings.loc["Tangential"] = str(analysis.Settings.Tangential)

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )  # Set additional params

    return analysis.complete(oncomplete, result)
