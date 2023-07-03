"""Zemax OpticStudio analyses from the MTF category."""

from __future__ import annotations

import os
from tempfile import mkstemp

import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def _correct_fft_through_focus_mtftype_api_bug(oss, analysis, mtftype) -> None:
    """Correction for an API bug in OpticStudio versions < 21.2.

    In these versions, the MTF Type cannot be set through the ZOS-API for the FFT Through Focus MTF
    See also: https://community.zemax.com/zos-api-12/zos-api-setting-mtf-property-type-not-working-730

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    analysis: Analysis
        An FFT Through Focus MTF analysis.
    mtftype: zospy.constants.Analysis.Settings.Mtf.MtfTypes.Modulation

    Returns
    -------
    None
    """
    if oss._ZOS.version < "21.2.0":
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)
        analysis.Settings.SaveTo(cfgoutfile)

        analysis.Settings.ModifySettings(
            cfgoutfile,
            "TFM_TYPE",
            str(int(constants.process_constant(constants.Analysis.Settings.Mtf.MtfTypes, mtftype))),
        )
        analysis.Settings.LoadFrom(cfgoutfile)
        os.remove(cfgoutfile)


def fft_through_focus_mtf(
    oss: OpticStudioSystem,
    sampling: str | int = "64x64",
    deltafocus: float = 0.1,
    frequency: float = 0,
    numberofsteps: int = 5,
    wavelength: str | int = "All",
    field: str | int = "All",
    mtftype: constants.Analysis.Settings.Mtf.MtfTypes | str = "Modulation",
    use_polarization: bool = False,
    use_dashes: bool = False,
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Wrapper around the OpticStudio FFT Through Focus MTF.

    For an in depth explanation of the parameters, see the Zemax OpticStudio user manual

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str | int
        The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants integer.
    deltafocus: float
        The delta focus, defaults to 0.1
    frequency: float
        The frequency. Defaults to 0.
    numberofsteps: int
        The number of steps. Defaults to 5.
    wavelength: str | int
        The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
    field: str | int
        The field to use in the MTF. Either 'All' or an integer specifying the field number.
    mtftype: zospy.constants.Analysis.Settings.Mtf.MtfTypes.Modulation
        The MTF type (e.g. `Modulation`) that is calculated.
    use_polarization: bool
        Use polarization. Defaults to False.
    use_dashes: bool
        Use dashes. Defaults to False.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A FftThroughFocusMtf analysis result
    """
    analysis_type = constants.Analysis.AnalysisIDM.FftThroughFocusMtf

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    # Apply settings
    analysis.Settings.SampleSize = getattr(constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(sampling))
    analysis.Settings.DeltaFocus = deltafocus
    analysis.Settings.Frequency = frequency
    analysis.Settings.NumberOfSteps = numberofsteps
    analysis.set_wavelength(wavelength)
    analysis.set_field(field)
    analysis.Settings.Type = constants.process_constant(constants.Analysis.Settings.Mtf.MtfTypes, mtftype)
    analysis.Settings.UsePolarization = use_polarization
    analysis.Settings.UseDashes = use_dashes

    # Correct an API bug in setting API type for OpticStudio version <21.2
    _correct_fft_through_focus_mtftype_api_bug(oss, analysis, mtftype)

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["SampleSize"] = str(analysis.Settings.SampleSize)
    settings.loc["DeltaFocus"] = analysis.Settings.DeltaFocus
    settings.loc["Frequency"] = analysis.Settings.Frequency
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["Field"] = analysis.get_field()
    settings.loc["Type"] = str(analysis.Settings.Type)
    settings.loc["UsePolarization"] = analysis.Settings.UsePolarization
    settings.loc["UseDashes"] = analysis.Settings.UseDashes

    # Get data and unpack
    data = []
    for ii in range(analysis.Results.NumberOfDataSeries):
        data.append(utils.zputils.unpack_dataseries(analysis.Results.DataSeries[ii]))

    if not len(data):
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


def fft_through_focus_mtf_fromcfg(
    oss: OpticStudioSystem, cfgfile: str, oncomplete: OnComplete | str = OnComplete.Close
):
    """Wrapper around the OpticStudio FFT Through Focus MTF using a configuration file.

    For an in depth explanation of the parameters, see the Zemax OpticStudio user manual

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    cfgfile: str
        Full filepath (including extension) to a configuration file.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        An FftThroughFocusMtf analysis result. Next to the standard data, the cfgfile will be added under 'UsedCfgFile'
    """
    analysis_type = constants.Analysis.AnalysisIDM.FftThroughFocusMtf

    # Create analysis
    analysis = new_analysis(oss, analysis_type)

    # Apply settings
    analysis.Settings.LoadFrom(cfgfile)

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)
    settings.drop(settings.index, inplace=True)

    settings.loc["SampleSize"] = str(analysis.Settings.SampleSize)
    settings.loc["DeltaFocus"] = analysis.Settings.DeltaFocus
    settings.loc["Frequency"] = analysis.Settings.Frequency
    settings.loc["NumberOfSteps"] = analysis.Settings.NumberOfSteps
    settings.loc["Wavelength"] = analysis.Settings.Wavelength.GetWavelengthNumber()  # Todo Evaluate
    settings.loc["Field"] = analysis.Settings.Field.GetFieldNumber()  # Todo Evaluate
    settings.loc["Type"] = str(analysis.Settings.Type)
    settings.loc["UsePolarization"] = analysis.Settings.UsePolarization
    settings.loc["UseDashes"] = analysis.Settings.UseDashes

    # Get data and unpack
    data = []
    for ii in range(analysis.Results.NumberOfDataSeries):
        data.append(utils.zputils.unpack_dataseries(analysis.Results.DataSeries[ii]))

    if not len(data):
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
        UsedCfgFile=cfgfile,
    )

    return analysis.complete(oncomplete, result)
