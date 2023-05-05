"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = (
    "ApertureShapes",
    "ArrayMode",
    "BirefringentMode",
    "BirefringentReflections",
    "DetectorDataType",
    "DetectorShowAsType",
    "DiffractionSplitType",
    "DiffractiveFaceChoices",
    "DrawingResolutionType",
    "EfficiencySpectrumType",
    "EndCapOptions",
    "FaceIsType",
    "HologramTypes",
    "InterpolateChoices",
    "NCEIndexType",
    "ObjectColumn",
    "ObjectScatteringTypes",
    "ObjectType",
    "OrderChoices",
    "PixelAddressing",
    "PolarDetectorDataType",
    "RaysIgnoreObjectType",
    "RayTraceModes",
    "ScatterToType",
    "ShapeChoices",
    "SourceBulkScatterMode",
    "SourceColorMode",
    "SourceSamplingMethod",
    "UniformAngleChoices",
    "VolumePhysicsModelType",
)

class ApertureShapes(Enum):
    Annular = 0
    Elliptical = 1
    Rectangular = 2
    CyliderWithRectangular = 3

class ArrayMode(Enum):
    None_ = 0
    Rectangular = 1
    Circular = 2
    Hexapolar = 3
    Hexagonal = 4

class BirefringentMode(Enum):
    TraceOrdinayAndExtraordinary = 0
    TraceOrdinaryOnly = 1
    TraceExtraordinaryOnly = 2
    Waveplate = 3

class BirefringentReflections(Enum):
    TraceReflectedAndRefracted = 0
    TraceRefractedOnly = 1
    TraceReflectedOnly = 2

class DetectorDataType(Enum):
    Real = 0
    Imaginary = 1
    Amplitude = 2
    Power = 3

class DetectorShowAsType(Enum):
    GreyScaleFlux = 0
    InverseGreyScaleFlux = 1
    FalseColorFlux = 2
    InverseFalseColorFlux = 3
    GreyScaleIrradiance = 4
    InverseGreyScaleIrradiance = 5
    FalseColorIrradiance = 6
    InverseFalseColorIrradiance = 7

class DiffractionSplitType(Enum):
    DontSplitByOrder = 0
    SplitByTable = 1
    SplitByDLL = 2

class DiffractiveFaceChoices(Enum):
    FrontFace = 1
    BackFace = 2

class DrawingResolutionType(Enum):
    Standard = 0
    Medium = 1
    High = 2
    Presentation = 3
    Custom = 4

class EfficiencySpectrumType(Enum):
    QuantumYield = 0
    Excitation = 1

class EndCapOptions(Enum):
    None_ = 0
    First = 1
    Second = 2
    Both = 3

class FaceIsType(Enum):
    ObjectDefault = 0
    Reflective = 1
    Absorbing = 2

class HologramTypes(Enum):
    Type_1 = 1
    Type_2 = 2

class InterpolateChoices(Enum):
    Bicubic = 0
    Linear = 1

class NCEIndexType(Enum):
    Isotropic = 0
    Birefringent = 1
    GRIN = 2

class ObjectColumn(Enum):
    Comment = 1
    RefObject = 2
    InsideOf = 3
    XPosition = 4
    YPosition = 5
    ZPosition = 6
    TiltX = 7
    TiltY = 8
    TiltZ = 9
    Material = 10
    Par1 = 11
    Par2 = 12
    Par3 = 13
    Par4 = 14
    Par5 = 15
    Par6 = 16
    Par7 = 17
    Par8 = 18
    Par9 = 19
    Par10 = 20
    Par11 = 21
    Par12 = 22
    Par13 = 23
    Par14 = 24
    Par15 = 25
    Par16 = 26
    Par17 = 27
    Par18 = 28
    Par19 = 29
    Par20 = 30
    Par21 = 31
    Par22 = 32
    Par23 = 33
    Par24 = 34
    Par25 = 35
    Par26 = 36
    Par27 = 37
    Par28 = 38
    Par29 = 39
    Par30 = 40
    Par31 = 41
    Par32 = 42
    Par33 = 43
    Par34 = 44
    Par35 = 45
    Par36 = 46
    Par37 = 47
    Par38 = 48
    Par39 = 49
    Par40 = 50
    Par41 = 51
    Par42 = 52
    Par43 = 53
    Par44 = 54
    Par45 = 55
    Par46 = 56
    Par47 = 57
    Par48 = 58
    Par49 = 59
    Par50 = 60
    Par51 = 61
    Par52 = 62
    Par53 = 63
    Par54 = 64
    Par55 = 65
    Par56 = 66
    Par57 = 67
    Par58 = 68
    Par59 = 69
    Par60 = 70
    Par61 = 71
    Par62 = 72
    Par63 = 73
    Par64 = 74
    Par65 = 75
    Par66 = 76
    Par67 = 77
    Par68 = 78
    Par69 = 79
    Par70 = 80
    Par71 = 81
    Par72 = 82
    Par73 = 83
    Par74 = 84
    Par75 = 85
    Par76 = 86
    Par77 = 87
    Par78 = 88
    Par79 = 89
    Par80 = 90
    Par81 = 91
    Par82 = 92
    Par83 = 93
    Par84 = 94
    Par85 = 95
    Par86 = 96
    Par87 = 97
    Par88 = 98
    Par89 = 99
    Par90 = 100
    Par91 = 101
    Par92 = 102
    Par93 = 103
    Par94 = 104
    Par95 = 105
    Par96 = 106
    Par97 = 107
    Par98 = 108
    Par99 = 109
    Par100 = 110
    Par101 = 111
    Par102 = 112
    Par103 = 113
    Par104 = 114
    Par105 = 115
    Par106 = 116
    Par107 = 117
    Par108 = 118
    Par109 = 119
    Par110 = 120
    Par111 = 121
    Par112 = 122
    Par113 = 123
    Par114 = 124
    Par115 = 125
    Par116 = 126
    Par117 = 127
    Par118 = 128
    Par119 = 129
    Par120 = 130
    Par121 = 131
    Par122 = 132
    Par123 = 133
    Par124 = 134
    Par125 = 135
    Par126 = 136
    Par127 = 137
    Par128 = 138
    Par129 = 139
    Par130 = 140
    Par131 = 141
    Par132 = 142
    Par133 = 143
    Par134 = 144
    Par135 = 145
    Par136 = 146
    Par137 = 147
    Par138 = 148
    Par139 = 149
    Par140 = 150
    Par141 = 151
    Par142 = 152
    Par143 = 153
    Par144 = 154
    Par145 = 155
    Par146 = 156
    Par147 = 157
    Par148 = 158
    Par149 = 159
    Par150 = 160
    Par151 = 161
    Par152 = 162
    Par153 = 163
    Par154 = 164
    Par155 = 165
    Par156 = 166
    Par157 = 167
    Par158 = 168
    Par159 = 169
    Par160 = 170
    Par161 = 171
    Par162 = 172
    Par163 = 173
    Par164 = 174
    Par165 = 175
    Par166 = 176
    Par167 = 177
    Par168 = 178
    Par169 = 179
    Par170 = 180
    Par171 = 181
    Par172 = 182
    Par173 = 183
    Par174 = 184
    Par175 = 185
    Par176 = 186
    Par177 = 187
    Par178 = 188
    Par179 = 189
    Par180 = 190
    Par181 = 191
    Par182 = 192
    Par183 = 193
    Par184 = 194
    Par185 = 195
    Par186 = 196
    Par187 = 197
    Par188 = 198
    Par189 = 199
    Par190 = 200
    Par191 = 201
    Par192 = 202
    Par193 = 203
    Par194 = 204
    Par195 = 205
    Par196 = 206
    Par197 = 207
    Par198 = 208
    Par199 = 209
    Par200 = 210
    Par201 = 211
    Par202 = 212
    Par203 = 213
    Par204 = 214
    Par205 = 215
    Par206 = 216
    Par207 = 217
    Par208 = 218
    Par209 = 219
    Par210 = 220
    Par211 = 221
    Par212 = 222
    Par213 = 223
    Par214 = 224
    Par215 = 225
    Par216 = 226
    Par217 = 227
    Par218 = 228
    Par219 = 229
    Par220 = 230
    Par221 = 231
    Par222 = 232
    Par223 = 233
    Par224 = 234
    Par225 = 235
    Par226 = 236
    Par227 = 237
    Par228 = 238
    Par229 = 239
    Par230 = 240
    Par231 = 241
    Par232 = 242
    Par233 = 243
    Par234 = 244
    Par235 = 245
    Par236 = 246
    Par237 = 247
    Par238 = 248
    Par239 = 249
    Par240 = 250
    Par241 = 251
    Par242 = 252
    Par243 = 253
    Par244 = 254
    Par245 = 255
    Par246 = 256
    Par247 = 257
    Par248 = 258
    Par249 = 259
    Par250 = 260

class ObjectScatteringTypes(Enum):
    None_ = 0
    Lambertian = 1
    Gaussian = 2
    ABg = 3
    ABgFile = 4
    BSDF = 5
    ISScatterCatalog = 6
    User = 7

class ObjectType(Enum):
    AnnularAsphericLens = 0
    AnnularAxialLens = 1
    AnnularVolume = 2
    Annulus = 3
    Array = 4
    ArrayRing = 5
    AsphericSurface = 6
    AsphericSurface2 = 7
    AxiconSurface = 8
    BiconicLens = 9
    BiconicSurface = 10
    BiconicZernike = 11
    BiconicZernikeSurface = 12
    Binary1 = 13
    Binary2 = 14
    Binary2A = 15
    Boolean = 16
    BooleanCAD = 16
    CADAssemblyAutodeskInventor = 17
    CADAssemblyCreoParametric = 18
    CADAssemblySolidWorks = 19
    CADPartAutodeskInventor = 20
    CADPartCreoParametric = 21
    CADPartSolidWorks = 22
    CADPartSTEPIGESSAT = 23
    CADPartSTL = 24
    CADPartZPD = 25
    Cone = 26
    CPC = 27
    CPCRectangular = 28
    CylinderPipe = 29
    CylinderVolume = 30
    Cylinder2Pipe = 31
    Cylinder2Volume = 32
    DetectorColor = 33
    DetectorPolar = 34
    DetectorRectangle = 35
    DetectorSurface = 36
    DetectorVolume = 37
    DiffractionGrating = 38
    DualBEFSurface = 39
    Ellipse = 40
    EllipticalVolume = 41
    EvenAsphereLens = 42
    ExtendedOddAsphereLens = 43
    ExtendedPolynomialLens = 44
    ExtendedPolynomialSurface = 45
    Extruded = 46
    FacetedSurface = 47
    FreeformZ = 48
    Fresnel1 = 49
    Fresnel2 = 50
    GridSagLens = 51
    GridSagSurface = 52
    GridSagFrontBack = 53
    HexagonalLensletArray = 54
    HologramLens = 55
    HologramSurface = 56
    JonesMatrix = 57
    LensletArray1 = 58
    LensletArray2 = 59
    MEMS = 60
    NullObject = 61
    OddAsphereLens = 62
    ParaxialLens = 63
    PolygonObject = 64
    RayRotator = 65
    RectangularCorner = 66
    Rectangle = 67
    RectangularPipe = 68
    RectangularPipeGrating = 69
    RectangularRoof = 70
    RectangularTorusSurface = 71
    RectangularTorusVolume = 72
    RectangularVolume = 73
    RectangularVolumeGrating = 74
    ReverseRadianceDetector = 75
    ReverseRadianceTarget = 76
    Slide = 77
    SourceDiffractive = 78
    SourceDiode = 79
    SourceDLL = 80
    SourceEllipse = 81
    SourceEULUMDATFile = 82
    SourceFilament = 83
    SourceFile = 84
    SourceGaussian = 85
    SourceIESNAFile = 86
    SourceImported = 87
    SourceObject = 88
    SourcePoint = 89
    SourceRadial = 90
    SourceRay = 91
    SourceRectangle = 92
    SourceTube = 93
    SourceTwoAngle = 94
    SourceVolumeCylindrical = 95
    SourceVolumeElliptical = 96
    SourceVolumeRectangular = 97
    Sphere = 98
    StandardLens = 99
    StandardSurface = 100
    Swept = 101
    TabulatedFactedRadial = 102
    TabulatedFactedToroid = 103
    TabulatedFrenselRadial = 104
    ToroidalHologram = 105
    ToroidalLens = 106
    ToroidalSurface = 107
    ToroidalSurfaceOddASphere = 108
    TorusSurface = 109
    TorusVolume = 110
    TriangularCorner = 111
    Triangle = 112
    UserDefinedObject = 113
    WolterSurface = 114
    ZernikeSurface = 115
    BooleanNative = 116
    CompoundLens = 117
    QTypeAsphereSurface = 118
    OffAxisMirror = 119

class OrderChoices(Enum):
    Before = 0
    After = 1

class PixelAddressing(Enum):
    ByRow = 0
    ByColumn = 1
    Individually = 2

class PolarDetectorDataType(Enum):
    Power = 1
    PowerSolidAngle = 2
    Lumens = 3
    LumensSolidAngle = 4
    Cx = 5
    Cy = 6
    u_T = 7
    u_V = 8
    TriX = 9
    TriY = 10
    TriZ = 11

class RaysIgnoreObjectType(Enum):
    Never = 0
    Always = 1
    OnLaunch = 2

class RayTraceModes(Enum):
    Standard = 0
    Flat = 1
    Shaded = 2
    Kernel = 3

class ScatterToType(Enum):
    ScatterToList = 0
    ImportanceSampling = 1

class ShapeChoices(Enum):
    Rectangular = 0
    Elliptical = 1

class SourceBulkScatterMode(Enum):
    Many = 0
    Once = 1
    Never = 2

class SourceColorMode(Enum):
    SystemWavelengths = 0
    CIE1931Tristimulus = 1
    CIE1931Chromaticity = 2
    CIE1931RGB = 3
    UniformPowerSpectrum = 4
    D65White = 5
    ColorTemperature = 6
    BlackBodySpectrum = 7
    SpectrumFile = 8
    CIE1976 = 9

class SourceSamplingMethod(Enum):
    Random = 0
    Sobol = 1

class UniformAngleChoices(Enum):
    UniformIrradiance = 0
    UniformInAngleSpace = 1

class VolumePhysicsModelType(Enum):
    None_ = 0
    AngleScattering = 1
    DLLDefinedScattering = 2
    PhotoluminescenceModel = 3
