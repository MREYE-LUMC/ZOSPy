__version__ = '0.6.2'

import logging

import zospy.api.config as _config
from zospy import functions, analyses
from zospy.api import constants
from zospy.zpcore import ZOS

logging.getLogger(__name__).addHandler(logging.NullHandler())
