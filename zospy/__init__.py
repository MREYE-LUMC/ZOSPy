"""Communicate with OpticStudio through the ZOS-API."""

from __future__ import annotations

import logging
from importlib.metadata import version

from zospy import analyses, functions, solvers
from zospy.api import config, constants
from zospy.zpcore import ZOS

__version__ = version("zospy")

__all__ = (
    "ZOS",
    "analyses",
    "constants",
    "functions",
    "solvers",
)

config.set_decimal_point_and_thousands_separator()
logging.getLogger(__name__).addHandler(logging.NullHandler())
