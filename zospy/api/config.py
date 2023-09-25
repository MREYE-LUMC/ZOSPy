import locale

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

    loc = locale.getlocale()  # get and save current locale
    locale.setlocale(locale.LC_ALL, "")
    DECIMAL_POINT = locale.localeconv()["decimal_point"]
    THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
    locale.setlocale(locale.LC_ALL, loc)  # restore saved locale
