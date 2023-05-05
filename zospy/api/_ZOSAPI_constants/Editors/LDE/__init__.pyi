"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = (
    "CoatingStatusType",
    "ConversionOrder",
    "CoordinateConversionResult",
    "CoordinateReturnType",
    "InterpolationMethod",
    "NodesDataType",
    "PilotRadiusMode",
    "PointCloudFileFormat",
    "PupilApodizationType",
    "QTypes",
    "STARDeformationOption",
    "SubstrateType",
    "SurfaceApertureTypes",
    "SurfaceColumn",
    "SurfaceEdgeDraw",
    "SurfaceScatteringTypes",
    "SurfaceType",
    "TiltDecenterOrderType",
    "TiltDecenterPickupType",
    "TiltType",
    "XYSampling",
)

class CoatingStatusType(Enum):
    Fixed = 0
    Variable = 1
    Pickup = 2

class ConversionOrder(Enum):
    Forward = 0
    Reverse = 1

class CoordinateConversionResult(Enum):
    Success = 0
    Error_MultiConfig = -5
    Error_TiltDecenter = -4
    Error_IgnoredSurface = -3
    Error_CoordianteBreak = -2
    Error_InvalidRange = -1

class CoordinateReturnType(Enum):
    None_ = 0
    OrientationOnly = 1
    OrientationXY = 2
    OrientationXYZ = 3

class InterpolationMethod(Enum):
    BicubicSpline = 0
    Linear = 1

class NodesDataType(Enum):
    SurfaceDeformationNoRBM = 1
    RefractiveIndex = 2
    TemperatureAndRefractiveIndex = 3
    SurfaceDeformation = 4

class PilotRadiusMode(Enum):
    BestFit = 0
    Shorter = 1
    Longer = 2
    X = 3
    Y = 4
    Plane = 5
    User = 6

class PointCloudFileFormat(Enum):
    ASCII = 0
    Binary = 1
    CompressedBinary = 2

class PupilApodizationType(Enum):
    None_ = 0
    Gaussian = 1
    Tangential = 2

class QTypes(Enum):
    Qbfs = 0
    Qcon = 1

class STARDeformationOption(Enum):
    DeformationWithRBMs = 0
    DeformationWithoutRBMs = 1
    OnlyRBMs = 2
    NoDeformation = 3

class SubstrateType(Enum):
    None_ = 0
    Flat = 1
    Curved = 2

class SurfaceApertureTypes(Enum):
    None_ = 0
    CircularAperture = 1
    CircularObscuration = 2
    Spider = 3
    RectangularAperture = 4
    RectangularObscuration = 5
    EllipticalAperture = 6
    EllipticalObscuration = 7
    UserAperture = 8
    UserObscuration = 9
    FloatingAperture = 10

class SurfaceColumn(Enum):
    Comment = 1
    Radius = 2
    Thickness = 3
    Material = 4
    Coating = 5
    SemiDiameter = 6
    ChipZone = 7
    MechanicalSemiDiameter = 8
    Conic = 9
    TCE = 10
    Par0 = 11
    Par1 = 12
    Par2 = 13
    Par3 = 14
    Par4 = 15
    Par5 = 16
    Par6 = 17
    Par7 = 18
    Par8 = 19
    Par9 = 20
    Par10 = 21
    Par11 = 22
    Par12 = 23
    Par13 = 24
    Par14 = 25
    Par15 = 26
    Par16 = 27
    Par17 = 28
    Par18 = 29
    Par19 = 30
    Par20 = 31
    Par21 = 32
    Par22 = 33
    Par23 = 34
    Par24 = 35
    Par25 = 36
    Par26 = 37
    Par27 = 38
    Par28 = 39
    Par29 = 40
    Par30 = 41
    Par31 = 42
    Par32 = 43
    Par33 = 44
    Par34 = 45
    Par35 = 46
    Par36 = 47
    Par37 = 48
    Par38 = 49
    Par39 = 50
    Par40 = 51
    Par41 = 52
    Par42 = 53
    Par43 = 54
    Par44 = 55
    Par45 = 56
    Par46 = 57
    Par47 = 58
    Par48 = 59
    Par49 = 60
    Par50 = 61
    Par51 = 62
    Par52 = 63
    Par53 = 64
    Par54 = 65
    Par55 = 66
    Par56 = 67
    Par57 = 68
    Par58 = 69
    Par59 = 70
    Par60 = 71
    Par61 = 72
    Par62 = 73
    Par63 = 74
    Par64 = 75
    Par65 = 76
    Par66 = 77
    Par67 = 78
    Par68 = 79
    Par69 = 80
    Par70 = 81
    Par71 = 82
    Par72 = 83
    Par73 = 84
    Par74 = 85
    Par75 = 86
    Par76 = 87
    Par77 = 88
    Par78 = 89
    Par79 = 90
    Par80 = 91
    Par81 = 92
    Par82 = 93
    Par83 = 94
    Par84 = 95
    Par85 = 96
    Par86 = 97
    Par87 = 98
    Par88 = 99
    Par89 = 100
    Par90 = 101
    Par91 = 102
    Par92 = 103
    Par93 = 104
    Par94 = 105
    Par95 = 106
    Par96 = 107
    Par97 = 108
    Par98 = 109
    Par99 = 110
    Par100 = 111
    Par101 = 112
    Par102 = 113
    Par103 = 114
    Par104 = 115
    Par105 = 116
    Par106 = 117
    Par107 = 118
    Par108 = 119
    Par109 = 120
    Par110 = 121
    Par111 = 122
    Par112 = 123
    Par113 = 124
    Par114 = 125
    Par115 = 126
    Par116 = 127
    Par117 = 128
    Par118 = 129
    Par119 = 130
    Par120 = 131
    Par121 = 132
    Par122 = 133
    Par123 = 134
    Par124 = 135
    Par125 = 136
    Par126 = 137
    Par127 = 138
    Par128 = 139
    Par129 = 140
    Par130 = 141
    Par131 = 142
    Par132 = 143
    Par133 = 144
    Par134 = 145
    Par135 = 146
    Par136 = 147
    Par137 = 148
    Par138 = 149
    Par139 = 150
    Par140 = 151
    Par141 = 152
    Par142 = 153
    Par143 = 154
    Par144 = 155
    Par145 = 156
    Par146 = 157
    Par147 = 158
    Par148 = 159
    Par149 = 160
    Par150 = 161
    Par151 = 162
    Par152 = 163
    Par153 = 164
    Par154 = 165
    Par155 = 166
    Par156 = 167
    Par157 = 168
    Par158 = 169
    Par159 = 170
    Par160 = 171
    Par161 = 172
    Par162 = 173
    Par163 = 174
    Par164 = 175
    Par165 = 176
    Par166 = 177
    Par167 = 178
    Par168 = 179
    Par169 = 180
    Par170 = 181
    Par171 = 182
    Par172 = 183
    Par173 = 184
    Par174 = 185
    Par175 = 186
    Par176 = 187
    Par177 = 188
    Par178 = 189
    Par179 = 190
    Par180 = 191
    Par181 = 192
    Par182 = 193
    Par183 = 194
    Par184 = 195
    Par185 = 196
    Par186 = 197
    Par187 = 198
    Par188 = 199
    Par189 = 200
    Par190 = 201
    Par191 = 202
    Par192 = 203
    Par193 = 204
    Par194 = 205
    Par195 = 206
    Par196 = 207
    Par197 = 208
    Par198 = 209
    Par199 = 210
    Par200 = 211
    Par201 = 212
    Par202 = 213
    Par203 = 214
    Par204 = 215
    Par205 = 216
    Par206 = 217
    Par207 = 218
    Par208 = 219
    Par209 = 220
    Par210 = 221
    Par211 = 222
    Par212 = 223
    Par213 = 224
    Par214 = 225
    Par215 = 226
    Par216 = 227
    Par217 = 228
    Par218 = 229
    Par219 = 230
    Par220 = 231
    Par221 = 232
    Par222 = 233
    Par223 = 234
    Par224 = 235
    Par225 = 236
    Par226 = 237
    Par227 = 238
    Par228 = 239
    Par229 = 240
    Par230 = 241
    Par231 = 242
    Par232 = 243
    Par233 = 244
    Par234 = 245
    Par235 = 246
    Par236 = 247
    Par237 = 248
    Par238 = 249
    Par239 = 250
    Par240 = 251
    Par241 = 252
    Par242 = 253
    Par243 = 254
    Par244 = 255
    Par245 = 256
    Par246 = 257
    Par247 = 258
    Par248 = 259
    Par249 = 260
    Par250 = 261
    Par251 = 262
    Par252 = 263
    Par253 = 264
    Par254 = 265

class SurfaceEdgeDraw(Enum):
    Squared = 0
    Tapered = 1
    Flat = 2

class SurfaceScatteringTypes(Enum):
    None_ = 0
    Lambertian = 1
    Gaussian = 2
    ABg = 3
    ABgFile = 4
    BSDF = 5
    User = 6
    ISScatterCatalog = 7

class SurfaceType(Enum):
    ABCD = 0
    AlternateEven = 1
    AlternateOdd = 2
    AnnularZernikeSag = 3
    Atmospheric = 4
    Biconic = 5
    BiconicZernike = 6
    Binary1 = 7
    Binary2 = 8
    Binary3 = 9
    Binary4 = 10
    BirefringentIn = 11
    BirefringentOut = 12
    BlackBoxLens = 13
    ChebyShv = 14
    Conjugate = 15
    CoordinateBreak = 16
    CubicSpline = 17
    CylinderFrensel = 18
    CylinderFresnel = 18
    Data = 19
    DiffractionGrating = 20
    EllipticalGrating1 = 21
    EllipticalGrating2 = 22
    EvenAspheric = 23
    ExtendedToroidalGrating = 24
    ExtendedAsphere = 25
    ExtendedCubicSpline = 26
    ExtendedFresnel = 27
    ExtendedOddAsphere = 28
    ExtendedPolynomial = 29
    Fresnel = 30
    GeneralizedFresnel = 31
    Gradient1 = 32
    Gradient2 = 33
    Gradient3 = 34
    Gradient4 = 35
    Gradient5 = 36
    Gradient6 = 37
    Gradient7 = 38
    Gradient9 = 39
    Gradient10 = 40
    Gradient12 = 41
    Gradium = 42
    GridGradient = 43
    GridPhase = 44
    GridSag = 45
    Hologram1 = 46
    Hologram2 = 47
    Irregular = 48
    JonesMatrix = 49
    NonSequential = 50
    OddAsphere = 51
    OddCosine = 52
    OffAxisConicFreeform = 53
    OpticallyFabricatedHologram = 54
    Paraxial = 55
    ParaxialXY = 56
    Periodic = 57
    Polynomial = 58
    QTypeAsphere = 59
    QTypeFreeform = 60
    RadialGrating = 61
    RadialNurbs = 62
    RetroReflect = 63
    SlideSurface = 64
    Standard = 65
    Superconic = 66
    Tilted = 67
    Toroidal = 68
    ToroidalGrat = 69
    ToroidalHologram = 70
    ToroidalNurbs = 71
    UserDefined = 72
    VariableLineSpaceGrating = 73
    ZernikeAnnularPhase = 74
    ZernikeFringePhase = 75
    ZernikeFringeSag = 76
    ZernikeStandardPhase = 77
    ZernikeStandardSag = 78
    ZonePlate = 79
    Freeform = 80

class TiltDecenterOrderType(Enum):
    Decenter_Tilt = 0
    Tilt_Decenter = 1

class TiltDecenterPickupType(Enum):
    Explicit = 0
    PickupSurface = 1
    ReverseSurface = 2

class TiltType(Enum):
    XTilt = 0
    YTilt = 1

class XYSampling(Enum):
    S32 = 0
    S64 = 1
    S128 = 2
    S256 = 3
    S512 = 4
    S1024 = 5
    S2048 = 6
    S4096 = 7
    S8192 = 8
    S16384 = 9
