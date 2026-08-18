"""ZOS-API connection management.

This module contains functions for initialization of and communication with the ZOS-API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zospy.api.stubs import _ZOSAPI, _ZOSAPI_constants  # ruff: ignore[runtime-import-in-type-checking-block]

    __all__ = ["_ZOSAPI", "_ZOSAPI_constants"]
