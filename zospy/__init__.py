"""Communicate with OpticStudio through the ZOS-API."""

import logging
from importlib.metadata import version

from zospy import analyses, functions, solvers
from zospy.api import config, constants
from zospy.zpcore import ZOS

__version__ = version("zospy")

__all__ = (
    "analyses",
    "constants",
    "functions",
    "solvers",
    "ZOS",
)

config.set_decimal_point_and_thousands_separator()
logging.getLogger(__name__).addHandler(logging.NullHandler())
