"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

from . import General, LMx, Optimization, RayTrace, Tolerancing

__all__ = (
    "General",
    "LMx",
    "Optimization",
    "RayTrace",
    "Tolerancing",
    "CriticalRayType",
    "HPCEnvironments",
    "HPCNodeSize",
    "HPCRunState",
    "MaterialFormulas",
    "MaterialStatuses",
    "RayPatternOption",
    "RunStatus",
    "VertexOrder",
)

class CriticalRayType(Enum):
    Chief = 0
    Marginal = 1
    Grid = 2
    Ring = 3
    Y_Fan = 4
    X_Fan = 5
    XY_Fan = 6
    List = 7

class HPCEnvironments(Enum):
    OnPremise = 0
    AWSKubernetes = 1
    AzureKubernetes = 2

class HPCNodeSize(Enum):
    Default = 0
    Tiny = 1
    Small = 2
    Medium = 3
    Large = 4
    XLarge = 5

class HPCRunState(Enum):
    NotRunning = 0
    Initializing = 1
    ClusterAllocating = 2
    UploadingData = 3
    Queued = 4
    RunStarting = 5
    WaitingForResults = 6
    Complete = 7

class MaterialFormulas(Enum):
    Schott = 1
    Sellmeier1 = 2
    Herzberger = 3
    Sellmeier2 = 4
    Conrady = 5
    Sellmeier3 = 6
    Handbook1 = 7
    Handbook2 = 8
    Sellmeier4 = 9
    Extended = 10
    Sellmeier5 = 11
    Extended2 = 12
    Extended3 = 13

class MaterialStatuses(Enum):
    Standard = 0
    Preferred = 1
    Obsolete = 2
    Special = 3
    Melt = 4

class RayPatternOption(Enum):
    XyFan = 0
    XFan = 1
    YFan = 2
    ChiefAndRing = 3
    List = 4
    Grid = 6
    ChiefAndMarginals = 8

class RunStatus(Enum):
    Completed = 0
    FailedToStart = 1
    TimedOut = 2
    InvalidTimeout = 3

class VertexOrder(Enum):
    First = 0
    Second = 1
    Third = 2
