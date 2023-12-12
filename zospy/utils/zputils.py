from __future__ import annotations

import re
from collections.abc import MutableMapping
from typing import TypeVar

import numpy as np
import pandas as pd

from zospy.api import _ZOSAPI


def flatten_dict(unflattend_dict, parent_key="", sep=".", keep_unflattend=False):
    """Flattens an nested dictionary to a one-level dictionary.

    Parameters
    ----------
    unflattend_dict: dict or MutableMapping
        A dictionary with nested dictionaries
    parent_key: str
        A key to which the flattened keys are added. Mainly present to support flatting of subdicts, should be '' in
        most primary calls.. Defaults to ''.
    sep: str
        The separator used for the flat items. Defaults to '.'
    keep_unflattend: bool
        Whether the keys, value pairs of nested dicts or MutableMappings should remain present in the output or not.
        Defaults to False

    Returns
    -------
    dict
        A dictionary with one (flattened) key for a value.
    """
    items = []
    for key, value in unflattend_dict.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            if keep_unflattend:
                items.append((new_key, value))
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def flatten_dlltreedict(dlltreedict):
    """Flattens the set of nested dictionaries that represent a dll tree.

    For instance, it can flatten the dictionary tree obtained from ZOSAPINestedNameSpaces.json.

    Parameters
    ----------
    dlltreedict: dict
        A dictionary with nested dictionaries

    Returns
    -------
    list:
        A list with the items of the nested dictionaries.
    """
    flatdict = flatten_dict(dlltreedict, parent_key="", sep=".", keep_unflattend=True)
    flatlist = list(flatdict.keys())
    return flatlist


def unpack_dataseries(dataseries: _ZOSAPI.Analysis.Data.IAR_DataSeries) -> pd.DataFrame:
    """Unpacks an OpticStudio dataseries in a dataframe.

    Parameters
    ----------
    dataseries : ZOSAPI.Analysis.Data.IAR_DataSeries
        Opticstudio DataSeries object.

    Returns
    -------
    pd.DataFrame
        A DataFrame holding all data and labels.
    """
    columns = pd.MultiIndex.from_product(
        [[dataseries.Description], list(dataseries.SeriesLabels)], names=["Description", "SeriesLabels"]
    )
    index = np.array(list(dataseries.XData.Data))
    data = np.array(list(dataseries.YData.Data)).reshape(dataseries.YData.Rows, dataseries.YData.Cols)
    df = pd.DataFrame(columns=columns, index=index, data=data)  # ToDo evaluate
    df.index.name = dataseries.XLabel

    return df


def unpack_datagrid(datagrid: _ZOSAPI.Analysis.Data.IAR_DataGrid) -> pd.DataFrame:
    """Unpack an OpticStudio datagrid to a Pandas DataFrame.

    Parameters
    ----------
    datagrid : ZOSAPI.Analysis.Data.IAR_DataGrid
        OpticStudio DataGrid object.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the grid and the spacing on the rows and columns.
        The X- and YLabels are assigned to `df.columns.name` and `df.index.name`.
    """
    values = np.array(datagrid.Values)

    columns = np.linspace(datagrid.MinX, datagrid.MinX + datagrid.Dx * (datagrid.Nx - 1), datagrid.Nx)
    rows = np.linspace(datagrid.MinY, datagrid.MinY + datagrid.Dy * (datagrid.Ny - 1), datagrid.Ny)

    df = pd.DataFrame(data=values, index=rows, columns=columns)
    df.index.name = datagrid.YLabel or "y"
    df.columns.name = datagrid.XLabel or "x"

    return df


SamplingType = TypeVar("SamplingType", int, str)


def standardize_sampling(sampling: SamplingType) -> SamplingType:
    """Standardizes the sampling patterns to either int or string (S_00x00) representation.

    Parameters
    ----------
    sampling: int | str
        The sampling pattern to use. Should be int or string. Accepts both S_00x00 and 00x00 string representation.

    Returns
    -------
    int | str
        The standardized sampling pattern that can be used for processing.

    Raises
    ------
    ValueError
        When `sampling` is a string that cannot be interpreted.
    TypeError
        When `sampling` is not int or string.
    """
    if isinstance(sampling, int):
        return sampling
    elif isinstance(sampling, str):
        res = re.search(r"\d+x\d+", sampling)
        if res:
            return "S_{}".format(res.group())
        else:
            raise ValueError('Cannot interpret sampling pattern "{}"'.format(sampling))
    else:
        raise TypeError("sampling should be int or string")
