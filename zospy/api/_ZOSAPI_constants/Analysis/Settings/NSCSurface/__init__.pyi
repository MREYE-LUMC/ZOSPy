"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("NSCSagRemoveOptions", "NSCSagShowAs")

class NSCSagRemoveOptions(Enum):
    None_ = 0
    BaseROC = 1
    BestFitSphere = 2
    AverageSag = 3
    MinimumSag = 4

class NSCSagShowAs(Enum):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    X_CrossSection = 6
    Y_CrossSection = 7
