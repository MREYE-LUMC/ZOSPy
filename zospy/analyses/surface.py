import pandas as pd

from zospy.analyses.base import AnalysisResult, AttrDict
from zospy.api import constants
from zospy.utils import zputils


def curvature(oss, sampling='65x65', data='TangentialCurvature', remove='None', surface=1, showas='Contour',
              offaxiscoordinates=False, contourformat='', bfs_criterion='MinimumVolume', bfs_reversedirection=False,
              oncomplete='Close'):
    """
    
    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str or int
        The size of the used grid, either string (e.g. '65x65') or int. The integer will be treated as if obtained from
        zospy.constants.Analysis.SampleSizes_Pow2Plus1_X. Defaults to '65x65'.
    data: str or int
        The used data type. Should be one of ['TangentialCurvature', 'SagitalCurvature', 'X_Curvature', 'Y_Curvature'] 
        or int. The integer will be treated as if obtained from zospy.constants.Analysis.SurfaceCurvatureData. Defaults 
        to 'TangentialCurvature'.
    remove: str or int
        Defines whether a reference volume is removed or not. Should be one of ['None', 'BaseROC', 'BestFitSphere'] or 
        int. The integer will be treated as if obtained from zospy.constants.Analysis.RemoveOptions. Defaults 
        to 'None'.
    surface: int
        The surface that is te be analyzed. defaults to 1.
    showas: str or int
        Defines how the data is displayed in OpticStudio. Should be one of ['Surface', 'Contour', 'GreyScale', 
        'InverseGreyScale', 'FalseColor', 'InverseFalseColor'] or int. The integer will be treated as if obtained from 
        zospyconstants.Analysis.ShowAs. Defaults to 'Contour'.
    offaxiscoordinates: bool
        Defines whether apertures defined in the Surface Properties of the surface are considered or not. Defaults to 
        False.

    contourformat: str
        The contour format. Only usable when showas == 'Contour'. Defaults to ''.
    
    bfs_criterion: str or int
        The criterion for BFS removal. Only usable when remove == 'BestFitSphere'. Should be one of ['MinimumVolume',
        'MinimumRMS', 'MinimumRMSWithOffset'] or int. The integer will be treated as if obtained from
        constants.Analysis.BestFitSphereOptions. Defaults to 'MinimumVolume'.
    bfs_reversedirection: bool
        Defines if the sign of the BFS radius should be reversed or not. Only usable when remove == 'BestFitSphere'
        and bfs_criterion == 'MinimumVolume'. Defaults to False.

    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.

    Returns
    -------
    AnalysisResult
        A SurfaceCurvature analysis result
    """
    analysistype = 'SurfaceCurvature'

    analysis = oss.Analyses.New_Analysis_SettingsFirst(constants.Analysis.AnalysisIDM.loc[analysistype])

    # Apply settings
    analysis.Settings.Sampling = zputils.proc_constant(constants.Analysis.SampleSizes_Pow2Plus1_X,
                                                       zputils.standardize_sampling(sampling))
    analysis.Settings.Data = zputils.proc_constant(constants.Analysis.SurfaceCurvatureData, data)
    analysis.Settings.RemoveOption = zputils.proc_constant(constants.Analysis.RemoveOptions, remove)
    zputils.analysis_set_surface(analysis, surface)
    analysis.Settings.ShowAs = zputils.proc_constant(constants.Analysis.ShowAs, showas)

    analysis.Settings.ConsiderOffAxisAperture = offaxiscoordinates
    if analysis.Settings.ShowAs == constants.Analysis.ShowAs.Contour:  # ContourFormat becomes available
        analysis.Settings.ContourFormat = contourformat

    if analysis.Settings.RemoveOption == constants.Analysis.RemoveOptions.BestFitSphere:  # Add Best fit sphere options
        analysis.Settings.BestFitSphereOptions = zputils.proc_constant(constants.Analysis.BestFitSphereOptions,
                                                                       bfs_criterion)

        if analysis.Settings.BestFitSphereOptions == constants.Analysis.BestFitSphereOptions.MinimumVolume:
            # Reversed direction becomes available
            analysis.Settings.ReverseDirection = bfs_reversedirection

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = zputils.analysis_get_headerdata(analysis)
    metadata = zputils.analysis_get_metadata(analysis)
    messages = zputils.analysis_get_messages(analysis)

    # Get settings
    settings = pd.Series(name='Settings')

    settings.loc['Sampling'] = constants.get_constantname_by_value(constants.Analysis.SampleSizes_Pow2Plus1_X,
                                                                   analysis.Settings.Sampling)
    settings.loc['Data'] = constants.get_constantname_by_value(constants.Analysis.SurfaceCurvatureData,
                                                               analysis.Settings.Data)
    settings.loc['RemoveOption'] = constants.get_constantname_by_value(constants.Analysis.RemoveOptions,
                                                                       analysis.Settings.RemoveOption)
    settings.loc['Surface'] = analysis.Settings.Surface.GetSurfaceNumber()
    settings.loc['ShowAs'] = constants.get_constantname_by_value(constants.Analysis.ShowAs,
                                                                 analysis.Settings.ShowAs)
    settings.loc['ConsiderOffAxisAperture'] = analysis.Settings.ConsiderOffAxisAperture

    if analysis.Settings.ShowAs == constants.Analysis.ShowAs.Contour:  # ContourFormat is available
        settings.loc['Contourformat'] = analysis.Settings.ContourFormat

    if analysis.Settings.RemoveOption == constants.Analysis.RemoveOptions.BestFitSphere:  # Add Best fit sphere options
        settings.loc['BestFitSphereOptions'] = \
            constants.get_constantname_by_value(constants.Analysis.BestFitSphereOptions,
                                                analysis.Settings.BestFitSphereOptions)
        if analysis.Settings.BestFitSphereOptions == constants.Analysis.BestFitSphereOptions.MinimumVolume:
            # Reversed direction is available
            settings.loc['ReverseDirection'] = analysis.Settings.ReverseDirection

    # Get data
    if analysis.Results.NumberOfDataGrids <= 0:
        data = None
    elif analysis.Results.NumberOfDataGrids == 1:
        data = zputils.unpack_datagrid(analysis.Results.DataGrids[0])
    else:
        data = AttrDict()
        for ii in range(analysis.Results.NumberOfDataGrids):
            desc = analysis.Results.DataGrids[ii].Description
            key = desc if desc != '' else str(ii)
            data[key] = zputils.unpack_datagrid(analysis.Results.DataGrids[ii])

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
