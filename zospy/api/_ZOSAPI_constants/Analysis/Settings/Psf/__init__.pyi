"""
This file provides autocompletions for the ZOS-API and was automatically generated.
It should not be edited manually.
"""

from enum import Enum

__all__ = ("FftPsfType", "PsfRotation", "PsfSampling")

class FftPsfType(Enum):
    Linear = 0
    Log = 1
    Phase = 2
    Real = 3
    Imaginary = 4

class PsfRotation(Enum):
    CW0 = 0
    CW90 = 1
    CW180 = 2
    CW270 = 3

class PsfSampling(Enum):
    PsfS_32x32 = 1
    PsfS_64x64 = 2
    PsfS_128x128 = 3
    PsfS_256x256 = 4
    PsfS_512x512 = 5
    PsfS_1024x1024 = 6
    PsfS_2048x2048 = 7
    PsfS_4096x4096 = 8
    PsfS_8192x8192 = 9
    PsfS_16384x16384 = 10
