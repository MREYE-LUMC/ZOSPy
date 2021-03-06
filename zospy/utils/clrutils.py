from datetime import datetime as dt

import clr  # noqa
from System import Enum, Double  # noqa
from pandas import Series

DUMMY_DOUBLE = Double(0.)
DUMMY_ENUM = 0

def clr_get_available_assemblies(with_meta=True):
    """Gets all the avaialble assemblies from the Common Language Runtime.

    Parameters
    ----------
    with_meta: bool
        Defines if metadata should also be returned

    Returns
    -------
    list
        A list of all available assemblies
    """
    return list(clr.ListAssemblies(with_meta))


def system_get_enum_key_from_value(enum, value):
    """Gets the key corresponding to a certain value from a System.Enum instance.

    Parameters
    ----------
    enum: System.Enum
        The Enum instance.
    value
        The value for which the key should be returned

    Returns
    -------
    Any
        The corresponding key
    """
    return Enum.GetName(enum, value)


def system_get_enum_names(enum):
    """Gets all names from a System.Enum instance.

    Parameters
    ----------
    enum: System.Enum
        A Enum instance.

    Returns
    -------
    list
        A list containing the names of the Enum instance
    """
    return list(Enum.GetNames(enum))


def system_get_enum_values(enum):
    """Gets all values from a System.Enum instance.

    Parameters
    ----------
    enum: System.Enum
        A Enum instance.

    Returns
    -------
    list
        A list containing the values of the Enum instance
    """
    return list(Enum.GetValues(enum))


def series_from_system_enum(enum):
    """Converts a System.Enum into a pandas series

    Parameters
    ----------
    enum: System.Enum
        A Enum instance.

    Returns
    -------
    Series
        A Series containing the enum data.

    """
    label = enum.__name__
    names = system_get_enum_names(enum)
    values = system_get_enum_values(enum)

    return Series(data=values, index=names, name=label)


def system_datetime_to_datetime(sdt):
    """Converts a System.DateTime into a datetime.datetime instance.

    N.B.: As the System.DateTime does not contain info on the timezone, there might be an error if these do not match
    between the supplied DateTime instance and the current computer

    Parameters
    ----------
    sdt: System.DateTime
        An System.DateTime instance

    Returns
    -------
    datetime.datetime
        The pyton datetime instance
    """
    return dt(year=sdt.Year, month=sdt.Month, day=sdt.Day,
              hour=sdt.Hour, minute=sdt.Minute, second=sdt.Second,
              microsecond=sdt.Millisecond*1000)
