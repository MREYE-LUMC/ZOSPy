import locale
import logging

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
    global DECIMAL_POINT
    global THOUSANDS_SEPARATOR

    logger = logging.getLogger(__name__)
    loc = locale.getlocale()  # get and save current locale
    locale.setlocale(locale.LC_ALL, "")
    DECIMAL_POINT = locale.localeconv()["decimal_point"]
    THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
    try:
        locale.setlocale(locale.LC_ALL, loc)  # restore saved locale
    except Exception as err:
        # if setlocale fails here there is no sane action to resolve this
        # leave the system with locale.setlocale(locale.LC_ALL, "")
        logger.warning('cannot set locale to "{}" leaving interpreter at LC_ALL'.format(str(loc)))
