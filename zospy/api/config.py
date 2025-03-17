"""Configuration module for ZOSPy.

Retrieves and stores the number format used by Zemax OpticStudio.
These values are used to parse analysis result text files.
"""

import locale
import logging

logger = logging.getLogger(__name__)

DECIMAL_POINT = locale.localeconv()["decimal_point"]
THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]


def set_decimal_point_and_thousands_separator() -> None:
    """Set `DECIMAL_POINT` and `THOUSHANDS_SEPARATOR` based on the system locale.

    These values are used to parse analysis result text files.

    Returns
    -------
    None

    Warnings
    --------
    This function is not thread-safe due to the use of `locale.setlocale`.
    Normal use of ZOSPy is unlikely to cause problems, but creating new threads prior to
    importing ZOSPy may cause issues. See also https://docs.python.org/3/library/locale.html#locale.setlocale
    for more information.
    """
    global DECIMAL_POINT  # noqa: PLW0603
    global THOUSANDS_SEPARATOR  # noqa: PLW0603

    old_locale = locale.setlocale(locale.LC_NUMERIC)  # get and save current numeric locale

    try:
        locale.setlocale(locale.LC_NUMERIC, "")

        DECIMAL_POINT = locale.localeconv()["decimal_point"]
        THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
    except locale.Error:
        logger.error("Failed to determine decimal point and thousands separator", exc_info=True)  # noqa: G201
    finally:
        locale.setlocale(locale.LC_NUMERIC, old_locale)  # restore saved locale
