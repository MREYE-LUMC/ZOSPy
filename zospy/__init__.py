"""A Python package to communicate with Zemax OpticStudio through its API."""

__version__ = "1.0.0"

import logging

import zospy.api.config as _config
from zospy import analyses, functions, solvers
from zospy.api import constants
from zospy.zpcore import ZOS

__all__ = (
    "_config",
    "analyses",
    "constants",
    "functions",
    "solvers",
    "ZOS",
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
