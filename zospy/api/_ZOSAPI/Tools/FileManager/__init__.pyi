"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

__all__ = ("FileSource", "IFile", "KnownFolder", "Operation")

class FileSource:
    Project = 0
    Root = 1
    Unknown = -1

class IFile:
    @property
    def Name(self) -> str: ...
    @property
    def KnownFolder(self) -> KnownFolder: ...
    @property
    def RelativePath(self) -> str: ...
    @property
    def Source(self) -> FileSource: ...

class KnownFolder:
    Project = 0
    ABgData = 1
    BlackBoxes = 2
    Coatings = 3
    Configs = 4
    DllBulkScatter = 5
    DllDiffractive = 6
    DllGradientIndex = 7
    DllObjects = 8
    DllPhysicalOptics = 9
    DllSources = 10
    DllSurfaceScatter = 11
    DllSurfaces = 12
    Extend = 13
    GlassCat = 14
    ImaFiles = 15
    Macros = 16
    MeritFunction = 17
    Miscellaneous = 18
    ObjectsApertures = 19
    ObjectsCadFiles = 20
    ObjectsCreoParametricFiles = 21
    ObjectsGridFiles = 22
    ObjectsInventorFiles = 23
    ObjectsPartDesignerObjects = 24
    ObjectsPhosphorsAndFluorescenceFiles = 25
    ObjectsPolygonObjects = 26
    ObjectsStopFiles = 27
    ObjectsSolidWorksFiles = 28
    ObjectsSourcesEulumdat = 29
    ObjectsSourcesIesna = 30
    ObjectsSourcesRadiantSourceModelFiles = 31
    ObjectsSourcesSourceFiles = 32
    ObjectsSourcesSpectrumFiles = 33
    ObjectsTabulatedObjects = 34
    PopBeamFiles = 35
    Profiles = 36
    ScatterData = 37
    Tolerance = 38
    Udo = 39
    ZosApiExtensions = 40
    ZosApiOperands = 41
    ZosApiUserAnalysis = 42
    DllBirefringence = 43
    Unknown = -1

class Operation:
    # None = 0
    GetFilesInUse = 1
    GetAdditionalFiles = 2
