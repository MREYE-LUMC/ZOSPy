"""Base functionality for tools."""

from __future__ import annotations

import dataclasses
import logging
import weakref
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import is_dataclass
from types import NoneType
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, get_args

import numpy as np
import pandas as pd
import pydantic

from zospy.analyses.base import _deserialize_analysis_data, _deserialize_zospy_class, _serialize_analysis_data_type
from zospy.analyses.parsers.types import ValidatedDataFrame

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from zospy.api import _ZOSAPI
    from zospy.zpcore import OpticStudioSystem


__all__ = ("BaseToolWrapper", "ToolResult", "open_tool")

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


ToolOutputData = TypeVar("ToolOutputData")
ToolSettings = TypeVar("ToolSettings")


@pydantic.dataclasses.dataclass(frozen=True, config=pydantic.ConfigDict(ser_json_inf_nan="constants"))
class ToolResult(Generic[ToolOutputData, ToolSettings]):
    """Zemax OpticStudio tool result.

    Attributes
    ----------
    data : ToolOutputData
        The data of the tool. Can be a `pandas.DataFrame`, `numpy.ndarray`, or a tool-specific dataclass.
    settings : ToolSettings | None
        The settings of the tool.
    error_message : str | None
        Error message from the analysis. If the tool ran successfully, this will be None.
    """

    data: ToolOutputData
    settings: ToolSettings | None
    error_message: str | None

    def to_json(self):
        """Convert the result to a JSON string."""
        return pydantic.RootModel(self).model_dump_json(indent=4)

    @classmethod
    def from_json(cls, data: str):
        """Create a result from a JSON string."""
        return pydantic.TypeAdapter(cls).validate_json(data)

    @pydantic.field_serializer("data", mode="wrap", when_used="json")
    @staticmethod
    def _serialize_data(
        value: ToolOutputData,
        nxt: pydantic.SerializerFunctionWrapHandler,
        info,  # noqa: ARG004
    ):
        if isinstance(value, pd.DataFrame):
            return pydantic.TypeAdapter(
                ValidatedDataFrame, config=pydantic.ConfigDict(ser_json_inf_nan="constants")
            ).dump_python(value, mode="json")

        if isinstance(value, np.ndarray):
            return value.tolist()

        return nxt(value)

    @pydantic.model_serializer(mode="wrap", when_used="json")
    def _serialize_types(self, nxt: pydantic.SerializerFunctionWrapHandler):
        data = nxt(self)
        data["__tool_data__"] = _serialize_analysis_data_type(self.data)
        data["__tool_settings__"] = {
            "data_type": "zospy_class",
            "name": type(self.settings).__name__,
            "module": type(self.settings).__module__,
        }

        return data

    @pydantic.model_validator(mode="wrap")
    @classmethod
    def _deserialize_types(cls, data: Any, handler):
        if isinstance(data, dict):
            if "__tool_data__" in data:
                data["data"] = _deserialize_analysis_data(data["data"], data.pop("__tool_data__"))
            if "__tool_settings__" in data:
                data["settings"] = _deserialize_zospy_class(data["settings"], data.pop("__tool_settings__"))

        return handler(data)


class BaseToolWrapper(ABC, Generic[ToolOutputData, ToolSettings]):
    """Base class for tool wrappers.

    This class provides a common interface for all tool wrappers. It defines the methods and properties that all
    tool wrappers should implement.

    Attributes
    ----------
    CONNECTION_MODE : {"standalone", "extension"} | None
        The connection mode required for the tool. If None, the tool can be used in any mode.
    """

    CONNECTION_MODE: Literal["standalone", "extension"] | None = None

    def __init__(self, *, settings_kws: dict[str, Any] | None = None):
        """Create a new tool wrapper.

        Settings can be changed by passing the settings as keyword arguments. Use the `with_settings` method to specify
        the settings using a settings object.

        Parameters
        ----------
        settings_kws : dict[str, Any]
            Arguments to set the settings of the tool.

        Raises
        ------
        ValueError
            If `settings` is not a dataclass.
        """
        self._settings = self._default_settings()
        self.update_settings(settings_kws=settings_kws)

        self._oss = None

    def __init_subclass__(
        cls,
        *,
        connection_mode: Literal["standalone", "extension"] | None = None,
        **kwargs,
    ):
        """Determine the settings type and class-level configuration of the tool."""
        cls.CONNECTION_MODE = connection_mode

        if not hasattr(cls, "_settings_type"):
            if hasattr(cls, "__orig_bases__"):
                base = cls.__orig_bases__[0]
                cls._settings_type: type[ToolSettings] = get_args(base)[1]
            else:
                cls._settings_type = NoneType

        super().__init_subclass__(**kwargs)

    @abstractmethod
    def _get_tool_opener(self, oss: OpticStudioSystem) -> Callable[[], _ZOSAPI.Tools.ISystemTool]:
        """Callable that opens the tool in OpticStudio and returns the tool object."""
        raise NotImplementedError("Subclasses of BaseToolWrapper must implement the `tool_opener` property.")

    def update_settings(
        self,
        *,
        settings: ToolSettings | None = None,
        settings_kws: dict[str, Any] | None = None,
    ) -> None:
        """Update the settings of the tool using a settings object or keyword arguments.

        Settings can be specified as an object and as keyword arguments. If both are specified, the keyword arguments
        take precedence. If no settings are specified, the default settings are used. Furthermore, instead of using
        a reference to the settings object, a new settings object is created with the specified parameters. This is done
        to avoid modifying the original settings object.

        Parameters
        ----------
        settings : ToolSettings
            Tool settings object.
        settings_kws
            Dictionary with the settings parameters.

        Raises
        ------
        ValueError
            If `settings` is not a dataclass.
        """
        # Use the existing settings if no settings are specified
        settings = settings or self.settings

        if settings is None:
            # Analysis does not have settings
            return

        if not is_dataclass(settings):
            raise TypeError("settings should be a dataclass.")

        # Create a new settings object with the specified parameters. If no parameters are specified, this creates a
        # copy of the settings object. This is done to avoid modifying the original settings object.
        self._settings = dataclasses.replace(settings, **(settings_kws or {}))

    @classmethod
    def _default_settings(cls) -> ToolSettings:
        """Get the default settings of the tool.

        Returns
        -------
        ToolSettings
            The default settings.
        """
        return cls._settings_type()

    @classmethod
    def with_settings(cls, settings: ToolSettings):
        """Create a new tool with the specified settings.

        Parameters
        ----------
        settings : ToolSettings
            Settings of the tool.

        Returns
        -------
        BaseAnalysisWrapper
            The tool wrapper.
        """
        instance = cls()
        instance.update_settings(settings=settings)

        return instance

    @property
    def settings(self) -> ToolSettings:
        """Settings of the tool."""
        return self._settings

    @property
    def oss(self) -> OpticStudioSystem:
        """The OpticStudio system. This property is set when the tool is run."""
        if self._oss is None:
            raise ValueError("OpticStudioSystem has not been set.")

        return self._oss

    @abstractmethod
    def _run_tool(self, tool: _ZOSAPI.Tools.ISystemTool, *args, **kwargs) -> ToolOutputData:
        """Run the tool and return the results."""

    def _check_mode(self):
        connection_modes: dict[str, str] = {
            "Server": "standalone",
            "Plugin": "extension",
        }

        if self.CONNECTION_MODE is None:
            return

        if str(self.oss.ZOS.Application.Mode) not in connection_modes:
            raise ValueError(f"Unknown connection mode: {self.oss.ZOS.Application.Mode}")

        current_mode = connection_modes[str(self.oss.ZOS.Application.Mode)]

        if current_mode != self.CONNECTION_MODE:
            raise ValueError(f"The tool requires {self.CONNECTION_MODE} mode, got {current_mode}.")

    def run(
        self,
        oss: OpticStudioSystem,
        *,
        close_current: bool = False,
    ) -> ToolResult[ToolOutputData, ToolSettings]:
        """Run the tool and return the results.

        This method opens and runs the tool in OpticStudio with the specified settings.
        If another tool is already open, it will be closed if `close_current` is True. Otherwise, a RuntimeError is raised.

        Parameters
        ----------
        oss : OpticStudioSystem
            The OpticStudio system.
        close_current : bool
            Whether to close the current tool if one is already open.

        Returns
        -------
        ToolResult
            The tool result.
        """
        self._oss = weakref.proxy(oss)
        self._check_mode()

        with open_tool(oss, self._get_tool_opener(oss), close_current=close_current) as tool:
            data = self._run_tool(tool)

            error_message = tool.ErrorMessage

        return ToolResult(
            data=data,
            settings=self.settings,
            error_message=error_message,
        )

    def __call__(self, oss: OpticStudioSystem, *args, **kwargs):
        """Run the tool and return the results."""
        return self.run(oss, *args, **kwargs)
