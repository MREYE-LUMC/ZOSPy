"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("ColorRaysBy", "Patterns", "Reference", "ShowScales")

class ColorRaysBy(Enum):
    Fields = 0
    Waves = 1
    Config = 2
    Wavelength = 3

class Patterns(Enum):
    Square = 0
    Hexapolar = 1
    Dithered = 2

class Reference(Enum):
    ChiefRay = 0
    Centroid = 1
    Middle = 2
    Vertex = 3

class ShowScales(Enum):
    ScaleBar = 0
    Box = 1
    Cross = 2
    Circle = 3
