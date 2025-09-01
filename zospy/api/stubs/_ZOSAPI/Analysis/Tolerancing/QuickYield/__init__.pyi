"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from zospy.api.stubs._ZOSAPI.Analysis.Tolerancing.QuickYield import (
    XYSymmetricField,
    YSymmetricField,
)
from zospy.api.stubs._ZOSAPI.Analysis import IMessage

from zospy.api.stubs._ZOSAPI_constants.Analysis.Tolerancing.QuickYield import (
    XYSymmetricField,
    YSymmetricField,
)

__all__ = ("IAS_QYField", "XYSymmetricField", "YSymmetricField")

class IAS_QYField:
    @property
    def IsFieldUser(self) -> bool: ...
    @property
    def IsFieldSymmetricXY(self) -> bool: ...
    @property
    def IsFieldSymmetricY(self) -> bool: ...
    def GetFieldSymmetricXY(self) -> XYSymmetricField: ...
    def GetFieldSymmetricY(self) -> YSymmetricField: ...
    def GetFieldUser(self) -> int: ...
    def SetFieldSymmetricXY(self, field: XYSymmetricField) -> IMessage: ...
    def SetFieldSymmetricY(self, field: YSymmetricField) -> IMessage: ...
    def SetFieldUser(self, fieldNumber: int) -> IMessage: ...

# XYSymmetricField is imported as constant

# YSymmetricField is imported as constant
