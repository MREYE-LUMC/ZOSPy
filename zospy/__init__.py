"""A Python package to communicate with Zemax OpticStudio through its API."""

__version__ = "1.1.2"

import logging

import zospy.api.config as config
from zospy import analyses, functions, solvers
from zospy.api import constants
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
