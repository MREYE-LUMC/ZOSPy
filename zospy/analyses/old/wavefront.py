"""Zemax OpticStudio analyses from the Wavefront category."""

from __future__ import annotations

import os
import re
from tempfile import mkstemp
from typing import Literal

import numpy as np
import pandas as pd

import zospy.api.config as _config
from zospy.analyses.old.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.utils.pyutils import atox
from zospy.utils.zputils import standardize_sampling, unpack_datagrid
from zospy.zpcore import OpticStudioSystem


def wavefront_map(
    oss: OpticStudioSystem,
    field: int = 1,
    surface: Literal["Image"] | int = "Image",
    wavelength: int = 1,
    show_as: constants.Analysis.ShowAs | str = "Surface",
    rotation: constants.Analysis.Settings.Rotations | str = "Rotate_0",
    sampling: constants.Analysis.SampleSizes | str = "64x64",
    polarization: constants.Analysis.Settings.Polarizations | str | None = None,
    reference_to_primary: bool = False,
    use_exit_pupil: bool = True,
    remove_tilt: bool = False,
    scale: float = 1.0,
    subaperture_x: float = 0.0,
    subaperture_y: float = 0.0,
    subaperture_r: float = 1.0,
    contour_format: str = "",
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Wavefront map analysis.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    field :
        The field that is to be analyzed. Defaults to 1.
    surface  str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    wavelength : int
        The wavelength number to use for the analysis. Defaults to 1.
    show_as : constants.Analysis.ShowAs | str
        Defines the output plot format. Defaults to 'Surface'.
    rotation : constants.Analysis.Settings.Rotations | str
        The rotation or surface plots for viewing. Defaults to 'Rotate_0'.
    sampling : constants.Analysis.SampleSizes | str
        The sampling. Defaults to '64x64'.
    polarization : constants.Analysis.Settings.Polarizations | str | None
        The polarization that is accounted for. When set to None, polarization is ignored. Defaults to None.
    reference_to_primary : bool
        Defines whether the aberrations are referenced to the reference sphere for the used wavelength or for the
        primary wavelength. If True, the reference sphere for the primary wavelength is used. Defaults to False.
    use_exit_pupil : bool
        Defines whether the exit pupil shape is used. Defaults to True.
    remove_tilt : bool
        Defines whether linear x- and y-tilt is removed from the data. Defaults to False.
    scale : float
        The scale factor for surface plots. Defaults to False.
    subaperture_x : float
        The subaperture x. Defaults to 0.0
    subaperture_y : float
        The subaperture t. Defaults to 0.0
    subaperture_r : float
        The subaperture r. Defaults to 1.0
    contour_format : str
        The contour format. Only used when show-As is set to 'Contour'. If set to an empty string, OpticStdio ignores
        it. Defaults to ''.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A wavefront map analysis result.
    """
    analysis_type = constants.Analysis.AnalysisIDM.WavefrontMap

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    # Adjust settings
    analysis.set_field(field)
    analysis.set_surface(surface)
    analysis.set_wavelength(wavelength)
    analysis.Settings.ShowAs = constants.process_constant(constants.Analysis.ShowAs, show_as)
    analysis.Settings.Rotation = constants.process_constant(constants.Analysis.Settings.Rotations, rotation)
    analysis.Settings.Sampling = constants.process_constant(
        constants.Analysis.SampleSizes, standardize_sampling(sampling)
    )
    analysis.Settings.Polarization = constants.process_constant(constants.Analysis.Settings.Polarizations, polarization)
    analysis.Settings.ReferenceToPrimary = reference_to_primary
    analysis.Settings.UseExitPupil = use_exit_pupil
    analysis.Settings.RemoveTilt = remove_tilt
    analysis.Settings.Scale = scale
    analysis.Settings.Subaperture_X = subaperture_x
    analysis.Settings.Subaperture_Y = subaperture_y
    analysis.Settings.Subaperture_R = subaperture_r
    analysis.Settings.ContourFormat = contour_format

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)
    settings.loc["Field"] = analysis.get_field()
    settings.loc["Surface"] = analysis.Settings.Surface.GetSurfaceNumber()
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["ShowAs"] = str(analysis.Settings.ShowAs)
    settings.loc["Rotation"] = str(analysis.Settings.Rotation)
    settings.loc["Sampling"] = str(analysis.Settings.Sampling)
    settings.loc["Polarization"] = str(analysis.Settings.Polarization)
    settings.loc["ReferenceToPrimary"] = analysis.Settings.ReferenceToPrimary
    settings.loc["UseExitPupil"] = analysis.Settings.UseExitPupil
    settings.loc["RemoveTilt"] = analysis.Settings.RemoveTilt
    settings.loc["Scale"] = analysis.Settings.Scale
    settings.loc["Subaperture_X"] = analysis.Settings.Subaperture_X
    settings.loc["Subaperture_Y"] = analysis.Settings.Subaperture_Y
    settings.loc["Subaperture_R"] = analysis.Settings.Subaperture_R
    settings.loc["ContourFormat"] = analysis.Settings.ContourFormat

    data = []
    for ii in range(analysis.Results.NumberOfDataGrids):
        data.append(unpack_datagrid(analysis.Results.DataGrids[ii],
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


def _structure_zernike_standard_coefficients_result(line_list: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Structures the result of a zernike standard coefficients analysis.

    Parameters
    ----------
    line_list : list of str
        The line list obtained by reading in the results

    Returns
    -------
    (pd.DataFrame, pd.DataFrame)
        Two dataframes, respectively the general results and the coefficients
    """
    zlinepat = re.compile(r"^Z\s+\d+")
    valuepat_start = re.compile(r"^((-)?\d+\{}\d+)".format(_config.DECIMAL_POINT))
    valuepat_any = re.compile(r"((-)?\d+(\{}\d+)?)".format(_config.DECIMAL_POINT))

    zernike_lines = [line for line in line_list if (zlinepat.search(line) is not None)]

    general_lines = [line for line in line_list if line not in zernike_lines]
    general_arr = [" ".join(line.split()) for line in general_lines if ":" in line]
    zernike_arr = np.array([line.replace(" ", "").split() for line in zernike_lines])
    general_data = pd.DataFrame(columns=["Value", "Unit"])
    for line in general_arr:
        spl = line.split(":", 1)
        if len(spl) == 1:
            ind = "".join([item.title() for item in spl[0].split()])
            general_data.loc[ind] = ["", ""]
        else:
            ind = "".join([item.title() for item in spl[0].split()])
            nvals = len(valuepat_any.findall(spl[1]))
            dat = spl[1].strip().split(maxsplit=nvals)
            if len(dat) == 0:
                val = ""
                unit = ""
                general_data.loc[ind] = [val, unit]
            elif len(dat) == 1:
                if ind == "Date":
                    val = dat[0]
                elif valuepat_start.search(dat[0]):  # value is number
                    val = atox(dat[0], float)
                else:
                    val = dat[0]
                unit = ""
                general_data.loc[ind] = [val, unit]
            elif len(dat) == 2:
                if valuepat_start.search(dat[0]):  # value is number
                    val = atox(dat[0], float)
                else:
                    val = dat[0]
                unit = dat[1]
                general_data.loc[ind] = [val, unit]
            else:
                for ii in range(len(dat) - 1):
                    if valuepat_start.search(dat[ii]):  # value is number
                        val = atox(valuepat_start.search(dat[ii]).group(), float)
                    else:
                        val = dat[ii]
                    unit = dat[-1]
                    general_data.loc["{}_{}".format(ind, ii)] = [val, unit]
    zernike_data = pd.DataFrame(index=zernike_arr[:, 0].copy(), columns=["Value", "Unit", "Function"])
    zernike_data.loc[zernike_arr[:, 0], "Value"] = list(map(lambda s: atox(s, float), zernike_arr[:, 1].copy()))
    zernike_data.loc[zernike_arr[:, 0], "Unit"] = "waves"
    zernike_data.loc[zernike_arr[:, 0], "Function"] = zernike_arr[:, 3].copy()

    return general_data, zernike_data


def zernike_standard_coefficients(
    oss: OpticStudioSystem,
    sampling: str = "64x64",
    maximum_term: int = 37,
    wavelength: str | int = 1,
    field: str | int = 1,
    reference_opd_to_vertex: bool = False,
    surface: str | int = "Image",
    sx: float = 0.0,
    sy: float = 0.0,
    sr: float = 0.0,
    oncomplete: OnComplete | str = OnComplete.Close,
    txtoutfile: str = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Zernike Standard Coefficient Analysis.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling : str | int
        The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants integer.
    maximum_term : int
        The maximum Zernike term, defaults to 37.
    wavelength : int
        The wavelength number that is to be used. Defaults to 1 (the first wavelength).
    field:
        The field that is to be analyzed. Defaults to 1.
    reference_opd_to_vertex : bool
        If the OPD should be referenced to vertex. Defaults to False.
    surface : str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    sx : float
        The sx.
    sy : float
        The sy.
    sr : float
        The sr.
    oncomplete : OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    txtoutfile : str | None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A ZernikeStandardCoefficients analysis result. Next to the standard data, the raw text return obtained from the
        analysis will be present under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.ZernikeStandardCoefficients

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
    analysis.Settings.SampleSize = getattr(constants.Analysis.SampleSizes, standardize_sampling(sampling))
    analysis.Settings.MaximumNumberOfTerms = maximum_term
    analysis.set_wavelength(wavelength)
    analysis.set_field(field)
    analysis.Settings.ReferenceOBDToVertex = reference_opd_to_vertex  # ToDo: Monitor name with zemax updates
    analysis.set_surface(surface)
    analysis.Settings.Sx = sx
    analysis.Settings.Sy = sy
    analysis.Settings.Sr = sr

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss.ZOS.get_txtfile_encoding())]

    general_data, zernike_data = _structure_zernike_standard_coefficients_result(line_list)
    data = AttrDict(GeneralData=general_data, Coefficients=zernike_data)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["SampleSize"] = str(analysis.Settings.SampleSize)
    settings.loc["MaximumNumberOfTerms"] = analysis.Settings.MaximumNumberOfTerms
    settings.loc["Wavelength"] = analysis.Settings.Wavelength.GetWavelengthNumber()  # Todo Evaluate with 'all'
    settings.loc["Field"] = analysis.Settings.Field.GetFieldNumber()  # Todo Evaluate with 'all'
    settings.loc["ReferenceOBDToVertex"] = analysis.Settings.ReferenceOBDToVertex
    settings.loc["Wavelength"] = analysis.Settings.Wavelength.GetWavelengthNumber()  # Todo Evaluate with 'all'
    settings.loc["Field"] = analysis.Settings.Field.GetFieldNumber()  # Todo Evaluate with 'all'
    settings.loc["ReferenceOBDToVertex"] = analysis.Settings.Surface.GetSurfaceNumber()  # Todo Evaluate with 'all'
    settings.loc["Sx"] = sx
    settings.loc["Sy"] = sy
    settings.loc["Sr"] = sr

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
