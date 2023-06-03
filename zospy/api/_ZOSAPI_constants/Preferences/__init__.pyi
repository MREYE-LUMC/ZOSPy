"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("DateTimeType", "EncodingType", "LanguageType", "ShowLineAsType")

class DateTimeType(Enum):
    None_ = 0
    Date = 1
    DateTime = 2

class EncodingType(Enum):
    ANSI = 0
    Unicode = 1

class LanguageType(Enum):
    Chinese = 0
    English = 1
    Japanese = 4

class ShowLineAsType(Enum):
    TextAbove = 0
    FileName = 1
    ConfigurationNumber = 2
