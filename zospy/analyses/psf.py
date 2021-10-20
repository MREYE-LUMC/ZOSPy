import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict


def huygens_psf(oss, pupil_sampling='32x32', image_sampling='32x32', image_delta=0, rotation=0, wavelength='All',
                field=1, psftype='Linear', show_as='Surface', use_polarization=False, use_centroid=False,
                normalize=False, oncomplete='Close'):
    """Wrapper around the OpticStudio Huygens PSF
    
    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    pupil_sampling: str or int
        The pupil sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants 
        integer.
    image_sampling: str or int
        The image sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants 
        integer.
    image_delta: float or int
        The image delta
    rotation: int
        The rotation, should be one off [0, 90, 180, 270].
    wavelength: str or int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number. 
        Defaults to 'All'.
    field: str or int
        The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 1. 
    psftype: str or int
        The PSF type (e.g. 'Linear') that is calculated. Defaults to 'Linear'.
    show_as: str or int
        Defines how the data is showed within OpticStudio. Defaults to 'Surface'
    use_polarization: bool
        Defines if polarization is used. Defaults to False.
    use_centroid: bool
        Defines if centroid is used. Defaults to False.
    normalize: bool
        Defines if normalization is used. Defaults to False.
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A HuygensPsf analysis result
    """  # ToDo check if default for filed is correct

    analysistype = 'HuygensPsf'

    # Create analysis
    analysis = oss.System.Analyses.New_Analysis_SettingsFirst(oss.Constants.Analysis.AnalysisIDM.loc[analysistype])

    # Apply settings
    analysis.Settings.PupilSampleSize = utils.zputils.proc_constant(oss.Constants.Analysis.SampleSizes,
                                                                    utils.zputils.standardize_sampling(pupil_sampling))
    analysis.Settings.ImageSampleSize = utils.zputils.proc_constant(oss.Constants.Analysis.SampleSizes,
                                                                    utils.zputils.standardize_sampling(image_sampling))
    analysis.Settings.ImageDelta = image_delta
    analysis.Settings.Rotation = oss.Constants.Analysis.Settings.Rotations.loc[f'Rotate_{rotation}']
    utils.zputils.analysis_set_wavelength(analysis, wavelength)
    utils.zputils.analysis_set_field(analysis, field)
    analysis.Settings.Type = oss.Constants.Analysis.Settings.HuygensPsfTypes.loc[psftype]
    analysis.Settings.ShowAsType = oss.Constants.Analysis.HuygensShowAsTypes.loc[show_as]
    analysis.Settings.UsePolarization = use_polarization
    analysis.Settings.UseCentroid = use_centroid
    analysis.Settings.Normalize = normalize

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis, constants=oss.Constants)

    # Get settings
    settings = pd.Series(name='Settings')

    settings.loc['PupilSampleSize'] = utils.zputils.series_index_by_value(oss.Constants.Analysis.SampleSizes,
                                                                          analysis.Settings.PupilSampleSize)
    settings.loc['ImageSampleSize'] = utils.zputils.series_index_by_value(oss.Constants.Analysis.SampleSizes,
                                                                          analysis.Settings.ImageSampleSize)
    settings.loc['ImageDelta'] = analysis.Settings.ImageDelta
    settings.loc['Rotation'] = int(utils.zputils.series_index_by_value(oss.Constants.Analysis.Settings.Rotations,
                                                                       analysis.Settings.Rotation).split('_')[1])
    settings.loc['Wavelength'] = utils.zputils.analysis_get_wavelength(analysis)
    settings.loc['Field'] = utils.zputils.analysis_get_field(analysis)
    settings.loc['Type'] = utils.zputils.series_index_by_value(oss.Constants.Analysis.Settings.HuygensPsfTypes,
                                                               analysis.Settings.Type)
    settings.loc['ShowAsType'] = utils.zputils.series_index_by_value(oss.Constants.Analysis.HuygensShowAsTypes,
                                                                     analysis.Settings.Type)
    settings.loc['UsePolarization'] = analysis.Settings.UsePolarization
    settings.loc['UseCentroid'] = analysis.Settings.UseCentroid
    settings.loc['Normalize'] = analysis.Settings.Normalize

    # Get data
    if analysis.Results.NumberOfDataGrids <= 0:
        data = None
    elif analysis.Results.NumberOfDataGrids == 1:
        data = utils.zputils.unpack_datagrid(analysis.Results.DataGrids[0])
    else:
        data = AttrDict()
        for ii in range(analysis.Results.NumberOfDataGrids):
            desc = analysis.Results.DataGrids[ii].Description
            key = desc if desc != '' else str(ii)
            data[key] = utils.zputils.unpack_datagrid(analysis.Results.DataGrids[ii])

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
