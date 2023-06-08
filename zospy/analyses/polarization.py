"""Zemax OpticStudio analyses from the Polarization category."""

from __future__ import annotations

import os
import re
import struct
from io import StringIO
from tempfile import mkstemp

import numpy as np
import pandas as pd

import zospy.api.config as _config
from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def polarization_pupil_map(
    oss: OpticStudioSystem,
    jx: float = 1,
    jy: float = 0,
    x_phase: float = 0,
    y_phase: float = 0,
    wavelength: int = 1,
    field: int = 1,
    surface: str | int = "Image",
    sampling: str | int = "11x11",
    add_configs: str = "",
    sub_configs: str = "",
    oncomplete: OnComplete | str = OnComplete.Close,
    cfgoutfile: str | None = None,
    txtoutfile: str | None = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Polarization Pupil Map Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    jx: float
        Jones x electric field. Defaults to 1.
    jy: float
        Jones y electric field. Defaults to 0.
    x_phase: float
        Phase of the X component of the Jones electric field in degrees. Defaults to 0.
    y_phase: float
        Phase of the Y component of the Jones electric field in degrees. Defaults to 0.
    wavelength: int
        The wavelength number that is to be used. Should be an integer specifying the wavelength number.
        Defaults to 1.
    field: int
        The field number that is to be used. Must be an integer specifying the field number. Defaults
        to 1.
    surface: str or int
        The surface that is to be analyzed. Either 'Image', or an integer. Defaults to 'Image'.
    sampling: str or int
        The size of the used grid, either string (e.g. '65x65') or int. The integer will be treated as if obtained from
        zospy.constants.Analysis.SampleSizes_ContrastLoss. Defaults to '11x11'.
    add_configs: str
        The add configs string.
    sub_configs: str
        The subtract configs string.
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    cfgoutfile: str or None
        The configuration file to which the current configuration is saved. If None, a temporary file will be created
        and deleted. If string, it should be a full system path with '.CFG' as extension, after which the file will be
        saved in that location. Defaults to
        None.
    txtoutfile: str or None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A Polarization Pupil Map. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.PolarizationPupilMap

    if cfgoutfile is None:
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)
        cleancfg = True
    else:
        if not cfgoutfile.endswith(".CFG"):
            raise ValueError('cfgfile should end with ".CFG"')
        cleancfg = False

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Modify the settings file
    analysis_settings = analysis.GetSettings()
    analysis_settings.SaveTo(cfgoutfile)

    # MODIFYSETTINGS are defined in the ZPL help files: The Programming Tab > About the ZPL > Keywords
    analysis_settings.ModifySettings(cfgoutfile, "PPM_JX", str(jx))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_JY", str(jy))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_PX", str(x_phase))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_PY", str(y_phase))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_WAVE", str(int(wavelength)))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_FIELD", str(int(field)))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_SURFACE", str(surface))
    sampling_value = getattr(
        constants.Analysis.SampleSizes_ContrastLoss, utils.zputils.standardize_sampling(sampling)
    ).value__
    analysis_settings.ModifySettings(cfgoutfile, "PPM_SAMP", str(sampling_value - 1))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_ADDCONFIG", str(add_configs))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_SUBCONFIGS", str(sub_configs))

    analysis_settings.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)

    with open(txtoutfile, "r", encoding="utf-16-le") as f:
        line_list = [line for line in f]

    # Create output dict
    data = AttrDict()

    # Add header
    hdr = line_list[0].strip().replace("\ufeff", "")
    data["Header"] = hdr

    # Add settings
    for ii in range(9):
        name = line_list[7 + ii].replace(" ", "").split(":")[0]
        data[name] = float(re.sub(r"[^\d\.]+", "", line_list[7 + ii]))

    # Read data table as dataframe
    df = pd.read_csv(StringIO("".join(line_list[17:]).replace(" ", "")), delimiter="\t", decimal=_config.DECIMAL)

    # Add to result dictionary
    data["Table"] = df

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["Jx"] = jx
    settings.loc["Jy"] = jy
    settings.loc["X-Phase"] = x_phase
    settings.loc["Y-Phase"] = y_phase
    settings.loc["Wavelength"] = int(wavelength)
    settings.loc["Field"] = int(field)
    settings.loc["Surface"] = surface
    settings.loc["Sampling"] = sampling
    settings.loc["Add Configs"] = add_configs
    settings.loc["Sub Configs"] = sub_configs

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        RawTextData=line_list,
        CgfOutFile=cfgoutfile,
        TxtOutFile=txtoutfile,
    )

    # cleanup if needed
    if cleancfg:
        os.remove(cfgoutfile)
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)


def transmission(
    oss: OpticStudioSystem,
    sampling: str | int = "32x32",
    unpolarized: bool = False,
    jx: float = 1,
    jy: float = 0,
    x_phase: float = 0,
    y_phase: float = 0,
    oncomplete: OnComplete | str = OnComplete.Close,
    cfgoutfile: str | None = None,
    txtoutfile: str | None = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Polarization Transmission Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str or int
        The size of the used grid, either string (e.g. '128x128') or int. The integer will be treated as if obtained
        from zospy.constants.Analysis.SampleSizes. Defaults to '32x32'.
    unpolarized: bool
        Defines if unpolarized light is used. Defaults to False.
    jx: float
        Jones x electric field. Defaults to 1.
    jy: float
        Jones y electric field. Defaults to 0.
    x_phase: float
        Phase of the X component of the Jones electric field in degrees. Defaults to 0.
    y_phase: float
        Phase of the Y component of the Jones electric field in degrees. Defaults to 0.
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    cfgoutfile: str or None
        The configuration file to which the current configuration is saved. If None, a temporary file will be created
        and deleted. If string, it should be a full system path with '.CFG' as extension, after which the file will be
        saved in that location. Defaults to
        None.
    txtoutfile: str or None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A Polarization Transmission Analysis. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.Transmission

    if cfgoutfile is None:
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)
        cleancfg = True
    else:
        if not cfgoutfile.endswith(".CFG"):
            raise ValueError('cfgfile should end with ".CFG"')
        cleancfg = False

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Modify the settings file
    analysis_settings = analysis.GetSettings()
    analysis_settings.SaveTo(cfgoutfile)

    settings_bytestring = b"".join(open(cfgoutfile, "rb").readlines())
    settings_bytearray = bytearray(settings_bytestring)

    # Change settings - all byte indices could only be found via reverse engineering :(
    sampling_value = getattr(constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(sampling)).value__
    settings_bytearray[56] = sampling_value
    settings_bytearray[60] = int(unpolarized)
    settings_bytearray[24:32] = struct.pack("<d", jx)
    settings_bytearray[32:40] = struct.pack("<d", jy)
    settings_bytearray[40:48] = struct.pack("<d", x_phase)
    settings_bytearray[48:56] = struct.pack("<d", y_phase)

    with open(cfgoutfile, "wb") as bfile:
        bfile.write(settings_bytearray)

    analysis_settings.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)

    with open(txtoutfile, "r", encoding="utf-16-le") as f:
        line_list = [line for line in f]

    # Create output dict
    data = AttrDict()

    # Add header and sections
    hdr = line_list[0].strip().replace("\ufeff", "")
    data["Header"] = hdr

    # Go line by line (skip first 5 lines) and sort data into data dictionary
    ifield = 0
    for ind, line in enumerate(line_list[5:], start=5):
        if "Field Pos :" in line:
            field = line.strip()
            if field not in data:
                data[field] = {}
                ifield += 1
                data[field]["Field number"] = ifield
        elif "Transmission at" in line or "Total Transmission " in line:
            line_split = line.split(":")
            data[field][re.sub(" +", " ", line_split[0]).strip()] = float(line_split[-1])
        elif "Wavelength " in line:
            wvl = "Chief ray " + line.strip()
        elif " Surf    	Tot. Tran    	Rel. Tran" in line:
            # Read as dataframe
            df = pd.read_csv(
                StringIO("".join(line_list[ind:]).strip()), dtype=object, delimiter="\t", decimal=_config.DECIMAL
            )
            df.columns = df.columns.str.strip()

            # Find nan, truncate and add to data
            nan_idxs = np.where(df["Tot. Tran"].isna())[0]
            if len(nan_idxs) != 0:
                first_nan = nan_idxs[0]
                df = df.truncate(after=first_nan - 1)
            data[field][wvl] = df

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["Sampling"] = sampling
    settings.loc["Unpolarized"] = unpolarized
    settings.loc["Jx"] = jx
    settings.loc["Jy"] = jy
    settings.loc["X-Phase"] = x_phase
    settings.loc["Y-Phase"] = y_phase

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        RawTextData=line_list,
        CgfOutFile=cfgoutfile,
        TxtOutFile=txtoutfile,
    )

    # cleanup if needed
    if cleancfg:
        os.remove(cfgoutfile)
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)
