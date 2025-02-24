from __future__ import annotations

import functools
from collections.abc import Callable
from os import PathLike
from pathlib import Path
from sys import version_info
from typing import TypeVar

import zospy.api.config as _config


def _check_path(path: Path, *, directory_only: bool = False) -> bool:
    if directory_only and not path.is_dir():
        return _check_path(path.parent)

    return path.exists()


def abspath(path: PathLike | str, *, check_directory_only: bool = False) -> str:
    """Convert a path to an absolute path and check if it exists.

    Parameters
    ----------
    path : Path | str
        The path to be made absolute.
    check_directory_only : bool
        Whether to check only if directories exist. If set to `True`, parent directories are verified to exist, but
        files are not.

    Returns
    -------
    str
        The absolute path, converted to a string.

    Raises
    ------
    FileNotFoundError
        If `check_directory_only` is False and the path does not exist, or if `check_directory_only` is True and the
        parent directory does not exist.
    """
    # Behaviour of Path.resolve when the file does not exist is incorrect prior to Python 3.10
    absolute_path = Path(path).absolute() if version_info <= (3, 10) else Path(path).resolve()

    if _check_path(absolute_path, directory_only=check_directory_only):
        return str(absolute_path)
    else:
        raise FileNotFoundError(absolute_path)


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


Number = TypeVar("Number", int, float)


def atox(
    string: str,
    dtype: Callable[[str], Number] = float,
    decimal_point: str = ...,
    thousands_separator: str | None = ...,
) -> Number:
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
