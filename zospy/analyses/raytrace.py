import os
import re
from tempfile import mkstemp
from io import StringIO

import numpy as np
import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult, AttrDict
from zospy.api import constants


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
                          delimiter='\t')

        # Recover case of target
        keyname = inds[target]['name'].replace(' ','')

        # Add to result dictionary
        res[keyname] = df

    return res


def single_ray_trace(oss, Hx=0, Hy=0, Px=0, Py=1, wavelength=1, field=0, ztype=0,
                     global_coordinates=False, oncomplete='Close', txtoutfile=None):
    """Wrapper around the OpticStudio Single Ray Trace Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    Hx: float
        Normalized X Field Coord. Defaults to 0.
    Hy: float
        Normalized Y Field Coord. Defaults to 0.
    Px: float
        Normalized X Pupil Coord. Defaults to 0.
    Py: float
        Normalized Y Pupil Coord. Defaults to 1.
    wavelength: int
        The wavelength number that is to be used. Must be an integer specifying the wavelength number. 
        Defaults to 1.
    field: int
        The field number that is to be used. Must an integer specifying the field number. "Arbitrary" is 0. Defaults to 0.
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
    analysis.Settings.Hx = Hx
    analysis.Settings.Hy = Hy
    analysis.Settings.Px = Px
    analysis.Settings.Py = Py
    utils.zputils.analysis_set_wavelength(analysis, wavelength)
    utils.zputils.analysis_set_field(analysis, field)
    analysis.Settings.Type = ztype
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

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=None, metadata=metadata,
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
