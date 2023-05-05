"""Zemax OpticStudio analyses from the PSF category."""

from __future__ import annotations

import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants


def huygens_psf(
    oss,
    pupil_sampling: str | int = "32x32",
    image_sampling: str | int = "32x32",
    image_delta: float = 0,
    rotation: float = 0,
    wavelength: str | int = "All",
    field: str | int = 1,
    psftype: constants.Analysis.Settings.HuygensPsfTypes | str = "Linear",
    show_as: constants.Analysis.HuygensShowAsTypes | str = "Surface",
    use_polarization: bool = False,
    use_centroid: bool = False,
    normalize: bool = False,
    oncomplete: OnComplete | str = OnComplete.Close,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Huygens PSF.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    pupil_sampling: str | int
        The pupil sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
        integer.
    image_sampling: str | int
        The image sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
        integer.
    image_delta: float | int
        The image delta
    rotation: int
        The rotation, should be one of [0, 90, 180, 270].
    wavelength: str | int
        The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number.
        Defaults to 'All'.
    field: str | int
        The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 1.
    psftype: str | int
        The PSF type (e.g. 'Linear') that is calculated. Defaults to 'Linear'.
    show_as: str | int
        Defines how the data is showed within OpticStudio. Defaults to 'Surface'
    use_polarization: bool
        Defines if polarization is used. Defaults to False.
    use_centroid: bool
        Defines if centroid is used. Defaults to False.
    normalize: bool
        Defines if normalization is used. Defaults to False.
    oncomplete: OnComplete | str
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
    analysistype = constants.Analysis.AnalysisIDM.HuygensPsf

    # Create analysis
    analysis = new_analysis(oss, analysistype)

    # Apply settings
    analysis.Settings.PupilSampleSize = getattr(
        constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(pupil_sampling)
    )
    analysis.Settings.ImageSampleSize = getattr(
        constants.Analysis.SampleSizes, utils.zputils.standardize_sampling(image_sampling)
    )
    analysis.Settings.ImageDelta = image_delta
    analysis.Settings.Rotation = getattr(constants.Analysis.Settings.Rotations, f"Rotate_{rotation}")
    analysis.set_wavelength(wavelength)
    analysis.set_field(field)
    analysis.Settings.Type = constants.process_constant(constants.Analysis.Settings.HuygensPsfTypes, psftype)
    analysis.Settings.ShowAsType = constants.process_constant(constants.Analysis.HuygensShowAsTypes, show_as)
    analysis.Settings.UsePolarization = use_polarization
    analysis.Settings.UseCentroid = use_centroid
    analysis.Settings.Normalize = normalize

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Get settings
    settings = pd.Series(name="Settings", dtype=object)

    settings.loc["PupilSampleSize"] = str(analysis.Settings.PupilSampleSize)
    settings.loc["ImageSampleSize"] = str(analysis.Settings.ImageSampleSize)
    settings.loc["ImageDelta"] = analysis.Settings.ImageDelta
    settings.loc["Rotation"] = int(str(analysis.Settings.Rotation).split("_")[1])
    settings.loc["Wavelength"] = analysis.get_wavelength()
    settings.loc["Field"] = analysis.get_field()
    settings.loc["Type"] = str(analysis.Settings.Type)
    settings.loc["ShowAsType"] = str(analysis.Settings.ShowAsType)
    settings.loc["UsePolarization"] = analysis.Settings.UsePolarization
    settings.loc["UseCentroid"] = analysis.Settings.UseCentroid
    settings.loc["Normalize"] = analysis.Settings.Normalize

    # Get data
    if analysis.Results.NumberOfDataGrids <= 0:
        data = None
    elif analysis.Results.NumberOfDataGrids == 1:
        data = utils.zputils.unpack_datagrid(analysis.Results.DataGrids[0])
    else:
        data = AttrDict()
        for ii in range(analysis.Results.NumberOfDataGrids):
            desc = analysis.Results.DataGrids[ii].Description
            key = desc if desc != "" else str(ii)
            data[key] = utils.zputils.unpack_datagrid(analysis.Results.DataGrids[ii])

    result = AnalysisResult(
        analysistype=str(analysistype),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
    )

    return analysis.complete(oncomplete, result)
