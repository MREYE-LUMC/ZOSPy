"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations
from . import FileManager, General, Layouts, Optimization, OptimizationTools, RayTrace, Tolerancing

__all__ = (
    "FileManager",
    "General",
    "Layouts",
    "Optimization",
    "OptimizationTools",
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

class CriticalRayType:
    Chief: CriticalRayType = None
    Marginal: CriticalRayType = None
    Grid: CriticalRayType = None
    Ring: CriticalRayType = None
    Y_Fan: CriticalRayType = None
    X_Fan: CriticalRayType = None
    XY_Fan: CriticalRayType = None
    List: CriticalRayType = None

class HPCEnvironments:
    OnPremise: HPCEnvironments = None
    AWSKubernetes: HPCEnvironments = None
    AzureKubernetes: HPCEnvironments = None

class HPCNodeSize:
    Default: HPCNodeSize = None
    Tiny: HPCNodeSize = None
    Small: HPCNodeSize = None
    Medium: HPCNodeSize = None
    Large: HPCNodeSize = None
    XLarge: HPCNodeSize = None

class HPCRunState:
    NotRunning: HPCRunState = None
    Initializing: HPCRunState = None
    ClusterAllocating: HPCRunState = None
    UploadingData: HPCRunState = None
    Queued: HPCRunState = None
    RunStarting: HPCRunState = None
    WaitingForResults: HPCRunState = None
    Complete: HPCRunState = None

class MaterialFormulas:
    Schott: MaterialFormulas = None
    Sellmeier1: MaterialFormulas = None
    Herzberger: MaterialFormulas = None
    Sellmeier2: MaterialFormulas = None
    Conrady: MaterialFormulas = None
    Sellmeier3: MaterialFormulas = None
    Handbook1: MaterialFormulas = None
    Handbook2: MaterialFormulas = None
    Sellmeier4: MaterialFormulas = None
    Extended: MaterialFormulas = None
    Sellmeier5: MaterialFormulas = None
    Extended2: MaterialFormulas = None
    Extended3: MaterialFormulas = None

class MaterialStatuses:
    Standard: MaterialStatuses = None
    Preferred: MaterialStatuses = None
    Obsolete: MaterialStatuses = None
    Special: MaterialStatuses = None
    Melt: MaterialStatuses = None

class RayPatternOption:
    XyFan: RayPatternOption = None
    XFan: RayPatternOption = None
    YFan: RayPatternOption = None
    ChiefAndRing: RayPatternOption = None
    List: RayPatternOption = None
    Grid: RayPatternOption = None
    ChiefAndMarginals: RayPatternOption = None

class RunStatus:
    Completed: RunStatus = None
    FailedToStart: RunStatus = None
    TimedOut: RunStatus = None
    InvalidTimeout: RunStatus = None

class VertexOrder:
    First: VertexOrder = None
    Second: VertexOrder = None
    Third: VertexOrder = None
