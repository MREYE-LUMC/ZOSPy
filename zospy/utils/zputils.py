import re
import warnings
from collections.abc import MutableMapping

import numpy as np
import pandas as pd

from zospy.api import constants
from zospy.utils.clrutils import system_datetime_to_datetime


def flatten_dict(unflattend_dict, parent_key='', sep='.', keep_unflattend=False):
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

    flatdict = flatten_dict(dlltreedict, parent_key='', sep='.', keep_unflattend=True)
    flatlist = list(flatdict.keys())
    return flatlist


def series_index_by_value(series, value):
    """Returns the index or indices of a pandas series that correspond to a certain value.

    Parameters
    ----------
    series: pandas.Series
        A pandas Series object
    value
        The value for which the index should be returned

    Returns
    -------
    Any
        The index at which this value occurs. If the value occurs multiple times, a list of indices is returned. If the
        value is not in the series, None is returned.
    """
    ret = series[series == value].index
    if len(ret) == 1:
        return ret[0]
    elif len(ret) > 1:
        return ret
    else:
        return None


def unpack_cdata(data):
    warnings.warn('unpack_cdata is depricated and will be removed', DeprecationWarning)
    if data.ToString().split('.')[-1] == 'SerializedVectorData':
        return np.array(list(data.Data))
    elif data.ToString().split('.')[-1] == 'SerializedMatrixData':
        return np.array(list(data.Data)).reshape(data.Rows, data.Cols)
    else:
        raise ValueError('Cannot handle "{}" data'.format(data.__name__))


def unpack_dataseries(dataseries):
    """Unpacks a dataseries in a dataframe.

    Parameters
    ----------
    dataseries: Zemax OpticStudio DataSeries
        A Zemax Opticstudio Dataseries.

    Returns
    -------
    pd.DataFrame
        A DataFrame holding all data and labels
    """
    columns = pd.MultiIndex.from_product([[dataseries.Description], list(dataseries.SeriesLabels)],
                                         names=['Description', 'SeriesLabels'])
    index = np.array(list(dataseries.XData.Data))
    data = np.array(list(dataseries.YData.Data)).reshape(dataseries.YData.Rows, dataseries.YData.Cols)
    df = pd.DataFrame(columns=columns, index=index,
                      data=data)  # ToDo evaluate
    df.index.name = dataseries.XLabel
    return df


def unpack_datagrid(datagrid):
    """Unpacks an OpticStudio datagrid

    Parameters
    ----------
    datagrid: OpticStudio DataGrid
        An OpticStudio DataGrid

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the grid and the spacing on the rows and columns. The X- and YLabels are assigned to the
        df.columns.name and df.index.name
    """

    values = np.array(list(datagrid.Values))
    values = values.reshape(datagrid.Ny, datagrid.Nx)

    columns = np.linspace(datagrid.MinX, datagrid.MinX+datagrid.Dx*(datagrid.Nx-1), datagrid.Nx)
    rows = np.linspace(datagrid.MinY, datagrid.MinY+datagrid.Dy*(datagrid.Ny-1), datagrid.Ny)

    df = pd.DataFrame(data=values, index=rows[::-1], columns=columns)
    df.index.name = datagrid.YLabel if datagrid.YLabel is not None else 'y'
    df.columns.name = datagrid.XLabel if datagrid.XLabel is not None else 'x'

    return df


def proc_constant(constant_series, constant):
    """Processes a constant to ensure that an integer is returned.

    Parameters
    ----------
    constant_series: pandas.Series
        A series of zosapi constants
    constant: int or str
        The constant name for which the integer representation should be returned.

    Returns
    -------
    int
        The integer representation of the specified constant

    Raises
    ------
    TypeError
        When 'constant' is not int or string

    Examples
    --------
    proc_constant(zp.constants.Analysis.Settings.Mtf.MtfTypes, 'Modulation')
    """
    if isinstance(constant, (int, np.integer)):
        return constant
    elif isinstance(constant, str):
        return constant_series[constant]
    else:
        raise TypeError('constant should be an int or a string to return an integer')


def standardize_sampling(sampling):
    """Standardizes the sampling patterns to either int or string (S_00x00) representation

    Parameters
    ----------
    sampling: int or str
        The sampling pattern to use. Should be int or string. Accepts both S_00x00 and 00x00 string representation.

    Returns
    -------
    Union[int, str]
        The standardized sampling pattern that can be used for processing.

    Raises
    ------
    ValueError
        When 'sampling' is a string that cannot be interpreted
    TypeError
        When 'sampling' is not int or string
    """
    if isinstance(sampling, int):
        return sampling
    elif isinstance(sampling, str):
        res = re.search(r'\d+x\d+', sampling)
        if res:
            return 'S_{}'.format(res.group())
        else:
            raise ValueError('Cannot interpret sampling pattern "{}"'.format(sampling))
    else:
        raise TypeError('sampling should be int or string')


def analysis_set_field(analysis, value):
    """Sets the field value for a specific analysis

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.
    value: int or str
        The value to which the field should be set. Either int or str. Accepts only 'All' as string.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        When 'value' is not integer or string. When it is a string, it also raises an error when the string does not
        equal 'All'.

    """
    if isinstance(value, str) and value == 'All':
        analysis.Settings.Field.UseAllFields()
    elif isinstance(value, int):
        analysis.Settings.Field.SetFieldNumber(value)
    else:
        raise ValueError('Field value should be "All" or an integer')


def analysis_get_field(analysis):
    """Gets the wavelength value of a specific analysis.

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.

    Returns
    -------
    int | str
        Either the field number, or 'All' if field was set to 'All'.

    """
    fn = analysis.Settings.Field.GetFieldNumber()
    if fn == 0:
        return 'All'
    else:
        return fn


def analysis_set_wavelength(analysis, value):
    """Sets the wavelength value for a specific analysis

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.
    value: int or str
        The value to which the wavelength should be set. Either int or str. Accepts only 'All' as string.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        When 'value' is not integer or string. When it is a string, it also raises an error when the string does not
        equal 'All'.

    """
    if isinstance(value, str) and value == 'All':
        analysis.Settings.Wavelength.UseAllWavelengths()
    elif isinstance(value, int):
        analysis.Settings.Wavelength.SetWavelengthNumber(value)
    else:
        raise ValueError('Wavelength value should be "All" or an integer')


def analysis_get_wavelength(analysis):
    """Gets the wavelength value of a specific analysis.

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.

    Returns
    -------
    int | str
        Either the wavelength number, or 'All' if wavelength was set to 'All'.

    """
    wl = analysis.Settings.Wavelength.GetWavelengthNumber()
    if wl == 0:
        return 'All'
    else:
        return wl


def analysis_set_surface(analysis, value):
    """Sets the surface value for a specific analysis

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.
    value: int or str
        The value to which the surface should be set. Either int or str. Accepts only 'Image' or 'Objective' as string.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        When 'value' is not integer or string. When it is a string, it also raises an error when the string does not
        equal 'Image' or 'Objective'.

    """
    if isinstance(value, str) and value == 'Image':
        analysis.Settings.Surface.UseImageSurface()
    elif isinstance(value, str) and value == 'Objective':
        analysis.Settings.Surface.UseObjectiveSurface()
    elif isinstance(value, int):
        analysis.Settings.Surface.SetSurfaceNumber(value)
    else:
        raise ValueError('Surface value should be "Image", "Objective" or an integer')


def analysis_get_headerdata(analysis):
    """Obtains the headerdata from an OpticStudio analysis.

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.

    Returns
    -------
    list
        The headerdata.
    """
    return list(analysis.Results.HeaderData.Lines)


def analysis_get_messages(analysis):
    """Obtains the messages from an OpticStudio analysis.

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.

    Returns
    -------
    pd.DataFrame
        The messages in a dataframe. Each row has 1 pair of (ErrorCode, Message).
    """
    ret = pd.DataFrame(columns=['ErrorCode', 'Message'])

    for ii in range(analysis.Results.NumberOfMessages):
        message = analysis.Results.GetMessageAt(ii)

        err = constants.get_constantname_by_value(constants.Analysis.ErrorType, message.ErrorCode)

        ret.loc[len(ret), :] = [err, message.Text]

    return ret


def analysis_get_metadata(analysis):
    """Obtains the metadata from an OpticStudio analysis.

    Parameters
    ----------
    analysis: Any
        An OpticStudio Analysis.

    Returns
    -------
    pd.Series
        A series containing the MetaData including 'DateTime', 'FeatureDescription', 'LensFile' and 'LensTitle'.
    """
    ret = pd.Series(index=['DateTime',
                           'FeatureDescription',
                           'LensFile',
                           'LensTitle'],
                    data=[system_datetime_to_datetime(analysis.Results.MetaData.Date),
                          analysis.Results.MetaData.FeatureDescription,
                          analysis.Results.MetaData.LensFile,
                          analysis.Results.MetaData.LensTitle])
    return ret
