"""This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from __future__ import annotations

from zospy.api._ZOSAPI.Common import ZemaxColor
from zospy.api._ZOSAPI.Editors import IEditor, IEditorCell, IEditorRow

__all__ = ("IMeritFunctionEditor", "IMFERow", "MeritColumn", "MeritOperandType")

class IMeritFunctionEditor(IEditor):
    @property
    def RowToOperandOffset(self) -> int: ...
    @property
    def NumberOfOperands(self) -> int: ...
    @property
    def FirstColumn(self) -> MeritColumn: ...
    @property
    def LastColumn(self) -> MeritColumn: ...
    @property
    def MeritFunctionDirectory(self) -> str: ...
    @property
    def NSCOptimizationWizard(self) -> INSCOptimizationWizard: ...
    @property
    def SEQOptimizationWizard(self) -> ISEQOptimizationWizard: ...
    @property
    def NSCBitmapWizard(self) -> INSCBitmapWizard: ...
    @property
    def NSCRoadwayLightingWizard(self) -> INSCRoadwayLightingWizard: ...
    @property
    def SEQOptimizationWizard2(self) -> ISEQOptimizationWizard2: ...
    def AddOperand(self) -> IMFERow: ...
    def CalculateMeritFunction(self) -> float: ...
    def CopyOperands(self, fromOperandNumber: int, NumberOfOperands: int, toOperandNumber: int) -> int: ...
    def CopyOperandsFrom(
        self, fromEditor: IMeritFunctionEditor, fromOperandNumber: int, NumberOfOperands: int, toOperandNumber: int
    ) -> int: ...
    def GetMeritFunctionFiles(self) -> list[str]: ...
    def GetOperandAt(self, OperandNumber: int) -> IMFERow: ...
    def GetOperandValue(
        self,
        type: MeritOperandType,
        srf: int,
        wave: int,
        Hx: float,
        Hy: float,
        Px: float,
        Py: float,
        Ex: float,
        Ey: float,
    ) -> float: ...
    def HideMFE(self) -> None: ...
    def InsertMeritFunction(self, fileName: str, OperandNumber: int) -> int: ...
    def InsertNewOperandAt(self, OperandNumber: int) -> IMFERow: ...
    def LoadMeritFunction(self, fileName: str) -> None: ...
    def RemoveOperandAt(self, OperandNumber: int) -> bool: ...
    def RemoveOperandsAt(self, OperandNumber: int, numOperands: int) -> int: ...
    def SaveMeritFunction(self, fileName: str) -> None: ...
    def ShowMFE(self) -> bool: ...

class IMFERow(IEditorRow):
    @property
    def IsActive(self) -> bool: ...
    @property
    def OperandNumber(self) -> int: ...
    @property
    def TypeName(self) -> str: ...
    @property
    def Type(self) -> MeritOperandType: ...
    @property
    def RowColor(self) -> ZemaxColor: ...
    @RowColor.setter
    def RowColor(self, value: ZemaxColor) -> None: ...
    @property
    def Target(self) -> float: ...
    @Target.setter
    def Target(self, value: float) -> None: ...
    @property
    def TargetCell(self) -> IEditorCell: ...
    @property
    def Weight(self) -> float: ...
    @Weight.setter
    def Weight(self, value: float) -> None: ...
    @property
    def WeightCell(self) -> IEditorCell: ...
    @property
    def Value(self) -> float: ...
    @property
    def ValueCell(self) -> IEditorCell: ...
    @property
    def Contribution(self) -> float: ...
    @property
    def ContributionCell(self) -> IEditorCell: ...
    def AvailableOperandTypes(self) -> list[MeritOperandType]: ...
    def ChangeType(self, type: MeritOperandType) -> bool: ...
    def GetOperandCell(self, Col: MeritColumn) -> IEditorCell: ...

class MeritColumn:
    Comment = 1
    Param1 = 2
    Param2 = 3
    Param3 = 4
    Param4 = 5
    Param5 = 6
    Param6 = 7
    Param7 = 8
    Param8 = 9
    Target = 10
    Weight = 11
    Value = 12
    Contrib = 13

class MeritOperandType:
    ACOS = 0
    ABSO = 1
    CVVA = 2
    DENC = 3
    DENF = 4
    DIFF = 5
    AMAG = 6
    ANAC = 7
    ANAR = 8
    ANAX = 9
    ANAY = 10
    ANCX = 11
    ANCY = 12
    ASIN = 13
    ASTI = 14
    ATAN = 15
    AXCL = 16
    BIOC = 17
    CTVA = 18
    CVGT = 19
    CVLT = 20
    CVOL = 21
    DIMX = 22
    DISC = 23
    DISG = 24
    DIST = 25
    DIVI = 26
    DLTN = 27
    DMFS = 28
    DMGT = 29
    DMLT = 30
    DMVA = 31
    DXDX = 32
    DXDY = 33
    DYDX = 34
    DYDY = 35
    EFFL = 36
    EFLX = 37
    EFLY = 38
    ENDX = 39
    ENPP = 40
    EPDI = 41
    EQUA = 42
    ETGT = 43
    ETLT = 44
    ETVA = 45
    EXPP = 46
    FCGS = 47
    FCGT = 48
    FCUR = 49
    FICL = 50
    FICP = 51
    FOUC = 52
    GBPD = 53
    GBPR = 54
    GBPS = 55
    GBPW = 56
    GBPP = 57
    GBSD = 58
    P1GT = 59
    P1LT = 60
    P1VA = 61
    P2GT = 62
    P2LT = 63
    P2VA = 64
    P3GT = 65
    P3LT = 66
    P3VA = 67
    P4GT = 68
    P4LT = 69
    P4VA = 70
    P5GT = 71
    P5LT = 72
    P5VA = 73
    P6GT = 74
    P6LT = 75
    P6VA = 76
    P7GT = 77
    P7LT = 78
    P7VA = 79
    P8GT = 80
    P8LT = 81
    P8VA = 82
    PANA = 83
    PANB = 84
    PANC = 85
    PARA = 86
    PARB = 87
    PARC = 88
    PARR = 89
    PARX = 90
    PARY = 91
    PARZ = 92
    PATX = 93
    PATY = 94
    PETC = 95
    PETZ = 96
    PIMH = 97
    PLEN = 98
    PMAG = 99
    POWR = 100
    PRIM = 101
    PROD = 102
    PMGT = 103
    PMLT = 104
    PMVA = 105
    POPD = 106
    QOAC = 107
    QSUM = 108
    RAGA = 109
    RAGB = 110
    RAGC = 111
    RAGX = 112
    RAGY = 113
    RAGZ = 114
    RAED = 115
    RAEN = 116
    RAID = 117
    RAIN = 118
    RANG = 119
    REAA = 120
    REAB = 121
    REAC = 122
    REAR = 123
    REAX = 124
    REAY = 125
    REAZ = 126
    RELI = 127
    GBSR = 128
    GBSS = 129
    TGTH = 130
    TMAS = 131
    TOTR = 132
    TRAC = 133
    TRAD = 134
    TRAE = 135
    TRAI = 136
    TRAN = 137
    TRAR = 138
    TRAX = 139
    TRAY = 140
    TRCX = 141
    TRCY = 142
    TTGT = 143
    TTHI = 144
    TTLT = 145
    GBSW = 146
    GBSP = 147
    GCOS = 148
    GENC = 149
    GENF = 150
    GLCA = 151
    GLCB = 152
    GLCC = 153
    GLCX = 154
    GLCY = 155
    GLCZ = 156
    GMTA = 157
    GMTS = 158
    GMTT = 159
    GOTO = 160
    GPIM = 161
    GRMN = 162
    GRMX = 163
    GTCE = 164
    HACG = 165
    HHCN = 166
    I1GT = 167
    BIOD = 168
    BIPF = 169
    BLNK = 170
    BSER = 171
    CENX = 172
    CENY = 173
    CMFV = 174
    CMGT = 175
    CMLT = 176
    CMVA = 177
    CODA = 178
    COGT = 179
    COLT = 180
    COMA = 181
    CONF = 182
    CONS = 183
    COSI = 184
    COVA = 185
    CTGT = 186
    CTLT = 187
    I2GT = 188
    I3GT = 189
    I4GT = 190
    I5GT = 191
    I6GT = 192
    I1LT = 193
    I2LT = 194
    I3LT = 195
    I4LT = 196
    I5LT = 197
    I6LT = 198
    I1VA = 199
    I2VA = 200
    I3VA = 201
    I4VA = 202
    I5VA = 203
    I6VA = 204
    IMAE = 205
    IMSF = 206
    INDX = 207
    ISFN = 208
    ISNA = 209
    LACL = 210
    LINV = 211
    LOGE = 212
    LOGT = 213
    LONA = 214
    LPTD = 215
    MAXX = 216
    MCOG = 217
    MCOL = 218
    MCOV = 219
    MINN = 220
    MNAB = 221
    MNCA = 222
    MNCG = 223
    MNCT = 224
    MNCV = 225
    MNDT = 226
    MNEA = 227
    MNEG = 228
    MNET = 229
    MNIN = 230
    MNPD = 231
    MNSD = 232
    MSWA = 233
    MSWS = 234
    MSWT = 235
    MTFA = 236
    MTFS = 237
    MTFT = 238
    MXAB = 239
    MXCA = 240
    MXCG = 241
    MXCT = 242
    MXCV = 243
    MXDT = 244
    MXEA = 245
    MXEG = 246
    MXET = 247
    MXIN = 248
    MXPD = 249
    MXSD = 250
    NPGT = 251
    NPLT = 252
    NPVA = 253
    NPXG = 254
    NPXL = 255
    NPXV = 256
    NPYG = 257
    NPYL = 258
    NPYV = 259
    NPZG = 260
    NPZL = 261
    NPZV = 262
    NSDC = 263
    NSDD = 264
    NSRA = 265
    NSTR = 266
    NTXG = 267
    NTXL = 268
    NTXV = 269
    NTYG = 270
    NTYL = 271
    NTYV = 272
    NTZG = 273
    NTZL = 274
    NTZV = 275
    OSCD = 276
    OBSN = 277
    OOFF = 278
    OPDC = 279
    OPDM = 280
    OPDX = 281
    OPGT = 282
    OPLT = 283
    OPVA = 284
    OPTH = 285
    OSUM = 286
    RENA = 287
    RENB = 288
    RENC = 289
    RETX = 290
    RETY = 291
    RGLA = 292
    RSCH = 293
    RSCE = 294
    RSRE = 295
    RSRH = 296
    RWCH = 297
    RWCE = 298
    RWRE = 299
    RWRH = 300
    SAGX = 301
    SAGY = 302
    SFNO = 303
    SINE = 304
    SKIS = 305
    SKIN = 306
    SPCH = 307
    SPHA = 308
    SQRT = 309
    SSAG = 310
    SUMM = 311
    SVIG = 312
    TANG = 313
    TFNO = 314
    WFNO = 315
    TTVA = 316
    UDOP = 317
    UDOC = 318
    USYM = 319
    VOLU = 320
    WLEN = 321
    XDVA = 322
    XDGT = 323
    XDLT = 324
    XENC = 325
    XENF = 326
    XNEA = 327
    XNEG = 328
    XNET = 329
    XXEA = 330
    XXEG = 331
    XXET = 332
    YNIP = 333
    ZERN = 334
    ZPLM = 335
    ZTHI = 336
    TOLR = 337
    FTGT = 338
    FTLT = 339
    GLCR = 340
    EFNO = 341
    DIVB = 342
    PROB = 343
    TCGT = 344
    TCLT = 345
    TCVA = 346
    NORX = 347
    NORY = 348
    NORZ = 349
    NORD = 350
    COSA = 351
    MTHA = 352
    MTHS = 353
    MTHT = 354
    BFSD = 355
    EXPD = 356
    CVIG = 357
    GPSX = 358
    GPSY = 359
    GPRX = 360
    GPRY = 361
    GPRT = 362
    POWF = 363
    STHI = 364
    CNPX = 365
    CNPY = 366
    CNAX = 367
    CNAY = 368
    STRH = 369
    CIGT = 370
    CILT = 371
    CIVA = 372
    CEGT = 373
    CELT = 374
    CEVA = 375
    NSST = 376
    ABCD = 377
    DISA = 378
    POWP = 379
    RECI = 380
    NSRM = 381
    FDMO = 382
    FDRE = 383
    FREZ = 384
    NSDE = 385
    ERFP = 386
    NSDP = 387
    POPI = 388
    ABGT = 389
    ABLT = 390
    SMIA = 391
    SCUR = 392
    SDRV = 393
    REVR = 394
    NSLT = 395
    NSTW = 396
    NSRW = 397
    MNRE = 398
    MXRE = 399
    MNRI = 400
    MXRI = 401
    CEHX = 402
    CEHY = 403
    BLTH = 404
    GBPZ = 405
    NSRD = 406
    NPAF = 407
    MECS = 408
    MECT = 409
    GMTN = 410
    GMTX = 411
    MTFN = 412
    MTFX = 413
    MTHN = 414
    MTHX = 415
    MECA = 416
    MSWN = 417
    MSWX = 418
    GAOI = 419
    MNAI = 420
    MXAI = 421
    HYLD = 422
    OGSS = 423
    SPHD = 424
    SPHS = 425
    SSLP = 426
    SCRV = 427
    DSAG = 428
    DPHS = 429
    DSLP = 430
    DCRV = 431
    EFLA = 432
    CARD = 433
    TSAG = 434
    PSLP = 435
    QSLP = 436
