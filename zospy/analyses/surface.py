"""Zemax OpticStudio analyses from the Surface category."""

from __future__ import annotations

import pandas as pd

from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.utils import zputils
from zospy.zpcore import OpticStudioSystem


def curvature(
    oss: OpticStudioSystem,
    sampling: str = "65x65",
    data: constants.Analysis.SurfaceCurvatureData | str = "TangentialCurvature",
    remove: constants.Analysis.RemoveOptions | str | None = "None_",
    surface: int = 1,
    showas: constants.Analysis.ShowAs | str = "Contour",
    offaxiscoordinates: bool = False,
    contourformat: str = "",
    bfs_criterion: constants.Analysis.BestFitSphereOptions | str = "MinimumVolume",
    bfs_reversedirection: bool = False,
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Curvature analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str | int
        The size of the used grid, either string (e.g. '65x65') or int. The integer will be treated as if obtained from
        zospy.constants.Analysis.SampleSizes_Pow2Plus1_X. Defaults to '65x65'.
    data: str
        The used data type. Should be one of ['TangentialCurvature', 'SagittalCurvature', 'X_Curvature', 'Y_Curvature']
        or int. The integer will be treated as if obtained from zospy.constants.Analysis.SurfaceCurvatureData. Defaults
        to 'TangentialCurvature'.
    remove: str | int
        Defines whether a reference volume is removed or not. Should be one of ['None', 'BaseROC', 'BestFitSphere'] or
        int. The integer will be treated as if obtained from zospy.constants.Analysis.RemoveOptions. Defaults
        to 'None'.
    surface: int
        The surface that is te be analyzed. defaults to 1.
    showas: str | int
        Defines how the data is displayed in OpticStudio. Should be one of ['Surface', 'Contour', 'GreyScale',
        'InverseGreyScale', 'FalseColor', 'InverseFalseColor'] or int. The integer will be treated as if obtained from
        zospyconstants.Analysis.ShowAs. Defaults to 'Contour'.
    offaxiscoordinates: bool
        Defines whether apertures defined in the Surface Properties of the surface are considered or not. Defaults to
        False.
    contourformat: str
        The contour format. Only usable when showas == 'Contour'. Defaults to ''.
    bfs_criterion: str | int
        The criterion for BFS removal. Only usable when remove == 'BestFitSphere'. Should be one of ['MinimumVolume',
        'MinimumRMS', 'MinimumRMSWithOffset'] or int. The integer will be treated as if obtained from
        constants.Analysis.BestFitSphereOptions. Defaults to 'MinimumVolume'.
    bfs_reversedirection: bool
        Defines if the sign of the BFS radius should be reversed or not. Only usable when remove == 'BestFitSphere'
        and bfs_criterion == 'MinimumVolume'. Defaults to False.
    oncomplete: OnComplete | str
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
    analysis_type = constants.Analysis.AnalysisIDM.SurfaceCurvature

    analysis = new_analysis(oss, analysis_type)

    # Apply settings
    analysis.Settings.Sampling = getattr(
        constants.Analysis.SampleSizes_Pow2Plus1_X, zputils.standardize_sampling(sampling)
    )
    analysis.Settings.Data = constants.process_constant(constants.Analysis.SurfaceCurvatureData, data)
    analysis.Settings.RemoveOption = constants.process_constant(constants.Analysis.RemoveOptions, remove)
    analysis.set_surface(surface)
    analysis.Settings.ShowAs = constants.process_constant(constants.Analysis.ShowAs, showas)

    analysis.Settings.ConsiderOffAxisAperture = offaxiscoordinates
    if analysis.Settings.ShowAs == constants.Analysis.ShowAs.Contour:  # ContourFormat becomes available
        analysis.Settings.ContourFormat = contourformat

    if analysis.Settings.RemoveOption == constants.Analysis.RemoveOptions.BestFitSphere:  # Add Best fit sphere options
        analysis.Settings.BestFitSphereOption = constants.process_constant(
            constants.Analysis.BestFitSphereOptions, bfs_criterion
        )

        if analysis.Settings.BestFitSphereOption == constants.Analysis.BestFitSphereOptions.MinimumVolume:
            # Reversed direction becomes available
            analysis.Settings.ReverseDirection = bfs_reversedirection

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["Sampling"] = str(analysis.Settings.Sampling)
    settings.loc["Data"] = str(analysis.Settings.Data)
    settings.loc["RemoveOption"] = str(analysis.Settings.RemoveOption)
    settings.loc["Surface"] = analysis.Settings.Surface.GetSurfaceNumber()
    settings.loc["ShowAs"] = str(analysis.Settings.ShowAs)
    settings.loc["ConsiderOffAxisAperture"] = analysis.Settings.ConsiderOffAxisAperture

    if analysis.Settings.ShowAs == constants.Analysis.ShowAs.Contour:  # ContourFormat is available
        settings.loc["Contourformat"] = str(analysis.Settings.ContourFormat)

    if analysis.Settings.RemoveOption == constants.Analysis.RemoveOptions.BestFitSphere:  # Add Best fit sphere options
        settings.loc["BestFitSphereOptions"] = str(analysis.Settings.BestFitSphereOption)
        if analysis.Settings.BestFitSphereOption == constants.Analysis.BestFitSphereOptions.MinimumVolume:
            # Reversed direction is available
            settings.loc["ReverseDirection"] = analysis.Settings.ReverseDirection

    # Get data
    if analysis.Results.NumberOfDataGrids <= 0:
        data = None
    elif analysis.Results.NumberOfDataGrids == 1:
        data = zputils.unpack_datagrid(analysis.Results.DataGrids[0])
    else:
        data = AttrDict()
        for ii in range(analysis.Results.NumberOfDataGrids):
            desc = analysis.Results.DataGrids[ii].Description
            key = desc if desc != "" else str(ii)
            data[key] = zputils.unpack_datagrid(analysis.Results.DataGrids[ii])

    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)
