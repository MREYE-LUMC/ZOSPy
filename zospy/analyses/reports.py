"""Zemax OpticStudio analyses from the Reports category."""

from __future__ import annotations

import os
import re
from tempfile import mkstemp
from typing import Any

import numpy as np
import pandas as pd

from zospy.analyses.base import AnalysisResult, AttrDict, OnComplete, new_analysis
from zospy.api import constants
from zospy.zpcore import OpticStudioSystem

# TODO use value from zospy.api._config
REFLOAT = re.compile(r"^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?$")
RECOMMASEP = re.compile(r"(?<=\d),(?=\d)")


def _structure_surface_data_result(line_list: list[str]) -> pd.Series:
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

    lm = pd.Series(
        index=[
            "Thickness",
            "Index of Refraction",
            "Best Fit Glass",
            "Surface Powers (as situated)",
            "Surface Powers (in air)",
            "Shape Factor",
        ],
        data=[0] * 6,
        dtype=int,
    )

    for item in lm.index:
        for num, line in enumerate(line_list):
            if line.lstrip().startswith(item):
                lm.loc[item] = num
                break

    general_lm = ["File", "Title", "Date", "Comment", "Lens units"]
    surface_lm = ["Thickness", "Diameter", "Y Edge Thick", "X Edge Thick"]
    ri_lm = ["nd", "Abbe", "dPgF", "Best Fit Glass"]

    for line in line_list[: lm["Thickness"]]:
        for item in general_lm:
            if line.lstrip().startswith(item):
                val = line.split(":")[-1].strip()

                fval = val.replace(",", ".")  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc["General", item] = val

    for line in line_list[lm["Thickness"] : lm["Index of Refraction"]]:
        for item in surface_lm:
            if line.lstrip().startswith(item):
                val = line.split(":")[-1].strip()

                fval = val.replace(",", ".")  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc["Surface", item] = val

    for line in line_list[lm["Index of Refraction"] : lm["Best Fit Glass"] + 1]:  # + 1 as bfg should be included
        for item in ri_lm:
            if line.lstrip().startswith(item):
                val = line.split(":")[-1].strip()

                fval = val.replace(",", ".")  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc["IndexOfRefraction", item] = val

    for line in line_list[
        lm["Best Fit Glass"] + 1 : lm["Surface Powers (as situated)"]
    ]:  # + 1 as bfg should be excluded
        if len(line.split("\t")) == 3:
            _, wl, ri = line.split("\t")
            fwl = wl.strip().replace(",", ".")
            if REFLOAT.match(fwl):
                wl = float(fwl)
            else:
                continue  # is not an actual wavelength

            ri = ri.strip().replace(",", ".")
            if REFLOAT.match(ri):
                ri = float(ri)

            res.loc["IndexOfRefractionPerWavelength", wl] = ri

    for line in line_list[lm["Surface Powers (as situated)"] + 1 : lm["Surface Powers (in air)"]]:
        if len(line.split(":")) == 2:
            param, val = line.split(":")
            param = re.sub(r" +", " ", param).strip()

            fval = val.strip().replace(",", ".")
            if REFLOAT.match(fval):
                val = float(fval)

            res.loc["SurfacePowerAsSituated", param] = val

    for line in line_list[lm["Surface Powers (in air)"] + 1 : lm["Shape Factor"]]:
        if len(line.split(":")) == 2:
            param, val = line.split(":")
            param = re.sub(r" +", " ", param).strip()

            fval = val.strip().replace(",", ".")
            if REFLOAT.match(fval):
                val = float(fval)

            res.loc["SurfacePowerInAir", param] = val

    for line in line_list[lm["Shape Factor"] :]:
        if len(line.split(":")) == 2:
            param, val = line.split(":")
            param = re.sub(r" +", " ", param).strip()

            val = val.strip()
            fval = val.replace(",", ".")
            if REFLOAT.match(fval):
                val = float(fval)

            res.loc["Other", param] = val

    return res


def surface_data(
    oss: OpticStudioSystem,
    surface: int,
    oncomplete: OnComplete | str = OnComplete.Close,
    cfgoutfile: str | None = None,
    txtoutfile: str | None = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Surface Data Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    surface: int
        The surface number that is to be analyzed
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    cfgoutfile: str | None
        The configuration file to which the current configuration is saved. If None, a temporary file will be created
        and deleted. If string, it should be a full system path with '.CFG' as extension, after which the file will be
        saved in that location. (Allowing usage of this configuration file using surface_data_fromcfg()). Defaults to
        None.
    txtoutfile: str | None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.SurfaceDataSettings

    if cfgoutfile is None:
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)
        cleancfg = True
    else:
        if not cfgoutfile.endswith(".CFG"):
            raise ValueError('cfgfile should end with ".CFG"')
        cleancfg = False

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Modify surface in the settings file
    an_sett = analysis.GetSettings()
    an_sett.SaveTo(cfgoutfile)

    settingsbstr = b"".join(open(cfgoutfile, "rb").readlines())
    settingsbarr = bytearray(settingsbstr)
    settingsbarr[20] = surface  # 20 maps to the selected surface

    with open(cfgoutfile, "wb") as bfile:
        bfile.write(settingsbarr)

    an_sett.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]
    data = _structure_surface_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name="Settings", dtype=object)
    settings.loc["Surface"] = surface

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        RawTextData=line_list,
        CgfOutFile=cfgoutfile,
        TxtOutFile=txtoutfile,
    )  # Set additional params

    # cleanup if needed
    if cleancfg:
        os.remove(cfgoutfile)
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)


def surface_data_fromcfg(
    oss: OpticStudioSystem, cfgfile: str, oncomplete: OnComplete | str = OnComplete.Close, txtoutfile: str | None = None
) -> AnalysisResult:
    """Wrapper around the OpticStudio Surface Data Analysis that uses a predefined configuration file.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    cfgfile: str
        The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    txtoutfile: str | None
        The textfile to which the Zemax output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the used cfgfile will be present under
        'UsedCfgFile', raw text return under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.SurfaceDataSettings

    if not cfgfile.endswith(".CFG"):
        raise ValueError('cfgfile should end with ".CFG"')

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Load settings
    analysis.Settings.LoadFrom(cfgfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]
    data = _structure_surface_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Manually create settings as they cannot be accessed
    # TODO replace by None
    settings = pd.Series(name="Settings", dtype=object)

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        UsedCfgFile=cfgfile,
        RawTextData=line_list,
        TxtOutFile=txtoutfile,
    )  # Set additional params

    # cleanup
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)


def _structure_system_data_result(line_list: list[str]) -> dict[str, Any]:
    """Structures the result of a system data report.

    Parameters
    ----------
    line_list: list[str]
        The line list obtained by reading in the results

    Returns
    -------
    dict
        The results structured in a dictionary
    """
    # Create output dict
    res = AttrDict()

    # Add header
    hdr = line_list[0].strip().replace("\ufeff", "")
    res["Header"] = hdr

    # Register landmarks
    landmarks = ["GENERAL LENS DATA", "Fields", "Vignetting Factors", "Wavelengths", "Predicted coordinate ABCD matrix"]
    comp = re.compile(rf'^({"|".join(landmarks)})', re.IGNORECASE)
    inds = {
        comp.match(line).group().lower(): {"rnum": rnum, "name": comp.match(line).group()}
        for rnum, line in enumerate(line_list)
        if comp.match(line)
    }

    order_of_appearance = [item[0] for item in sorted(inds.items(), key=lambda x: x[1]["rnum"])]

    # Add general lens data
    target = "general lens data"
    gld = pd.Series(dtype=object)
    if target in inds:
        section_start = inds[target]["rnum"] + 1  # + 1 to ignore section title

        # Get endpoint
        if order_of_appearance.index(target) == len(inds) - 1:
            section_end = len(line_list)
        else:
            target2 = order_of_appearance[order_of_appearance.index(target) + 1]
            section_end = inds[target2]["rnum"]

        for line in line_list[section_start:section_end]:
            if line.strip() == "":
                continue

            # Get param and value, strip whitespaces
            param, val = line.split(":")
            param = re.sub(r"\s+", " ", param).strip()

            # convert value to float if needed
            val = re.sub(r"\s+", " ", val).strip()
            val = RECOMMASEP.sub(".", val)
            if REFLOAT.match(val):
                if "." in val or "e" in val:
                    val = float(val)
                else:
                    val = int(val)

            # add
            ii = 0
            while param in gld.index:
                ii += 1
                param = f"{param} {ii}"
            gld.loc[param] = val
    res["GeneralLensData"] = gld

    # Fields, Wavelengths
    for target in ["fields", "wavelengths"]:
        info = pd.Series(dtype=object)
        data = pd.DataFrame()
        if target in inds:
            section_start = inds[target]["rnum"]

            # Get endpoint
            if order_of_appearance.index(target) == len(inds) - 1:
                section_end = len(line_list)
            else:
                target2 = order_of_appearance[order_of_appearance.index(target) + 1]
                section_end = inds[target2]["rnum"]

            for ii, line in enumerate(line_list[section_start:section_end]):
                if line.strip().startswith("#"):
                    ht_loc = section_start + ii
                    break
            else:
                ht_loc = None

            param_end = ht_loc if ht_loc is not None else section_end
            for line in line_list[section_start:param_end]:
                if line.strip() == "":
                    continue

                # Get param and value, strip whitespaces
                param, val = line.split(":")
                param = re.sub(r"\s+", " ", param).strip()

                # convert value to float if needed
                val = re.sub(r"\s+", " ", val).strip()
                val = RECOMMASEP.sub(".", val)
                if REFLOAT.match(val):
                    if "." in val:
                        val = float(val)
                    else:
                        val = int(val)

                # add
                ii = 0
                while param in gld.index:
                    ii += 1
                    param = f"{param} {ii}"
                info.loc[param] = val

            if ht_loc is not None:
                columns = re.sub(r"\s+", " ", line_list[ht_loc]).strip().split(" ")
                data = []
                for ii in range(ht_loc + 1, section_end):
                    if line_list[ii].strip() == "":
                        continue
                    items = re.sub(r"\s+", " ", line_list[ii]).strip().split(" ")
                    values = []
                    for item in items:
                        val = RECOMMASEP.sub(".", item)
                        if REFLOAT.match(val):
                            if "." in val:
                                val = float(val)
                            else:
                                val = int(val)
                        values.append(val)
                    data.append(values)
                data = pd.DataFrame(columns=columns, data=data)
            res[inds[target]["name"]] = AttrDict(Info=info, Data=data)

    # Vignetting factors
    target = "vignetting factors"
    if target in inds:
        section_start = inds[target]["rnum"] + 1  # + 1 to ignore section title

        # Get endpoint
        if order_of_appearance.index(target) == len(inds) - 1:
            section_end = len(line_list)
        else:
            target2 = order_of_appearance[order_of_appearance.index(target) + 1]
            section_end = inds[target2]["rnum"]

        for ii, line in enumerate(line_list[section_start:section_end]):
            if line.strip().startswith("#"):
                ht_loc = section_start + ii
                break
        else:
            ht_loc = None

        if ht_loc is not None:
            columns = re.sub(r"\s+", " ", line_list[ht_loc]).strip().split(" ")
            data = []
            for ii in range(ht_loc + 1, section_end):
                if line_list[ii].strip() == "":
                    continue
                items = re.sub(r"\s+", " ", line_list[ii]).strip().split(" ")
                values = []
                for item in items:
                    val = RECOMMASEP.sub(".", item)
                    if REFLOAT.match(val):
                        if "." in val:
                            val = float(val)
                        else:
                            val = int(val)
                    values.append(val)
                data.append(values)
            data = pd.DataFrame(columns=columns, data=data)
        res["VignettingFactors"] = data

    # Predicted ABCD matrix
    target = "predicted coordinate abcd matrix"
    abcd = pd.Series(dtype=object)
    if target in inds:
        section_start = inds[target]["rnum"] + 1  # + 1 to ignore section title

        # Get endpoint
        if order_of_appearance.index(target) == len(inds) - 1:
            section_end = len(line_list)
        else:
            target2 = order_of_appearance[order_of_appearance.index(target) + 1]
            section_end = inds[target2]["rnum"]

        for line in line_list[section_start:section_end]:
            if line.strip() == "":
                continue

            # Get param and value, strip whitespaces
            param, val = line.split("=")
            param = re.sub(r"\s+", " ", param).strip()

            # convert value to float if needed
            val = re.sub(r"\s+", " ", val).strip()
            val = RECOMMASEP.sub(".", val)
            if REFLOAT.match(val):
                if "." in val:
                    val = float(val)
                else:
                    val = int(val)

            # add
            ii = 0
            while param in gld.index:
                ii += 1
                param = f"{param} {ii}"
            abcd.loc[param] = val
        res["PredictedCoordinateABCDMatrix"] = abcd

        return res


def system_data(
    oss: OpticStudioSystem, oncomplete: OnComplete | str = OnComplete.Close, txtoutfile: str | None = None
) -> AnalysisResult:
    """Wrapper around the OpticStudio System Data Analysis.

    Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
    subsequently reading in this file

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    oncomplete: OnComplete | str
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
        A SystemData analysis result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.SystemData

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]
    data = _structure_system_data_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=None,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        RawTextData=line_list,
        TxtOutFile=txtoutfile,
    )  # Set additional params

    # cleanup if needed
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)


def _structure_cardinal_point_result(line_list: list[str]) -> pd.Series:
    """Structures the result of a cardinal point analysis.

    Parameters
    ----------
    line_list: list[str]
        The line list obtained by reading in the results

    Returns
    -------
    pd.Series
        The results structured in a Series
    """
    res = pd.Series(index=pd.MultiIndex([[]] * 2, [[]] * 2), dtype=object)

    # Determine landmarks
    idx = [
        "Starting surface",
        "Ending surface",
        "Object space positions",
        "Focal Length",
        "Anti-Nodal Planes",
        "Error computing cardinal points",
    ]
    lm = pd.Series(index=idx, data=[pd.NA] * len(idx), dtype=object)

    for item in lm.index:
        for num, line in enumerate(line_list):
            if line.lstrip().startswith(item):
                lm.loc[item] = num
                break

    general_lm = ["File", "Title", "Date", "Wavelength", "Orientation", "Lens units"]
    surface_lm = ["Starting surface", "Ending surface"]
    carpoints_lm = [
        "Focal Length",
        "Focal Planes",
        "Principal Planes",
        "Anti-Principal Planes",
        "Nodal Planes",
        "Anti-Nodal Planes",
    ]

    # Get general info
    for line in line_list[: lm["Object space positions"]]:
        for item in general_lm:
            if line.lstrip().startswith(item):
                val = line.split(":")[-1].strip()

                fval = val.replace(",", ".")  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc["General", item] = val

    space1 = space2 = "Space"
    for option in ["Focal Length", "Error computing cardinal points"]:
        try:
            res.loc["General", "Info"] = "\n".join(
                [
                    item.strip()
                    for item in line_list[lm["Object space positions"] : lm[option] - 1]
                    if item.strip() != ""
                ]
            )
            _, space1, space2 = line_list[lm[option] - 1].split("\t")
            space1 = space1.strip()
            space2 = space2.strip()

            break
        except TypeError:
            continue
    else:
        res.loc["General", "Info"] = "ZOSPy: Cannot determine spaces"

    for line in line_list[lm["Starting surface"] : lm["Ending surface"] + 1]:
        for item in surface_lm:
            if line.lstrip().startswith(item):
                val = line.split(":")[-1].strip()

                fval = val.replace(",", ".")  # to enable conversion to float
                if REFLOAT.match(fval):
                    val = float(fval)

                res.loc["Surface", item] = val

    try:
        for line in line_list[lm["Focal Length"] : lm["Anti-Nodal Planes"] + 1]:
            for item in carpoints_lm:
                if line.lstrip().startswith(item):
                    val1, val2 = line.split(":")[-1].strip().split("\t")
                    val1 = val1.strip()
                    val2 = val2.strip()

                    fval1 = val1.replace(",", ".")  # to enable conversion to float
                    if REFLOAT.match(fval1):
                        val1 = float(fval1)

                    fval2 = val2.replace(",", ".")  # to enable conversion to float
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


def cardinal_points(
    oss: OpticStudioSystem,
    surface_1: int,
    surface_2: int,
    oncomplete: OnComplete | str = OnComplete.Close,
    cfgoutfile: str | None = None,
    txtoutfile: str | None = None,
) -> AnalysisResult:
    """Wrapper around the OpticStudio Cardinal Point Analysis.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    surface_1: int
        The surface number corresponding to the first surface of the analyzed system
    surface_2: int
        The surface number corresponding to the last surface of the analyzed system
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    cfgoutfile: str | None
        The configuration file to which the current configuration is saved. If None, a temporary file will be created
        and deleted. If string, it should be a full system path with '.CFG' as extension, after which the file will be
        saved in that location. (Allowing usage of this configuration file using surface_data_fromcfg()). Defaults to
        None.
    txtoutfile: str | None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the raw text return obtained from the analysis
        will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.CardinalPoints

    if surface_1 > surface_2:
        raise ValueError("Surface 1 cannot be higher than Surface 2")

    if cfgoutfile is None:
        fd, cfgoutfile = mkstemp(suffix=".CFG", prefix="zospy_")
        os.close(fd)
        cleancfg = True
    else:
        if not cfgoutfile.endswith(".CFG"):
            raise ValueError('cfgoutfile should end with ".CFG"')
        cleancfg = False

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtoutfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Modify surface in the settings file
    analysis_settings = analysis.Settings
    analysis_settings.SaveTo(cfgoutfile)

    settingsbstr = b"".join(open(cfgoutfile, "rb").readlines())
    settingsbarr = bytearray(settingsbstr)
    settingsbarr[20] = surface_1  # byte 20 maps to the first surface
    settingsbarr[24] = surface_2  # byte 24 maps to the first surface

    with open(cfgoutfile, "wb") as bfile:
        bfile.write(settingsbarr)

    analysis_settings.LoadFrom(cfgoutfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]
    data = _structure_cardinal_point_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Manually create settings as they cannot be accessed
    settings = pd.Series(name="Settings", dtype=object)
    settings.loc["Surface1"] = surface_1
    settings.loc["Surface2"] = surface_2

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        RawTextData=line_list,
        CgfOutFile=cfgoutfile,
        TxtOutFile=txtoutfile,
    )  # Set additional params

    # cleanup if needed
    if cleancfg:
        os.remove(cfgoutfile)
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)


def cardinal_points_fromcfg(
    oss: OpticStudioSystem, cfgfile: str, oncomplete: OnComplete | str = OnComplete.Close, txtoutfile: str | None = None
) -> AnalysisResult:
    """Wrapper around the OpticStudio Cardinal Point Analysis that uses a predefined configuration file.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance. Should be sequential.
    cfgfile: str
        The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
    oncomplete: OnComplete | str
        Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If 'Close',
        the analysis will be closed after completion. If 'Release', the analysis will remain open in OpticStudio, but
        the link with python will be destroyed. If 'Sustain' the analysis will be kept open in OpticStudio and the link
        with python will be sustained. To enable interaction when oncomplete == 'Sustain', the OpticStudio Analysis
        instance will be available in the returned AnalysisResult through AnalysisResult.Analysis. Defaults to 'Close'.
    txtoutfile: str | None
        The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and deleted. If
        string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
        location. Defaults to None.

    Returns
    -------
    AnalysisResult
        A SurfaceDataSettings analysis result. Next to the standard data, the used cfgfile will be present under
        'UsedCfgFile', raw text return under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
    """
    analysis_type = constants.Analysis.AnalysisIDM.CardinalPoints

    if not cfgfile.endswith(".CFG"):
        raise ValueError('cfgfile should end with ".CFG"')

    if txtoutfile is None:
        fd, txtoutfile = mkstemp(suffix=".txt", prefix="zospy_")
        os.close(fd)
        cleantxt = True
    else:
        if not txtoutfile.endswith(".txt"):
            raise ValueError('txtfile should end with ".txt"')
        cleantxt = False

    analysis = new_analysis(oss, analysis_type)

    # Load the settings file
    analysis.Settings.LoadFrom(cfgfile)

    # Run analysis
    analysis.ApplyAndWaitForCompletion()

    # Get results
    analysis.Results.GetTextFile(txtoutfile)
    line_list = [line for line in open(txtoutfile, "r", encoding=oss._ZOS.get_txtfile_encoding())]
    data = _structure_cardinal_point_result(line_list)

    # Get headerdata, metadata and messages
    headerdata = analysis.get_header_data()
    metadata = analysis.get_metadata()
    messages = analysis.get_messages()

    # Manually create settings as they cannot be accessed
    # TODO replace by None
    settings = pd.Series(name="Settings", dtype=object)

    # Create output
    result = AnalysisResult(
        analysistype=str(analysis_type),
        data=data,
        settings=settings,
        metadata=metadata,
        headerdata=headerdata,
        messages=messages,
        UsedCfgFile=cfgfile,
        RawTextData=line_list,
        TxtOutFile=txtoutfile,
    )  # Set additional params

    # cleanup if needed
    if cleantxt:
        os.remove(txtoutfile)

    return analysis.complete(oncomplete, result)
