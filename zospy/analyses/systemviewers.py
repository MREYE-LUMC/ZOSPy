"""Zemax OpticStudio System Viewers."""

from __future__ import annotations

from zospy.analyses.base import AnalysisResult, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem


def cross_section(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Cross-Section viewer.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A Cross-Section analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.Draw2D

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def viewer_3d(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio 3D Viewer.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A Viewer 3D analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.Draw3D

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def shaded_model(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Shaded Model Viewer.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A Shaded Model analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.ShadedModel

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def nsc_3d_layout(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio NSC 3D Layout viewer.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be non-sequential.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A NSC 3D Layout analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.NSC3DLayout

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)


def nsc_shaded_model(
    oss: OpticStudioSystem,
    oncomplete: OnComplete | str = OnComplete.Release,
) -> AnalysisResult:
    """Wrapper around the OpticStudio NSC Shaded Model Viewer.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be non-sequential.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to
        'Release'.

    Returns
    -------
    AnalysisResult
        A NSC Shaded Model analysis result. As the viewers do not return data, the AnalysisResult can mainly be used to
        further control the analysis when oncomplete is set to `Sustain`.
    """
    analysis_type = constants.Analysis.AnalysisIDM.NSCShadedModel

    analysis = new_analysis(oss, analysis_type, settings_first=False)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=None,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)
