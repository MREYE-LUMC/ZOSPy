"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Analysis.Settings import IAS_

__all__ = ("IAS_PathAnalysis", "PathAnalysisSortType")

class IAS_PathAnalysis(IAS_):
    @property
    def RayDatabaseFile(self) -> str: ...
    @RayDatabaseFile.setter
    def RayDatabaseFile(self, value: str) -> None: ...
    @property
    def AvailableRayDatabaseFiles(self) -> list[str]: ...
    @property
    def FirstRay(self) -> int: ...
    @FirstRay.setter
    def FirstRay(self, value: int) -> None: ...
    @property
    def LastRay(self) -> int: ...
    @LastRay.setter
    def LastRay(self, value: int) -> None: ...
    @property
    def FilterString(self) -> str: ...
    @FilterString.setter
    def FilterString(self, value: str) -> None: ...
    @property
    def GeneratePathFilters(self) -> bool: ...
    @GeneratePathFilters.setter
    def GeneratePathFilters(self, value: bool) -> None: ...
    @property
    def RelativeMinimumFlux(self) -> float: ...
    @RelativeMinimumFlux.setter
    def RelativeMinimumFlux(self, value: float) -> None: ...
    @property
    def SortBy(self) -> PathAnalysisSortType: ...
    @SortBy.setter
    def SortBy(self, value: PathAnalysisSortType) -> None: ...

class PathAnalysisSortType:
    TotalEndingFlux = 0
    NumberOfObjectsStruck = 1
    NumberOfBranches = 2
    LastObjectStruck = 3
    NumberOfUniqueObjectsStruct = 4
    AverageOpticalPathLength = 5
    NumberOfDiffractionEvents = 6
