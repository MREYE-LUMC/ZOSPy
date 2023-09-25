"""Zemax OpticStudio analyses from the Polarization category."""

from __future__ import annotations

import os
import re
import struct
from dataclasses import dataclass
from io import StringIO
from tempfile import mkstemp

import pandas as pd

import zospy.api.config as _config
from zospy import utils
from zospy.analyses.base import AnalysisResult, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def _get_number_field(name: str, text: str) -> str:
    return re.search(
        rf"{re.escape(name)}\s*:\s*([-+]?(\d+({re.escape(_config.DECIMAL_POINT)}\d*)?|{re.escape(_config.DECIMAL_POINT)}\d+)(?:[Ee][-+]?\d+)?)",
        text,
    ).group(1)


@dataclass
class PupilMapData:
    """Pupil map analysis data."""

    Header: str
    Wavelength: float
    FieldPos: float
    XField: float
    YField: float
    XPhase: float
    YPhase: float
    Configs: int
    Surface: int
    Transmission: float
    Table: pd.DataFrame


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
    analysis_settings.ModifySettings(cfgoutfile, "PPM_JX", utils.pyutils.xtoa(jx, thousands_separator=None))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_JY", utils.pyutils.xtoa(jy, thousands_separator=None))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_PX", utils.pyutils.xtoa(x_phase, thousands_separator=None))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_PY", utils.pyutils.xtoa(y_phase, thousands_separator=None))
    analysis_settings.ModifySettings(
        cfgoutfile, "PPM_WAVE", utils.pyutils.xtoa(int(wavelength), thousands_separator=None)
    )
    analysis_settings.ModifySettings(cfgoutfile, "PPM_FIELD", utils.pyutils.xtoa(int(field), thousands_separator=None))
    if isinstance(surface, str):
        analysis_settings.ModifySettings(cfgoutfile, "PPM_SURFACE", surface)
    else:
        analysis_settings.ModifySettings(
            cfgoutfile, "PPM_SURFACE", utils.pyutils.xtoa(surface, thousands_separator=None)
        )
    sampling_value = getattr(
        constants.Analysis.SampleSizes_ContrastLoss,
        utils.zputils.standardize_sampling(sampling),
    ).value__
    analysis_settings.ModifySettings(
        cfgoutfile, "PPM_SAMP", utils.pyutils.xtoa(sampling_value - 1, thousands_separator=None)
    )
    analysis_settings.ModifySettings(cfgoutfile, "PPM_ADDCONFIG", str(add_configs))
    analysis_settings.ModifySettings(cfgoutfile, "PPM_SUBCONFIGS", str(sub_configs))

    analysis_settings.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)

    with open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding()) as f:
        text_output = f.read()
        line_list = text_output.split("\n")

    # Get header
    header = line_list[0].strip().replace("\ufeff", "")

    # Read data table as dataframe
    df = pd.read_csv(
        StringIO("\n".join(line_list[17:]).replace(" ", "")),
        delimiter="\t",
        decimal=_config.DECIMAL_POINT,
    )

    data = PupilMapData(
        Header=header,
        Wavelength=utils.pyutils.atox(_get_number_field("Wavelength", text_output), dtype=float),
        FieldPos=utils.pyutils.atox(_get_number_field("Field Pos", text_output), dtype=float),
        XField=utils.pyutils.atox(_get_number_field("X-Field", text_output), dtype=float),
        YField=utils.pyutils.atox(_get_number_field("Y-Field", text_output), dtype=float),
        XPhase=utils.pyutils.atox(_get_number_field("X-Phase", text_output), dtype=float),
        YPhase=utils.pyutils.atox(_get_number_field("Y-Phase", text_output), dtype=float),
        Configs=utils.pyutils.atox(_get_number_field("Configs", text_output), dtype=int),
        Surface=utils.pyutils.atox(_get_number_field("Surface", text_output), dtype=int),
        Transmission=utils.pyutils.atox(_get_number_field("Transmission", text_output), dtype=float),
        Table=df,
    )

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


@dataclass
class TransmissionData:
    """Transmission analysis data."""

    # TODO add support for multiple fields and wavelengths
    Header: str
    FieldPos: float
    TotalTransmission: float
    Wavelength: float
    Table: pd.DataFrame


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
    subsequently reading in this file.

    WARNING: This analysis currently only works for systems with a single wavelength and field. A
    `NotImplementedException` will be raised if multiple fields or wavelengths are used. See the discussion in
    https://github.com/MREYE-LUMC/ZOSPy/pull/14 for more details.

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

    Raises
    ------
    NotImplementedException
        If multiple fields or wavelenghts are present in the optical system/
    """
    if oss.SystemData.Fields.NumberOfFields > 1 or oss.SystemData.Wavelengths.NumberOfWavelengths > 1:
        raise NotImplementedError("Only systems with a single field and a single wavelength are currently supported.")

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

    with open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding()) as f:
        text_output = f.read()
        line_list = text_output.split("\n")

    # Get header
    header = line_list[0].strip().replace("\ufeff", "")

    # Read data table as dataframe
    df = pd.read_csv(
        StringIO("\n".join(line_list[26:]).strip()),
        delimiter="\t",
        decimal=_config.DECIMAL_POINT,
    )
    df.columns = df.columns.str.strip()

    data = TransmissionData(
        Header=header,
        FieldPos=utils.pyutils.atox(_get_number_field("Field Pos", text_output), dtype=float),
        Wavelength=utils.pyutils.atox(_get_number_field("Wavelength 1", text_output), dtype=float),
        TotalTransmission=utils.pyutils.atox(_get_number_field("Total Transmission", text_output), dtype=float),
        Table=df,
    )

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
