"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("EncircledEnergyTypes", "ExtendedSourceTypes", "GeometricLineEdgeSpreadTypes", "ReferToTypes")

class EncircledEnergyTypes(Enum):
    Encircled = 1
    X_Only = 2
    Y_Only = 3
    Ensquared = 4

class ExtendedSourceTypes(Enum):
    Encircled = 1
    X_Only = 2
    Y_Only = 3
    Ensquared = 4
    X_Distrib = 5
    Y_Distrib = 6

class GeometricLineEdgeSpreadTypes(Enum):
    LineEdge = 1
    Line = 2
    Edge = 3

class ReferToTypes(Enum):
    ChiefRay = 0
    Centroid = 1
    Vertex = 2
