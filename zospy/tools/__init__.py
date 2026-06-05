"""OpticStudio Tools.

Tools in OpticStudio are available through `zospy.tools`.
This module provides basic classes and functions for interacting with
tools (in `zospy.tools.base`), as well as an object-oriented interface
to several tools.
"""

from __future__ import annotations

from zospy.tools.base import open_tool
from zospy.tools.batch_raytrace import (
    BatchRayTraceNormUnpol,
    BatchRayTraceNormUnpolSettings,
)
from zospy.tools.quick_focus import QuickFocus, QuickFocusSettings

__all__ = (
    "BatchRayTraceNormUnpol",
    "BatchRayTraceNormUnpolSettings",
    "QuickFocus",
    "QuickFocusSettings",
    "open_tool",
)
