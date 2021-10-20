import os
import re
from tempfile import mkstemp

import numpy as np
import pandas as pd

from zospy import utils
from zospy.analyses.base import AnalysisResult

REFLOAT = re.compile(r'^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?$')


def _structure_surface_data_result(line_list):
    """Structures the result of a surface data analysis.

    Parameters
    ----------
    line_list: list of str
        The line list obtained by reading in the results

    Returns
    -------
    pd.Series
        The results structured in a Series
    """
    res = pd.Series(index=pd.MultiIndex([[]] * 2, [[]] * 2), dtype=object)

    lm = pd.Series(index=['Thickness', 'Index of Refraction',
                          'Best Fit Glass',
                          'Surface Powers (as situated)',
                          'Surface Powers (in air)',
                          'Shape Factor'], dtype=int)

    for item in lm.index:
        for num, line in enumerate(line_list):
            if line.lstrip().startswith(item):
                lm.loc[item] = num
                break

    general_lm = ['File', 'Title', 'Date', 'Comment', 'Lens units']
    surface_lm = ['Thickness', 'Diameter', 'Y Edge Thick', 'X Edge Thick']
    ri_lm = ['nd', 'Abbe', 'dPgF', 'Best Fit Glass']

    for line in line_list[:lm['Thickness']]:
        for item in general_lm:
            if line.lstrip().startswith(item):
                val = line.split(':')[-1].strip()

                fval = val.replace(',', '.')  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc['General', item] = val

    for line in line_list[lm['Thickness']:lm['Index of Refraction']]:
        for item in surface_lm:
            if line.lstrip().startswith(item):

                val = line.split(':')[-1].strip()

                fval = val.replace(',', '.')  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc['Surface', item] = val

    for line in line_list[lm['Index of Refraction']:lm['Best Fit Glass'] + 1]:  # + 1 as bfg should be included
        for item in ri_lm:
            if line.lstrip().startswith(item):

                val = line.split(':')[-1].strip()

                fval = val.replace(',', '.')  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc['IndexOfRefraction', item] = val

    for line in line_list[lm['Best Fit Glass'] + 1:lm['Surface Powers (as situated)']]:  # + 1 as bfg should be excluded
        if len(line.split('\t')) == 3:
            _, wl, ri = line.split('\t')
            fwl = wl.strip().replace(',', '.')
            if REFLOAT.match(fwl):
                wl = float(fwl)
            else:
                continue  # is not an actual wavelength

            ri = ri.strip().replace(',', '.')
            if REFLOAT.match(ri):
                ri = float(ri)

            res.loc['IndexOfRefractionPerWavelength', wl] = ri

    for line in line_list[lm['Surface Powers (as situated)'] + 1:lm['Surface Powers (in air)']]:
        if len(line.split(':')) == 2:
            param, val = line.split(':')
            param = re.sub(r' +', ' ', param).strip()

            fval = val.strip().replace(',', '.')
            if REFLOAT.match(fval):
                val = float(fval)

            res.loc['SurfacePowerAsSituated', param] = val

    for line in line_list[lm['Surface Powers (in air)'] + 1:lm['Shape Factor']]:
        if len(line.split(':')) == 2:
            param, val = line.split(':')
            param = re.sub(r' +', ' ', param).strip()

            fval = val.strip().replace(',', '.')
            if REFLOAT.match(fval):
                val = float(fval)

            res.loc['SurfacePowerInAir', param] = val

    for line in line_list[lm['Shape Factor']:]:
        if len(line.split(':')) == 2:
            param, val = line.split(':')
            param = re.sub(r' +', ' ', param).strip()

            val = val.strip()
            fval = val.replace(',', '.')
            if REFLOAT.match(fval):
                val = float(fval)

            res.loc['Other', param] = val

    return res


def surface_data(oss, surf, oncomplete='Close', cfgoutfile=None, txtoutfile=None):
    """Wrapper around the OpticStudio Surface Data Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    surf: int
        The surface number that is to be analyzed
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    cfgoutfile: str or None
        The configuration file to which the current configuration is saved. If None, a temporary file will be created
        and deleted. If string, it should be a full system path with '.CFG' as extension, after which the file will be
        saved in that location. (Allowing usage of this configuration file using surface_data_fromcfg()). Defaults to
        None.
    txtoutfile: str or None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under 'TxtOutFile'.
    """

    analysistype = 'SurfaceDataSettings'

    if cfgoutfile is None:
        fd, cfgoutfile = mkstemp(suffix='.CFG', prefix='zospy_')
        os.close(fd)
        cleancfg = True
    else:
        if not cfgoutfile.endswith('.CFG'):
            raise ValueError('cfgfile should end with ".CFG"')
        cleancfg = False

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix='.txt', prefix='zospy_')
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith('.txt'):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = oss.System.Analyses.New_Analysis_SettingsFirst(oss.Constants.Analysis.AnalysisIDM.loc[analysistype])

    # Modify surface in the settings file
    an_sett = analysis.GetSettings()
    an_sett.SaveTo(cfgoutfile)

    settingsbstr = b''.join(open(cfgoutfile, 'rb').readlines())
    settingsbarr = bytearray(settingsbstr)
    settingsbarr[20] = surf  # 20 maps to the selected surface

    with open(cfgoutfile, 'wb') as bfile:
        bfile.write(settingsbarr)

    an_sett.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, 'r', encoding='utf-16-le')]
    data = _structure_surface_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis, constants=oss.Constants)

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name='Settings')
    settings.loc['Surface'] = surf

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         RawTextData=line_list, CgfOutFile=cfgoutfile, TxtOutFile=txtoutfile)  # Set additional params

    # cleanup if needed
    if cleancfg:
        os.remove(cfgoutfile)
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


def surface_data_fromcfg(oss, cfgfile, oncomplete='Close', txtoutfile=None):
    """Wrapper around the OpticStudio Surface Data Analysis that uses a predefined configuration file.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    cfgfile: str
        The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    txtoutfile: str or None
        The textfile to which the Zemax output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the used cfgfile will be present under
        'UsedCfgFile', raw text return under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
    """

    analysistype = 'SurfaceDataSettings'

    if not cfgfile.endswith('.CFG'):
        raise ValueError('cfgfile should end with ".CFG"')

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix='.txt', prefix='zospy_')
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith('.txt'):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = oss.System.Analyses.New_Analysis_SettingsFirst(oss.Constants.Analysis.AnalysisIDM.loc[analysistype])

    # Load settings
    analysis.Settings.LoadFrom(cfgfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, 'r', encoding='utf-16-le')]
    data = _structure_surface_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis, constants=oss.Constants)

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name='Settings')

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         UsedCfgFile=cfgfile, RawTextData=line_list, TxtOutFile=txtoutfile)  # Set additional params

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


def _structure_cardinal_point_result(line_list):
    """Structures the result of a cardinal point analysis.

    Parameters
    ----------
    line_list: list of str
        The line list obtained by reading in the results

    Returns
    -------
    pd.Series
        The results structured in a Series
    """
    res = pd.Series(index=pd.MultiIndex([[]] * 2, [[]] * 2), dtype=object)

    # Determine landmarks
    idx = ['Starting surface',
           'Ending surface',
           'Object space positions',
           'Focal Length',
           'Anti-Nodal Planes',
           'Error computing cardinal points']
    lm = pd.Series(index=idx, data=[pd.NA]*len(idx), dtype=object)

    for item in lm.index:
        for num, line in enumerate(line_list):
            if line.lstrip().startswith(item):
                lm.loc[item] = num
                break

    general_lm = ['File', 'Title', 'Date', 'Wavelength', 'Orientation', 'Lens units']
    surface_lm = ['Starting surface', 'Ending surface']
    carpoints_lm = ['Focal Length', 'Focal Planes', 'Principal Planes', 'Anti-Principal Planes',
                    'Nodal Planes', 'Anti-Nodal Planes']

    # Get general info
    for line in line_list[:lm['Object space positions']]:
        for item in general_lm:
            if line.lstrip().startswith(item):
                val = line.split(':')[-1].strip()

                fval = val.replace(',', '.')  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc['General', item] = val

    space1 = space2 = 'Space'
    for option in ['Focal Length', 'Error computing cardinal points']:
        try:
            res.loc['General', 'Info'] = '\n'.join([item.strip() for item in
                                                    line_list[lm['Object space positions']:lm[option]-1]
                                                    if item.strip() != ''])
            _, space1, space2 = line_list[lm[option] - 1].split('\t')
            space1 = space1.strip()
            space2 = space2.strip()

            break
        except TypeError:
            continue
    else:
        res.loc['General', 'Info'] = 'ZOSPy: Cannot determine spaces'

    for line in line_list[lm['Starting surface']:lm['Ending surface'] + 1]:
        for item in surface_lm:
            if line.lstrip().startswith(item):
                val = line.split(':')[-1].strip()

                fval = val.replace(',', '.')  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc['Surface', item] = val

    try:
        for line in line_list[lm['Focal Length']:lm['Anti-Nodal Planes'] + 1]:
            for item in carpoints_lm:
                if line.lstrip().startswith(item):
                    val1, val2 = line.split(':')[-1].strip().split('\t')
                    val1 = val1.strip()
                    val2 = val2.strip()

                    fval1 = val1.replace(',', '.')  # to enable conversion to float
                    if REFLOAT.match(fval1):
                        val1 = float(fval1)

                    fval2 = val2.replace(',', '.')  # to enable conversion to float
                    if REFLOAT.match(fval2):
                        val2 = float(fval2)

                    res.loc[space1, item] = val1
                    res.loc[space2, item] = val2
    except TypeError:
        for item in carpoints_lm:
            res.loc[space1, item] = np.nan
            res.loc[space2, item] = np.nan
    res = res.loc[res.index.get_level_values(0).unique()]

    return res


def cardinal_points(oss, surf1, surf2, oncomplete='Close', cfgoutfile=None, txtoutfile=None):
    """Wrapper around the OpticStudio Cardinal Point Analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    surf1: int
        The surface number corresponding to the first surface of the analyzed system
    surf2: int
        The surface number corresponding to the last surface of the analyzed system
    oncomplete: str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    cfgoutfile: str or None
        The configuration file to which the current configuration is saved. If None, a temporary file will be created
        and deleted. If string, it should be a full system path with '.CFG' as extension, after which the file will be
        saved in that location. (Allowing usage of this configuration file using surface_data_fromcfg()). Defaults to
        None.
    txtoutfile: str or None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under 'TxtOutFile'.
    """

    analysistype = 'CardinalPoints'

    if surf1 > surf2:
        raise ValueError('Surface 1 cannot be higher than Surface 2')

    if cfgoutfile is None:
        fd, cfgoutfile = mkstemp(suffix='.CFG', prefix='zospy_')
        os.close(fd)
        cleancfg = True
    else:
        if not cfgoutfile.endswith('.CFG'):
            raise ValueError('cfgoutfile should end with ".CFG"')
        cleancfg = False

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix='.txt', prefix='zospy_')
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith('.txt'):
            raise ValueError('txtoutfile should end with ".txt"')
        cleantxt = False

    analysis = oss.System.Analyses.New_Analysis_SettingsFirst(oss.Constants.Analysis.AnalysisIDM.loc[analysistype])

    # Modify surface in the settings file
    an_sett = analysis.GetSettings()
    an_sett.SaveTo(cfgoutfile)

    settingsbstr = b''.join(open(cfgoutfile, 'rb').readlines())
    settingsbarr = bytearray(settingsbstr)
    settingsbarr[20] = surf1  # byte 20 maps to the first surface
    settingsbarr[24] = surf2  # byte 24 maps to the first surface

    with open(cfgoutfile, 'wb') as bfile:
        bfile.write(settingsbarr)

    an_sett.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, 'r', encoding='utf-16-le')]
    data = _structure_cardinal_point_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis, constants=oss.Constants)

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name='Settings')
    settings.loc['Surface1'] = surf1
    settings.loc['Surface2'] = surf2

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         RawTextData=line_list, CgfOutFile=cfgoutfile, TxtOutFile=txtoutfile)  # Set additional params

    # cleanup if needed
    if cleancfg:
        os.remove(cfgoutfile)
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


def cardinal_points_fromcfg(oss, cfgfile, oncomplete='Close', txtoutfile=None):
    """Wrapper around the OpticStudio Cardinal Point Analysis that uses a predefined configuration file.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    cfgfile: str
        The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
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
        A SurfaceDataSettings analysis result. Next to the standard data, the used cfgfile will be present under
        'UsedCfgFile', raw text return under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
    """

    analysistype = 'CardinalPoints'

    if not cfgfile.endswith('.CFG'):
        raise ValueError('cfgfile should end with ".CFG"')

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix='.txt', prefix='zospy_')
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith('.txt'):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = oss.System.Analyses.New_Analysis_SettingsFirst(oss.Constants.Analysis.AnalysisIDM.loc[analysistype])

    # Load the settings file
    analysis.Settings.LoadFrom(cfgfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, 'r', encoding='utf-16-le')]
    data = _structure_cardinal_point_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = utils.zputils.analysis_get_headerdata(analysis)
    metadata = utils.zputils.analysis_get_metadata(analysis)
    messages = utils.zputils.analysis_get_messages(analysis, constants=oss.Constants)

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name='Settings')

    # Create output
    ret = AnalysisResult(analysistype=analysistype, data=data, settings=settings, metadata=metadata,
                         headerdata=headerdata, messages=messages,
                         UsedCfgFile=cfgfile, RawTextData=line_list, TxtOutFile=txtoutfile)  # Set additional params

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
