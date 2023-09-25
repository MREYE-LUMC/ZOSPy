"""Zemax OpticStudio analyses from the Wavefront category."""

from __future__ import annotations

import os
import re
from tempfile import mkstemp

import numpy as np
import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def _structure_zernike_standard_coefficients_result(line_list: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Structures the result of a zernike standard coefficients analysis.

    Parameters
    ----------
    line_list: list of str
        The line list obtained by reading in the results

    Returns
    -------
    (pd.DataFrame, pd.DataFrame)
        Two dataframes, respectively the general results and the coefficients
    """
    zlinepat = re.compile(r"^Z\s+\d+")
    valuepat_start = re.compile(r"^((-)?\d+\.\d+)")
    valuepat_any = re.compile(r"((-)?\d+(\.\d+)?)")

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
            nvals = len(valuepat_any.findall(spl[1].replace(",", ".")))
            dat = spl[1].strip().split(maxsplit=nvals)
            if len(dat) == 0:
                val = ""
                unit = ""
                general_data.loc[ind] = [val, unit]
            elif len(dat) == 1:
                if valuepat_start.search(dat[0].replace(",", ".")):  # value is number
                    val = float(dat[0].replace(",", "."))
                else:
                    val = dat[0]
                unit = ""
                general_data.loc[ind] = [val, unit]
            elif len(dat) == 2:
                if valuepat_start.search(dat[0].replace(",", ".")):  # value is number
                    val = float(dat[0].replace(",", "."))
                else:
                    val = dat[0]
                unit = dat[1]
                general_data.loc[ind] = [val, unit]
            else:
                for ii in range(len(dat) - 1):
                    if valuepat_start.search(dat[ii].replace(",", ".")):  # value is number
                        val = float(valuepat_start.search(dat[ii].replace(",", ".")).group())
                    else:
                        val = dat[ii]
                    unit = dat[-1]
                    general_data.loc["{}_{}".format(ind, ii)] = [val, unit]
    zernike_data = pd.DataFrame(index=zernike_arr[:, 0].copy(), columns=["Value", "Unit", "Function"])
    zernike_data.loc[zernike_arr[:, 0], "Value"] = list(
        map(lambda s: float(s.replace(",", ".")), zernike_arr[:, 1].copy())
    )
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
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str | int
        The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants integer.
    maximum_term: int
        The maximum Zernike term, defaults to 37.
    wavelength: int
        The wavelength number that is to be used. Defaults to 1 (the first wavelength).
    field:
        The field that is to be analyzed. Defaults to 1.
    reference_opd_to_vertex: bool
        If the OPD should be referenced to vertex. Defaults to False.
    surface: str | int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    sx: float
        The sx.
    sy: float
        The sy.
    sr: float
        The sr.
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
    analysis.Settings.SampleSize = getattr(constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(sampling))
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
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]

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
