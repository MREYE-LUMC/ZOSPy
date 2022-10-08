import os
import re
from tempfile import mkstemp

import numpy as np
import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict
from zospy.api import constants


def _structure_zernike_standard_coefficients_result(line_list):
    """Structures the result of a zernike standard coefficients analysis.

    Parameters
    ----------
    line_list: list of str
        The line list obtained by reading in the results

    Returns
    -------
    (pd.DataFrame, pd.DataFrame)
        Two dataframes, respectively the general results and the coefficients
    """
    zlinepat = re.compile(r'^Z\s+\d+')
    valuepat_start = re.compile(r'^((-)?\d+\.\d+)')
    valuepat_any = re.compile(r'((-)?\d+(\.\d+)?)')

    zernike_lines = [line for line in line_list if (zlinepat.search(line) is not None)]

    general_lines = [line for line in line_list if line not in zernike_lines]
    general_arr = [' '.join(line.split()) for line in general_lines if ':' in line]
    zernike_arr = np.array([line.replace(' ', '').split() for line in zernike_lines])
    general_data = pd.DataFrame(columns=['Value', 'Unit'])
    for line in general_arr:
        spl = line.split(':', 1)
        if len(spl) == 1:
            ind = ''.join([item.title() for item in spl[0].split()])
            general_data.loc[ind] = ['', '']
        else:
            ind = ''.join([item.title() for item in spl[0].split()])
            nvals = len(valuepat_any.findall(spl[1].replace(',', '.')))
            dat = spl[1].strip().split(maxsplit=nvals)
            if len(dat) == 0:
                val = ''
                unit = ''
                general_data.loc[ind] = [val, unit]
            elif len(dat) == 1:
                if valuepat_start.search(dat[0].replace(',', '.')):  # value is number
                    val = float(dat[0].replace(',', '.'))
                else:
                    val = dat[0]
                unit = ''
                general_data.loc[ind] = [val, unit]
            elif len(dat) == 2:
                if valuepat_start.search(dat[0].replace(',', '.')):  # value is number
                    val = float(dat[0].replace(',', '.'))
                else:
                    val = dat[0]
                unit = dat[1]
                general_data.loc[ind] = [val, unit]
            else:
                for ii in range(len(dat) - 1):
                    if valuepat_start.search(dat[ii].replace(',', '.')):  # value is number
                        val = float(valuepat_start.search(dat[ii].replace(',', '.')).group())
                    else:
                        val = dat[ii]
                    unit = dat[-1]
                    general_data.loc['{}_{}'.format(ind, ii)] = [val, unit]
    zernike_data = pd.DataFrame(index=zernike_arr[:, 0].copy(),
                                columns=['Value', 'Unit', 'Function'])
    zernike_data.loc[zernike_arr[:, 0], 'Value'] = list(map(lambda s: float(s.replace(',', '.')),
                                                            zernike_arr[:, 1].copy()))
    zernike_data.loc[zernike_arr[:, 0], 'Unit'] = 'waves'
    zernike_data.loc[zernike_arr[:, 0], 'Function'] = zernike_arr[:, 3].copy()

    return general_data, zernike_data


def zernike_standard_coefficients(oss, sampling='64x64', maximum_term=37, wavelength=1, field=1,
                                  reference_opd_to_vertex=False, surface='Image', sx=0.0, sy=0.0, sr=0.0,
                                  oncomplete='Close', txtoutfile=None):
    """Wrapper around the OpticStudio Zernike Standard Coefficient Analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    sampling: str or int
        The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants integer.
    maximum_term: int
        The maximum Zernike term, defaults to 37.
    wavelength: int
        The wavelength number that is to be used. Defaults to 1 (the first wavelength).
    field:
        The field that is to be analyzed. Defaults to 1.
    reference_opd_to_vertex: bool
        If the OPD should be referenced to vertex. Defaults to False.
    surface: str or int
        The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
    sx: float
        The sx.
    sy: float
        The sy.
    sr: float
        The sr.
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
        A ZernikeStandardCoefficients analysis result. Next to the standard data, the raw text return obtained from the
        analysis will be present under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
    """

    analysistype = 'ZernikeStandardCoefficients'

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix='.txt', prefix='zospy_')
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith('.txt'):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    # Create analysis
    analysis = oss.Analyses.New_Analysis_SettingsFirst(constants.Analysis.AnalysisIDM.loc[analysistype])

    # Apply settings
    analysis.Settings.SampleSize = utils.zputils.proc_constant(constants.Analysis.SampleSizes,
                                                               utils.zputils.standardize_sampling(sampling))
    analysis.Settings.MaximumNumberOfTerms = maximum_term
    utils.zputils.analysis_set_wavelength(analysis, wavelength)
    utils.zputils.analysis_set_field(analysis, field)
    analysis.Settings.ReferenceOBDToVertex = reference_opd_to_vertex  # ToDo: Monitor name with zemax updates
    utils.zputils.analysis_set_surface(analysis, surface)
    analysis.Settings.Sx = sx
    analysis.Settings.Sy = sy
    analysis.Settings.Sr = sr

    # Calculate
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, 'r', encoding='utf-16-le')]

    general_data, zernike_data = _structure_zernike_standard_coefficients_result(line_list)
    data = AttrDict(GeneralData=general_data, Coefficients=zernike_data)

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis)

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name='Settings')

    settings.loc['SampleSize'] = constants.get_constantname_by_value(constants.Analysis.SampleSizes,
                                                                     analysis.Settings.SampleSize)
    settings.loc['MaximumNumberOfTerms'] = analysis.Settings.MaximumNumberOfTerms
    settings.loc['Wavelength'] = analysis.Settings.Wavelength.GetWavelengthNumber()  # Todo Evaluate with 'all'
    settings.loc['Field'] = analysis.Settings.Field.GetFieldNumber()  # Todo Evaluate with 'all'
    settings.loc['ReferenceOBDToVertex'] = analysis.Settings.ReferenceOBDToVertex
    settings.loc['Wavelength'] = analysis.Settings.Wavelength.GetWavelengthNumber()  # Todo Evaluate with 'all'
    settings.loc['Field'] = analysis.Settings.Field.GetFieldNumber()  # Todo Evaluate with 'all'
    settings.loc['ReferenceOBDToVertex'] = analysis.Settings.Surface.GetSurfaceNumber()  # Todo Evaluate with 'all'
    settings.loc['Sx'] = sx
    settings.loc['Sy'] = sy
    settings.loc['Sr'] = sr

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         RawTextData=line_list, TxtOutFile=txtoutfile)  # Set additional params

    # cleanup
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
