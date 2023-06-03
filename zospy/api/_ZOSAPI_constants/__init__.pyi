"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

from . import Analysis, Common, Editors, Preferences, SystemData, Tools, Wizards

__all__ = (
    "Analysis",
    "Common",
    "Editors",
    "Preferences",
    "SystemData",
    "Tools",
    "Wizards",
    "LensUpdateMode",
    "LicenseStatusType",
    "SessionModes",
    "STARUpdateMode",
    "SystemType",
    "UpdateStatus",
    "ZOSAPI_Mode",
)

class LensUpdateMode(Enum):
    None_ = 0
    EditorsOnly = 1
    AllWindows = 2

class LicenseStatusType(Enum):
    Unknown = 0
    KeyNotWorking = 1
    NewLicenseNeeded = 2
    StandardEdition = 3
    ProfessionalEdition = 4
    PremiumEdition = 5
    TooManyInstances = 6
    NotAuthorized = 7
    KeyNotFound = 8
    KeyExpired = 9
    Timeout = 10
    InstanceConflict = 11
    OpticsViewer = 12
    OpticStudioHPCEdition = 13
    EnterpriseEdition = 14

class SessionModes(Enum):
    FromPreferences = 0
    SessionOn = 1
    SessionOff = 2

class STARUpdateMode(Enum):
    Normal = 0
    Suspended = 1

class SystemType(Enum):
    Sequential = 0
    NonSequential = 1

class UpdateStatus(Enum):
    NotChecked = 0
    UpToDate = 1
    AvailableEligible = 2
    AvailableIneligible = 3
    CheckFailed = -2
    NotSupported = -1

class ZOSAPI_Mode(Enum):
    Server = 0
    Operand = 1
    Plugin = 2
    UserAnalysis = 3
    UserAnalysisSettings = 4
