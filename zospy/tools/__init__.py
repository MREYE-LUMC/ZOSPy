"""OpticStudio Tools.

Tools in OpticStudio are available through `zospy.tools`.
This module provides basic classes and functions for interacting with
tools (in `zospy.tools.base`), as well as an object-oriented interface
to several tools.
"""

from __future__ import annotations

from zospy.tools.base import open_tool
from zospy.tools.quick_focus import QuickFocus, QuickFocusSettings

__all__ = ("QuickFocus", "QuickFocusSettings", "open_tool")
