"""Utility functions for working with Python types."""

from __future__ import annotations

from operator import attrgetter
from pathlib import Path
from sys import version_info
from typing import TYPE_CHECKING, TypeVar

import zospy.api.config as _config

if TYPE_CHECKING:
    from collections.abc import Callable
    from os import PathLike


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
    raise FileNotFoundError(absolute_path)


def attrsetter(obj, attr, val):
    """Set an attribute of an object.

    Parameters
    ----------
    obj
        The object from which the attribute is set
    attr
        The name of the attribute
    val
        The value to which the attribute is set

    Returns
    -------
        None
    """
    pre, _, post = attr.rpartition(".")
    return setattr(attrgetter(pre)(obj) if pre else obj, post, val)


def _delocalize(
    string: str,
    decimal_point: str = ...,
    thousands_separator: str | None = ...,
) -> str:
    """Delocalize a string as a normalized number.

    By default, the locale settings stored in zospy.api.config are used.

    Parameters
    ----------
    string : str
        The string that is to be converted.
    decimal_point : str
        The decimal point separator used in the string. Defaults to zospy.api.config.DECIMAL_POINT.
    thousands_separator : str | None
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
    """Parse a string to a numeric type.

    By default, the locale settings stored in zospy.api.config are used to delocalize the string.

    Parameters
    ----------
    string : str
        The string that is to be converted.
    dtype : Callable[[str], int | float]
        The function used to convert the delocalized string into a number.
    decimal_point : str
        The decimal point separator used in the string. Defaults to zospy.api.config.DECIMAL_POINT.
    thousands_separator : str | None
        The thousands separator used in the string. Defaults to zospy.api.config.THOUSANDS_SEPARATOR.

    Returns
    -------
    str
        The delocalized string.
    """
    return dtype(_delocalize(string, decimal_point=decimal_point, thousands_separator=thousands_separator))


def xtoa(
    number: float,
    decimal_point: str = ...,
    thousands_separator: str | None = ...,
) -> str:
    """Localize a number back to a string using the locale settings.

    By default, the locale settings stored in zospy.api.config are used.

    Parameters
    ----------
    number : int | float
        The number that is to be converted.
    decimal_point : str
        The decimal point separator used in the string. Defaults to zospy.api.config.DECIMAL_POINT.
    thousands_separator : str | None
        The thousands separator used in the string. Defaults to zospy.api.config.THOUSANDS_SEPARATOR.

    Returns
    -------
    str
        The localized string representation of the number.
    """
    thousands_separator = _config.THOUSANDS_SEPARATOR if thousands_separator is ... else thousands_separator
    decimal_point = _config.DECIMAL_POINT if decimal_point is ... else decimal_point

    if isinstance(number, int):
        return format(number, ",").replace(",", thousands_separator) if thousands_separator else str(number)

    if isinstance(number, float):
        if not decimal_point:
            raise ValueError("Converting float to string requires decimal point to be known")

        string = format(number, ",") if thousands_separator else str(number)

        # swap , and . simultaneously for thousands_separator and decimal_point
        return string.translate(str.maketrans({",": thousands_separator, ".": decimal_point}))

    raise TypeError(f"Expected int or float, got {type(number).__name__}")
