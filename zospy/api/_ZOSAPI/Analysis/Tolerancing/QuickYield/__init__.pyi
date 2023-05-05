"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis import IMessage

__all__ = ("IAS_QYField", "IAS_QYField", "XYSymmetricField", "YSymmetricField")

class IAS_QYField:
    @property
    def IsFieldSymmetricXY(self) -> bool: ...
    @property
    def IsFieldSymmetricY(self) -> bool: ...
    @property
    def IsFieldUser(self) -> bool: ...
    def GetFieldSymmetricXY(self) -> XYSymmetricField: ...
    def GetFieldSymmetricY(self) -> YSymmetricField: ...
    def GetFieldUser(self) -> int: ...
    def SetFieldSymmetricXY(self, field: XYSymmetricField) -> IMessage: ...
    def SetFieldSymmetricY(self, field: YSymmetricField) -> IMessage: ...
    def SetFieldUser(self, fieldNumber: int) -> IMessage: ...

class XYSymmetricField:
    All = 0
    Zero = 1
    YPositive70Percent = 2
    YNegative70Percent = 3
    YPositive100Percent = 4
    YNegative100Percent = 5
    XPositive70Percent = 6
    XNegative70Percent = 7
    XPositive100Percent = 8
    XNegative100Percent = 9

class YSymmetricField:
    All = 0
    Zero = 1
    Positive70Percent = 2
    Negative70Percent = 3
    Positive100Percent = 4
    Negative100Percent = 5
