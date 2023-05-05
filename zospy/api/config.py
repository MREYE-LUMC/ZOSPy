import locale

# Get decimal point used by ZOS
loc = locale.getlocale()  # get and save current locale
locale.setlocale(locale.LC_ALL, "")
DECIMAL = locale.localeconv()["decimal_point"]
locale.setlocale(locale.LC_ALL, loc)  # restore saved locale
