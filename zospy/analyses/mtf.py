import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult
from zospy.api import constants


def fft_through_focus_mtf(oss, sampling='64x64', deltafocus=0.1, frequency=0,
                          numberofsteps=5, wavelength='All', field='All', mtftype='Modulation',
                          use_polarization=False, use_dashes=False, oncomplete='Close'):
    """Wrapper around the OpticStudio FFT Through Focus MTF.

    For an in depth explanation of the parameters, see the Zemax OpticStudio user manual

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str or int
        The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants integer.
    deltafocus: float
        The delta focus, defaults to 0.1
    frequency: float
        The frequency. Defaults to 0.
    numberofsteps: int
        The number of steps. Defaults to 5.
    wavelength: str or int
        The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
    field: str or int
        The field to use in the MTF. Either 'All' or an integer specifying the field number.
    mtftype: str or int
        The MTF type (e.g. 'Modulation') that is calculated.
    use_polarization: bool
        Use polarization. Defaults to False.
    use_dashes: bool
        Use dashes. Defaults to False.
    oncomplete: str
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
    analysistype = 'FftThroughFocusMtf'

    # Create analysis
    analysis = oss.Analyses.New_Analysis_SettingsFirst(constants.Analysis.AnalysisIDM.loc[analysistype])

    # Apply settings
    analysis.Settings.SampleSize = utils.zputils.proc_constant(constants.Analysis.SampleSizes,
                                                               utils.zputils.standardize_sampling(sampling))
    analysis.Settings.DeltaFocus = deltafocus
    analysis.Settings.Frequency = frequency
    analysis.Settings.NumberOfSteps = numberofsteps
    utils.zputils.analysis_set_wavelength(analysis, wavelength)
    utils.zputils.analysis_set_field(analysis, field)
    analysis.Settings.Type = utils.zputils.proc_constant(constants.Analysis.Settings.Mtf.MtfTypes, mtftype)
    analysis.Settings.UsePolarization = use_polarization
    analysis.Settings.UseDashes = use_dashes

    # Calculate
    analysis.ApplyAndWaitForCompletion()
    
    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis)

    # Get settings
    settings = pd.Series(name='Settings')

    settings.loc['SampleSize'] = utils.zputils.series_index_by_value(constants.Analysis.SampleSizes,
                                                                     analysis.Settings.SampleSize)
    settings.loc['DeltaFocus'] = analysis.Settings.DeltaFocus
    settings.loc['Frequency'] = analysis.Settings.Frequency
    settings.loc['Wavelength'] = utils.zputils.analysis_get_wavelength(analysis)
    settings.loc['Field'] = utils.zputils.analysis_get_field(analysis)
    settings.loc['Type'] = utils.zputils.series_index_by_value(constants.Analysis.Settings.Mtf.MtfTypes,
                                                               analysis.Settings.Type)
    settings.loc['UsePolarization'] = analysis.Settings.UsePolarization
    settings.loc['UseDashes'] = analysis.Settings.UseDashes
    
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
    
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages)

    if oncomplete == 'Close':  # Close if needed
        analysis.Close()
    elif oncomplete == 'Release':  # Keep the analysis open within OpticStudio but release it
        analysis.Release()
    elif oncomplete == 'Sustain':  # Add the analysis to the return
        ret.Analysis = analysis
    else:
        raise ValueError('oncomplete should be one of "Close", "Release", "Sustain"')

    return ret


def fft_through_focus_mtf_fromcfg(oss, cfgfile, oncomplete='Close'):
    """Wrapper around the OpticStudio FFT Through Focus MTF using a configuration file.

    For an in depth explanation of the parameters, see the Zemax OpticStudio user manual

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    cfgfile: str
        Full filepath (including extension) to a configuration file.
    oncomplete: str
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
    analysistype = 'FftThroughFocusMtf'

    # Create analysis
    analysis = oss.Analyses.New_Analysis_SettingsFirst(constants.Analysis.AnalysisIDM.loc[analysistype])

    # Apply settings
    analysis.Settings.LoadFrom(cfgfile)

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis)

    # Get settings
    settings = pd.Series()
    settings.drop(settings.index, inplace=True)

    settings.loc['SampleSize'] = constants.get_constantname_by_value(
        constants.Analysis.SampleSizes, analysis.Settings.SampleSize)
    settings.loc['DeltaFocus'] = analysis.Settings.DeltaFocus
    settings.loc['Frequency'] = analysis.Settings.Frequency
    settings.loc['NumberOfSteps'] = analysis.Settings.NumberOfSteps
    settings.loc['Wavelength'] = analysis.Settings.Wavelength.GetWavelengthNumber()  # Todo Evaluate
    settings.loc['Field'] = analysis.Settings.Field.GetFieldNumber()  # Todo Evaluate
    settings.loc['Type'] = constants.get_constantname_by_value(
        constants.Analysis.Settings.Mtf.MtfTypes, analysis.Settings.Type)
    settings.loc['UsePolarization'] = analysis.Settings.UsePolarization
    settings.loc['UseDashes'] = analysis.Settings.UseDashes

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

    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         UsedCfgFile=cfgfile)

    # Process oncomplete
    if oncomplete == 'Close':  # Close if needed
        analysis.Close()
    elif oncomplete == 'Release':  # Keep the analysis open within OpticStudio but release it
        analysis.Release()
    elif oncomplete == 'Sustain':  # Add the analysis to the return
        ret.Analysis = analysis
    else:
        raise ValueError('oncomplete should be one of "Close", "Release", "Sustain"')

    return ret
