"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

from . import LDE, MCE, MFE, NCE, TDE

__all__ = (
    "LDE",
    "MCE",
    "MFE",
    "NCE",
    "TDE",
    "CellDataType",
    "EditorType",
    "ReflectTransmitCode",
    "SampleSides",
    "Samplings",
    "SolveStatus",
    "SolveType",
)

class CellDataType(Enum):
    Integer = 0
    Double = 1
    String = 2

class EditorType(Enum):
    LDE = 0
    NCE = 1
    MFE = 2
    TDE = 3
    MCE = 4

class ReflectTransmitCode(Enum):
    Success = 0
    NoReflectDataInFile = 1
    NoTransmitDataInFile = 2

class SampleSides(Enum):
    Front = 0
    Back = 1

class Samplings(Enum):
    FiveDegrees = 0
    TwoDegrees = 1
    OneDegree = 2

class SolveStatus(Enum):
    Success = 0
    InvalidSolveType = 1
    InvalidRow = 2
    InvalidColumn = 3
    PostSurfaceStopOnly = 4
    InvalidMacro = 5
    Failed = 10000

class SolveType(Enum):
    None_ = 0
    Fixed = 1
    Variable = 2
    SurfacePickup = 3
    ZPLMacro = 4
    MarginalRayAngle = 5
    MarginalRayHeight = 6
    ChiefRayAngle = 7
    MarginalRayNormal = 8
    ChiefRayNormal = 9
    Aplanatic = 10
    ElementPower = 11
    CocentricSurface = 12
    ConcentricSurface = 12
    CocentricRadius = 13
    ConcentricRadius = 13
    FNumber = 14
    ChiefRayHeight = 15
    EdgeThickness = 16
    OpticalPathDifference = 17
    Position = 18
    Compensator = 19
    CenterOfCurvature = 20
    PupilPosition = 21
    MaterialSubstitute = 22
    MaterialOffset = 23
    MaterialModel = 24
    Automatic = 25
    Maximum = 26
    PickupChiefRay = 27
    ObjectPickup = 28
    ConfigPickup = 29
    ThermalPickup = 30
    MarginPercent = 31
    CA_fill = 32
    DIA_fill = 33
    DuplicateSag = 34
    InvertSag = 35
    FieldPickup = 10000
