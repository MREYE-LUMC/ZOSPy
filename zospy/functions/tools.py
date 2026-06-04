"""Utility functions for Tools in OpticStudio."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from zospy.api import _ZOSAPI
    from zospy.zpcore import OpticStudioSystem

__all__ = ("open_tool",)

logger = logging.getLogger(__name__)


@contextmanager
def open_tool(
    oss: OpticStudioSystem, tool: Callable[[], _ZOSAPI.Tools.ISystemTool], *, close_current: bool = False
) -> Generator[_ZOSAPI.Tools.ISystemTool, Any, None]:
    """Context manager for opening a tool in OpticStudio.

    Opens a tool in OpticStudio and ensures that it is properly closed after use. If there is already an open tool, it
    will be closed if `close_current` is True. Otherwise, a RuntimeError is raised.

    Parameters
    ----------
    oss : OpticStudioSystem
        The OpticStudio system to use for opening the tool.
    tool : Callable[..., _ZOSAPI.Tools.ISystemTool]
        A callable that returns an instance of the tool to be opened.
    close_current : bool
        Whether to close the currently open tool before opening the new one. Defaults to False.

    Yields
    ------
    _ZOSAPI.Tools.ISystemTool
        An instance of the opened tool.

    Raises
    ------
    RuntimeError
        If there is already an open tool and `close_current` is False.
    """
    if oss.Tools.CurrentTool is not None:
        if close_current:
            logger.warning(
                "A tool is already open. Closing the currently open tool (%s) before opening the new one.",
                oss.Tools.CurrentTool.__class__.__name__,
            )
            oss.Tools.CurrentTool.Close()
        else:
            raise RuntimeError("Cannot open tool because another tool is already open.")

    new_tool = tool()

    try:
        yield new_tool
    finally:
        if oss.Tools.CurrentTool is not None and oss.Tools.CurrentTool == new_tool:
            logger.info("Closing tool %s.", new_tool.__class__.__name__)
            new_tool.Close()
