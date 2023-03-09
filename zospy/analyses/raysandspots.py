import os
import re

from tempfile import mkstemp
from io import StringIO

import numpy as np
import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict
from zospy.api import constants
import zospy.api.config as _config

def _structure_ray_trace_data_result(line_list):
    """Structures the result of a ray trace data report.

    Parameters
    ----------
    line_list: list of str
        The line list obtained by reading in the results

    Returns
    -------
    dict
        The results structured in a dictionary
    """
    # Create output dict
    res = AttrDict()

    # Add header
    hdr = line_list[0].strip().replace('\ufeff', '')
    res['Header'] = hdr

    # Register landmarks
    landmarks = ['Real Ray Trace Data',
                 'Paraxial Ray Trace Data',
                 'Trace of Paraxial Y marginal, U marginal, Y chief, U chief only']
    comp = re.compile(rf'^({"|".join(landmarks)})', re.IGNORECASE)
    inds = {comp.match(line).group().lower(): {'rnum': rnum, 'name': comp.match(line).group()}
            for rnum, line in enumerate(line_list) if comp.match(line)}

    order_of_appearance = [item[0] for item in sorted(inds.items(), key=lambda x: x[1]['rnum'])]

    # Add general lens data
    for target in inds.keys():
        section_start = inds[target]['rnum'] + 1  # + 1 to ignore section title

        # Get endpoint
        if order_of_appearance.index(target) == len(inds) - 1:
            section_end = len(line_list)
        else:
            target2 = order_of_appearance[order_of_appearance.index(target) + 1]
            section_end = inds[target2]['rnum']

        # Read as dataframe
        df = pd.read_csv(StringIO(''.join(line_list[section_start:section_end]).replace(' ','')),
                          delimiter='\t', decimal=_config.DECIMAL)

        # Recover case of target
        keyname = inds[target]['name'].replace(' ','')

        # Add to result dictionary
        res[keyname] = df

    return res


def single_ray_trace(oss, hx=0, hy=0, px=0, py=1, wavelength=1, field=0, rttype='DirectionCosines',
                     global_coordinates=False, oncomplete='Close', txtoutfile=None):
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
    rttype: str or int
        The Ray Trace type (e.g. 'DirectionCosines') that is calculated. Defaults to 'DirectionCosines'.
    wavelength: int
        The wavelength number that is to be used. Must be an integer specifying the wavelength number. 
        Defaults to 1.
    field: int
        The field number that is to be used. Must be an integer specifying the field number. "Arbitrary" is 0. Defaults 
        to 0.
    global_coordinates: bool
        Defines if global coordinates are used. Defaults to False.
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    txtoutfile: str or None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A Single Ray Trace result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', and the txtoutfile under 'TxtOutFile'.
    """

    analysistype = 'RayTrace'

    # Temp file
    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix='.txt', prefix='zospy_')
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith('.txt'):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False


    analysis = oss.Analyses.New_Analysis_SettingsFirst(constants.Analysis.AnalysisIDM.loc[analysistype])

    # Settings for ray trace
    analysis.Settings.Hx = hx
    analysis.Settings.Hy = hy
    analysis.Settings.Px = px
    analysis.Settings.Py = py
    utils.zputils.analysis_set_wavelength(analysis, wavelength)
    utils.zputils.analysis_set_field(analysis, field)
    analysis.Settings.Type = utils.zputils.proc_constant(constants.Analysis.Settings.Aberrations.RayTraceType, rttype)
    analysis.Settings.UseGlobal = global_coordinates
    
    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, 'r', encoding='utf-16-le')]
    data = _structure_ray_trace_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis)

    # Get settings
    settings = pd.Series(name='Settings')

    settings.loc['Hx'] = analysis.Settings.Hx
    settings.loc['Hy'] = analysis.Settings.Hy
    settings.loc['Px'] = analysis.Settings.Px
    settings.loc['Py'] = analysis.Settings.Py
    settings.loc['Wavelength'] = utils.zputils.analysis_get_wavelength(analysis)
    settings.loc['Field'] = utils.zputils.analysis_get_field(analysis)
    settings.loc['Type'] = utils.zputils.series_index_by_value(constants.Analysis.Settings.Aberrations.RayTraceType,
                                                               analysis.Settings.Type)
    settings.loc['GlobalCoordinates'] = analysis.Settings.UseGlobal

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         RawTextData=line_list, TxtOutFile=txtoutfile)  # Set additional params

    # cleanup if needed
    if cleantxt:
        os.remove(txtoutfile)

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



def ray_fan(oss, plot_scale=0, number_of_rays=20, field='All', wavelength='All', tangential='Aberration_Y',
            sagittal='Aberration_X', surface='Image', use_dashes=False, vignetted_pupil=True, check_apertures=True,
            oncomplete='Close'):
    """Wrapper around the OpticStudio Ray Fan Analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    plot_scale: int or float
        Sets the maximum vertical scale for the plots. When 0, automatic scaling is used. Defaults to 0.
    number_of_rays: int
        This is the number of rays traced on each side of the origin of the plot.
    field: str or int
        The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 'All'.
    wavelength: str or int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number. 
        Defaults to 'All'.
    tangential: str or int
        The aberration component that is plotted for the tangential fan. Accepts sting ('Aberration_Y' or
        'Aberration_X') or int (respectively 0 and 1). Defaults to 'Aberration_Y'.
    sagittal: str or int
        The aberration component that is plotted for the sagittal fan. Accepts sting ('Aberration_X' or
        'Aberration_Y') or int (respectively 0 and 1). Defaults to 'Aberration_X'.
    surface: str or int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    use_dashes: bool
        Defines whether solid lines or dashes are used to differentiate curves. Defaults to False.
    vignetted_pupil: bool
        Defines whether the pupil axis is scaled to the unvignetted pupil or not. Defaults to True.
    check_apertures: bool
        Defines whether only rays that pass all surface apertures are drawn or not. Defaults to True.
    oncomplete: str
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
    analysistype = 'RayFan'
    analysis = oss.Analyses.New_Analysis_SettingsFirst(constants.Analysis.AnalysisIDM.loc[analysistype])

    # Settings for ray fan
    utils.zputils.analysis_set_field(analysis, field)
    utils.zputils.analysis_set_surface(analysis, surface)
    utils.zputils.analysis_set_wavelength(analysis, wavelength)
    analysis.Settings.NumberOfRays = number_of_rays
    analysis.Settings.PlotScale = plot_scale
    analysis.Settings.CheckApertures = check_apertures
    analysis.Settings.VignettedPupil = vignetted_pupil
    analysis.Settings.UseDashes = use_dashes
    analysis.Settings.Sagittal = \
        utils.zputils.proc_constant(constants.Analysis.Settings.Fans.SagittalAberrationComponent, sagittal)
    analysis.Settings.Tangential = \
        utils.zputils.proc_constant(constants.Analysis.Settings.Fans.TangentialAberrationComponent, tangential)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Parse results
    results = analysis.GetResults()
    data = AttrDict()
    data['Header'] = 'Ray Fan Data'
    for ii in range(results.DataSeries.Length):
        # get raw .NET data into numpy array
        ds = results.GetDataSeries(ii)
        xRaw = np.asarray(tuple(ds.XData.Data))
        yRaw = np.asarray(tuple(ds.YData.Data))

        # Reshape data
        x = xRaw
        y = yRaw.reshape(ds.YData.Data.GetLength(0), ds.YData.Data.GetLength(1))

        # Make data frame
        df = {ds.XLabel:x}
        for jj, label in enumerate(ds.SeriesLabels):
            df[label] = y[:,jj]
        df = pd.DataFrame(data=df)
        
        # Add data to dictionary
        data[ds.Description] = df

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis)

    # Get settings
    settings = pd.Series(name='Settings')
    settings.loc['Field'] = utils.zputils.analysis_get_field(analysis)
    settings.loc['Surface'] = analysis.Settings.Surface.GetSurfaceNumber()
    settings.loc['Wavelength'] = utils.zputils.analysis_get_wavelength(analysis)
    settings.loc['NumberOfRays'] = analysis.Settings.NumberOfRays
    settings.loc['PlotScale'] = analysis.Settings.PlotScale
    settings.loc['CheckApertures'] = analysis.Settings.CheckApertures
    settings.loc['VignettedPupil'] = analysis.Settings.VignettedPupil
    settings.loc['UseDashes'] = analysis.Settings.UseDashes
    settings.loc['Sagittal'] = \
        utils.zputils.series_index_by_value(constants.Analysis.Settings.Fans.SagittalAberrationComponent,
                                            analysis.Settings.Sagittal)
    settings.loc['Tangential'] = \
        utils.zputils.series_index_by_value(constants.Analysis.Settings.Fans.TangentialAberrationComponent,
                                            analysis.Settings.Tangential)

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages)  # Set additional params

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
