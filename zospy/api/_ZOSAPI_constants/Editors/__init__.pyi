"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations
from . import LDE, MCE, MFE, NCE, TDE

__all__ = (
    "LDE",
    "MCE",
    "MFE",
    "NCE",
    "TDE",
    "CellDataType",
    "DirectionOfRayTravel",
    "EditorType",
    "ReflectTransmitCode",
    "SampleSides",
    "Samplings",
    "SolveStatus",
    "SolveType",
)

class CellDataType:
    Integer: CellDataType = None
    Double: CellDataType = None
    String: CellDataType = None

class DirectionOfRayTravel:
    inward: DirectionOfRayTravel = None
    outward: DirectionOfRayTravel = None

class EditorType:
    LDE: EditorType = None
    NCE: EditorType = None
    MFE: EditorType = None
    TDE: EditorType = None
    MCE: EditorType = None

class ReflectTransmitCode:
    Success: ReflectTransmitCode = None
    NoReflectDataInFile: ReflectTransmitCode = None
    NoTransmitDataInFile: ReflectTransmitCode = None

class SampleSides:
    Front: SampleSides = None
    Back: SampleSides = None

class Samplings:
    FiveDegrees: Samplings = None
    TwoDegrees: Samplings = None
    OneDegree: Samplings = None

class SolveStatus:
    Success: SolveStatus = None
    InvalidSolveType: SolveStatus = None
    InvalidRow: SolveStatus = None
    InvalidColumn: SolveStatus = None
    PostSurfaceStopOnly: SolveStatus = None
    InvalidMacro: SolveStatus = None
    Failed: SolveStatus = None

class SolveType:
    None_: SolveType = None
    Fixed: SolveType = None
    Variable: SolveType = None
    SurfacePickup: SolveType = None
    ZPLMacro: SolveType = None
    MarginalRayAngle: SolveType = None
    MarginalRayHeight: SolveType = None
    ChiefRayAngle: SolveType = None
    MarginalRayNormal: SolveType = None
    ChiefRayNormal: SolveType = None
    Aplanatic: SolveType = None
    ElementPower: SolveType = None
    CocentricSurface: SolveType = None
    ConcentricSurface: SolveType = None
    CocentricRadius: SolveType = None
    ConcentricRadius: SolveType = None
    FNumber: SolveType = None
    ChiefRayHeight: SolveType = None
    EdgeThickness: SolveType = None
    OpticalPathDifference: SolveType = None
    Position: SolveType = None
    Compensator: SolveType = None
    CenterOfCurvature: SolveType = None
    PupilPosition: SolveType = None
    MaterialSubstitute: SolveType = None
    MaterialOffset: SolveType = None
    MaterialModel: SolveType = None
    Automatic: SolveType = None
    Maximum: SolveType = None
    PickupChiefRay: SolveType = None
    ObjectPickup: SolveType = None
    ConfigPickup: SolveType = None
    ThermalPickup: SolveType = None
    MarginPercent: SolveType = None
    CA_fill: SolveType = None
    DIA_fill: SolveType = None
    DuplicateSag: SolveType = None
    InvertSag: SolveType = None
    FieldPickup: SolveType = None
