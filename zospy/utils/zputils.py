"""Utility functions for ZOSPy."""

from __future__ import annotations

import re
from collections.abc import MutableMapping
from typing import Literal, TypeVar

import numpy as np
import pandas as pd

from zospy.api import _ZOSAPI
from zospy.api import config as _config


def flatten_dict(unflattened_dict, parent_key="", sep=".", *, keep_unflattened=False):
    """Flatten a nested dictionary to a single-level dictionary.

    Parameters
    ----------
    unflattened_dict : dict or MutableMapping
        A dictionary with nested dictionaries
    parent_key : str
        A key to which the flattened keys are added. Mainly present to support flatting of subdicts, should be '' in
        most primary calls.. Defaults to ''.
    sep : str
        The separator used for the flat items. Defaults to '.'
    keep_unflattened : bool
        Whether the keys, value pairs of nested dicts or MutableMappings should remain present in the output or not.
        Defaults to False

    Returns
    -------
    dict
        A dictionary with one (flattened) key for a value.
    """
    items = []
    for key, value in unflattened_dict.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            if keep_unflattened:
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
    dlltreedict : dict
        A dictionary with nested dictionaries

    Returns
    -------
    list:
        A list with the items of the nested dictionaries.
    """
    flatdict = flatten_dict(dlltreedict, parent_key="", sep=".", keep_unflattened=True)
    return list(flatdict.keys())


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
    df = pd.DataFrame(columns=columns, index=index, data=data)  # TODO evaluate
    df.index.name = dataseries.XLabel

    return df


def unpack_datagrid(
    datagrid: _ZOSAPI.Analysis.Data.IAR_DataGrid,
    minx: float | None = None,
    miny: float | None = None,
    cell_origin: Literal["bottom_left", "center"] = "bottom_left",
    label_rounding: int | None = 10,
) -> pd.DataFrame:
    """Unpack an OpticStudio datagrid to a Pandas DataFrame.

    Parameters
    ----------
    datagrid : ZOSAPI.Analysis.Data.IAR_DataGrid
        OpticStudio DataGrid object.
    minx : float, optional
        The MinX coordinate to be used when unpacking the datagrid.
    miny : float, optional
        The MinY coordinate to be used when unpacking the datagrid.
    cell_origin : Literal["bottom_left", "center"]
        Defines how minx and miny are handled to determine coordinates. Either 'bottom_left' indicating that they are
        defining the bottom left of the grd cell, or 'center', indicating that they provide the center of the grid cell.
        Defaults to 'bottom_left'.
    label_rounding : int, optional
        Defines the numbers of decimals to which the column and index labels are rounded, to fix floating point errors.
        If set to None, no rounding is applied. Defaults to 10.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the grid and the spacing on the rows and columns.
        The X- and YLabels are assigned to `df.columns.name` and `df.index.name`.
    """
    values = np.array(datagrid.Values)

    minx = datagrid.MinX if minx is None else minx
    miny = datagrid.MinY if miny is None else miny

    if cell_origin == "bottom_left":  # datagrid.MinX and .MinY point to edge of pixel, shift by half Dx and Dy
        minx += 0.5 * datagrid.Dx
        miny += 0.5 * datagrid.Dy
    elif cell_origin == "center":
        pass  # minx and miny remain equal
    else:
        raise ValueError(f"Cannot process the cell origin '{cell_origin}'")

    columns = np.linspace(minx, minx + datagrid.Dx * (datagrid.Nx - 1), datagrid.Nx)
    rows = np.linspace(miny, miny + datagrid.Dy * (datagrid.Ny - 1), datagrid.Ny)

    if label_rounding is not None:
        columns = columns.round(label_rounding)
        rows = rows.round(label_rounding)

    df = pd.DataFrame(data=values, index=rows, columns=columns)
    df.index.name = datagrid.YLabel or "y"
    df.columns.name = datagrid.XLabel or "x"

    return df


SamplingType = TypeVar("SamplingType", int, str)


def standardize_sampling(sampling: SamplingType, prefix: str = "S") -> SamplingType:
    """Standardizes the sampling patterns to either int or string (S_00x00) representation.

    Parameters
    ----------
    sampling : int | str
        The sampling pattern to use. Should be int or string. Accepts both S_00x00 and 00x00 string representation.
    prefix : str
        The prefix to use for the sampling pattern. Defaults to 'S'.

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
    if isinstance(sampling, str):
        res = re.match(rf"^(?:{re.escape(prefix)}_)?(?P<size>\d+)x(?P=size)$", sampling)
        if res:
            size = res.group("size")
            return f"{prefix}_{size}x{size}"
        raise ValueError(f'Cannot interpret sampling pattern "{sampling}"')
    raise TypeError("sampling should be int or string")


# TODO: Remove in ZOSPy 2.0.0
def _get_number_field(name: str, text: str) -> str:
    return re.search(
        rf"{re.escape(name)}\s*:\s*([-+]?(\d+({re.escape(_config.DECIMAL_POINT)}\d*)?|{re.escape(_config.DECIMAL_POINT)}\d+)(?:[Ee][-+]?\d+)?)",
        text,
    ).group(1)
