"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations
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

class LensUpdateMode:
    None_: LensUpdateMode = None
    EditorsOnly: LensUpdateMode = None
    AllWindows: LensUpdateMode = None

class LicenseStatusType:
    Unknown: LicenseStatusType = None
    KeyNotWorking: LicenseStatusType = None
    NewLicenseNeeded: LicenseStatusType = None
    StandardEdition: LicenseStatusType = None
    ProfessionalEdition: LicenseStatusType = None
    PremiumEdition: LicenseStatusType = None
    TooManyInstances: LicenseStatusType = None
    NotAuthorized: LicenseStatusType = None
    KeyNotFound: LicenseStatusType = None
    KeyExpired: LicenseStatusType = None
    Timeout: LicenseStatusType = None
    InstanceConflict: LicenseStatusType = None
    OpticsViewer: LicenseStatusType = None
    OpticStudioHPCEdition: LicenseStatusType = None
    EnterpriseEdition: LicenseStatusType = None
    StudentEdition: LicenseStatusType = None

class SessionModes:
    FromPreferences: SessionModes = None
    SessionOn: SessionModes = None
    SessionOff: SessionModes = None

class STARUpdateMode:
    Normal: STARUpdateMode = None
    Suspended: STARUpdateMode = None

class SystemType:
    Sequential: SystemType = None
    NonSequential: SystemType = None

class UpdateStatus:
    NotChecked: UpdateStatus = None
    UpToDate: UpdateStatus = None
    AvailableEligible: UpdateStatus = None
    AvailableIneligible: UpdateStatus = None
    CheckFailed: UpdateStatus = None
    NotSupported: UpdateStatus = None

class ZOSAPI_Mode:
    Server: ZOSAPI_Mode = None
    Operand: ZOSAPI_Mode = None
    Plugin: ZOSAPI_Mode = None
    UserAnalysis: ZOSAPI_Mode = None
    UserAnalysisSettings: ZOSAPI_Mode = None
