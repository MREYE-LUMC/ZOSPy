import locale
import os

# Do not run this code when building documentation
if not os.environ.get("READTHEDOCS"):
    # Get decimal point used by ZOS
    loc = locale.getlocale()  # get and save current locale
    locale.setlocale(locale.LC_ALL, "")
    DECIMAL_POINT = locale.localeconv()["decimal_point"]
    THOUSANDS_SEPARATOR = locale.localeconv()["thousands_sep"]
    locale.setlocale(locale.LC_ALL, loc)  # restore saved locale
