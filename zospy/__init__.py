"""Communicate with OpticStudio through the ZOS-API."""

__version__ = "2.0.0"

import logging

from zospy import analyses, functions, solvers
from zospy.api import config, constants
from zospy.zpcore import ZOS

config.set_decimal_point_and_thousands_separator()

__all__ = (
    "analyses",
    "constants",
    "functions",
    "solvers",
    "ZOS",
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
