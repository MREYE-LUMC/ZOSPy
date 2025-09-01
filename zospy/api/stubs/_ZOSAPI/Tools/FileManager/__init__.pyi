"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from zospy.api.stubs._ZOSAPI.Tools import ISystemTool
from zospy.api.stubs._ZOSAPI.Tools.FileManager import FileSource, IFile, KnownFolder

from zospy.api.stubs._ZOSAPI_constants.Tools.FileManager import (
    FileSource,
    KnownFolder,
    Operation,
)

__all__ = (
    "FileSource",
    "IConvertProjectToFileTool",
    "IFile",
    "KnownFolder",
    "Operation",
)

# FileSource is imported as constant

class IConvertProjectToFileTool(ISystemTool):
    @property
    def NumberOfFilesInUse(self) -> int: ...
    def GetFileInUse(self, fileIndex: int) -> IFile: ...
    def GetOutputDirectoryName(self) -> str: ...
    def SetFileOverwrite(self, fileIndex: int, allowOverwrite: bool) -> None: ...
    def SetFilesAllOverwrite(self) -> None: ...
    def SetFilesNoOverwrite(self) -> None: ...
    def SetOutputDirectoryName(self, directoryName: str) -> bool: ...

class IFile:
    @property
    def Name(self) -> str: ...
    @property
    def KnownFolder(self) -> KnownFolder: ...
    @property
    def RelativePath(self) -> str: ...
    @property
    def Source(self) -> FileSource: ...

# KnownFolder is imported as constant

# Operation is imported as constant
