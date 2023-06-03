"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("DataType", "FoucaultShowAs", "KnifeType", "Types")

class DataType(Enum):
    Computed = 0
    Reference = 1
    Difference = 2

class FoucaultShowAs(Enum):
    Surface = 0
    Contour = 1
    GreyScale = 2
    InverseGreyScale = 3
    FalseColor = 4
    InverseFalseColor = 5
    X_CrossSection = 6
    Y_CrossSection = 7

class KnifeType(Enum):
    Horiz_Above = 0
    Horiz_Below = 1
    Vert_Right = 2
    Vert_Left = 3

class Types(Enum):
    Linear = 0
    Log_Minus_3 = 1
    Log_Minus_6 = 2
    Log_Minus_9 = 3
    Log_Minus_12 = 4
    Log_Minus_15 = 5
    Log_Minus_18 = 6
