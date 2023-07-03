from __future__ import annotations

import functools
from collections.abc import Callable

import zospy.api.config as _config


def rsetattr(obj, attr, val):
    """Wrapper for the setattr() function that handles nested strings.

    Parameters
    ----------
    obj
        The object from which the attribute is set
    attr
        The name of the attribute. Can be nested, e.g. 'aa.bb.cc'
    val
        The value to which the attribute is set

    Returns
    -------
        None
    """
    pre, _, post = attr.rpartition(".")
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, attr, *args):
    """Wrapper for the getattr() function that handles nested strings.

    Parameters
    ----------
    obj
        The object from which the attribute is obtained
    attr
        The name of the attribute. Can be nested, e.g. 'aa.bb.cc'
    *args
        [default,] The default return if the attribute is not found. If not supplied, AttributeError can be
        raised

    Returns
    -------
    attribute
        The attribute or the default return when not the attribute is not found

    Raises
    ------
    AttributeError
        When the attribute does not exist and no default is supplied in the *args
    """

    def _getattr(subobj, subattr, *subargs):
        return getattr(subobj, subattr, *subargs)

    return functools.reduce(lambda x, y: _getattr(x, y, *args), [obj] + attr.split("."))


def _delocalize(
    string: str,
    decimal_point: str = ...,
    thousands_separator: str | None = ...,
) -> str:
    """Delocalize a string as a normalized number.

    By default, the locale settings stored in zospy.api.config are used.

    Parameters
    ----------
    string: str
        The string that is to be converted.
    decimal_point: str
        The decimal point separator used in the string. Defaults to zospy.api.config.DECIMAL_POINT.
    thousands_separator: str | None
        The thousands separator used in the string. Defaults to zospy.api.config.THOUSANDS_SEPARATOR.

    Returns
    -------
    str
        The delocalized string.
    """
    # Get rid of the thousands grouping
    thousands_separator = _config.THOUSANDS_SEPARATOR if thousands_separator is ... else thousands_separator
    decimal_point = _config.DECIMAL_POINT if decimal_point is ... else decimal_point

    if thousands_separator:
        string = string.replace(thousands_separator, "")

    # Replace the decimal point with a dot
    if decimal_point:
        string = string.replace(decimal_point, ".")

    return string


def atox(
    string: str,
    dtype: Callable[[str], int | float] = float,
    decimal_point: str = ...,
    thousands_separator: str | None = ...,
) -> int | float:
    """Parses a string as a number format.

    By default, the locale settings stored in zospy.api.config are used to delocalize the string.

    Parameters
    ----------
    string: str
        The string that is to be converted.
    dtype: Callable[[str], int | float]
        The function used to convert the delocalized string into a number.
    decimal_point: str
        The decimal point separator used in the string. Defaults to zospy.api.config.DECIMAL_POINT.
    thousands_separator: str | None
        The thousands separator used in the string. Defaults to zospy.api.config.THOUSANDS_SEPARATOR.

    Returns
    -------
    str
        The delocalized string.
    """
    return dtype(_delocalize(string, decimal_point=decimal_point, thousands_separator=thousands_separator))


def xtoa(
    number: float | int,
    decimal_point: str = ...,
    thousands_separator: str | None = ...,
) -> str:
    """Localizes a number back to a string suing the locale settings.

    By default, the locale settings stored in zospy.api.config are used.

    Parameters
    ----------
    number: int | float
        The number that is to be converted.
    decimal_point: str
        The decimal point separator used in the string. Defaults to zospy.api.config.DECIMAL_POINT.
    thousands_separator: str | None
        The thousands separator used in the string. Defaults to zospy.api.config.THOUSANDS_SEPARATOR.

    Returns
    -------
    str
        The localized string representation of the number.
    """
    thousands_separator = _config.THOUSANDS_SEPARATOR if thousands_separator is ... else thousands_separator
    decimal_point = _config.DECIMAL_POINT if decimal_point is ... else decimal_point

    if isinstance(number, int):
        if thousands_separator:
            string = format(number, ",").replace(",", thousands_separator)
        else:
            string = str(number)
        return string

    if isinstance(number, float):
        if not decimal_point:
            raise ValueError("Converting float to string requires decimal point to be known")

        if thousands_separator:
            string = format(number, ",")
        else:
            string = str(number)

        # swap , and . simultaneously for thousands_separator and decimal_point
        string = string.translate(str.maketrans({",": thousands_separator, ".": decimal_point}))

        return string
