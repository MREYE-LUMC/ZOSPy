"""Base functionality for analyses.

This module provides classes and functions to handle the creation, configuration, and execution of analyses, as well as
the serialization and deserialization of analysis results.

Classes
-------
AnalysisMessage
    Represents a message from a OpticStudio analysis.
AnalysisMetadata
    Contains metadata from a OpticStudio analysis.
AnalysisResult
    Represents the result of a OpticStudio analysis.
OnComplete
    Enum defining actions to perform after running an analysis.
Analysis
    Provides access to the settings and results of a OpticStudio analysis.
AnalysisWrapper
    Abstract base class for analysis wrappers.

Functions
---------
new_analysis(oss, analysis_type, settings_first=True)
    Creates a new analysis in OpticStudio.
"""

from __future__ import annotations

import dataclasses
import os
import weakref
from abc import ABC, abstractmethod
from dataclasses import dataclass, is_dataclass
from datetime import datetime  # noqa: TCH003 Pydantic needs datetime to be present at runtime
from enum import Enum
from importlib import import_module
from pathlib import Path
from tempfile import mkstemp
from typing import TYPE_CHECKING, Any, Generic, Literal, TypedDict, TypeVar, cast, get_args

import numpy as np
import pandas as pd
import pydantic
from pydantic import (
    BaseModel,
    ConfigDict,
    RootModel,
    TypeAdapter,
    field_serializer,
    model_serializer,
    model_validator,
)

from zospy.analyses.parsers import load_grammar, parse
from zospy.analyses.parsers.types import ValidatedDataFrame
from zospy.api import _ZOSAPI, constants
from zospy.utils import zputils
from zospy.utils.clrutils import system_datetime_to_datetime

if TYPE_CHECKING:
    import sys

    from lark import Transformer
    from pydantic_core.core_schema import SerializerFunctionWrapHandler

    from zospy.zpcore import OpticStudioSystem

    if sys.version_info <= (3, 11):
        from typing_extensions import NotRequired
    else:
        from typing import NotRequired


__all__ = (
    "Analysis",
    "AnalysisResult",
    "BaseAnalysisWrapper",
    "OnComplete",
    "new_analysis",
)


@dataclass(frozen=True)
class AnalysisMessage:
    """Zemax OpticStudio analysis message."""

    ErrorCode: str
    Message: str


@dataclass(frozen=True)
class AnalysisMetadata:
    """Zemax OpticStudio analysis metadata."""

    DateTime: datetime
    FeatureDescription: str
    LensFile: str
    LensTitle: str


AnalysisData = TypeVar("AnalysisData")
AnalysisSettings = TypeVar("AnalysisSettings")


class _TypeInfo(TypedDict):
    data_type: Literal["dataframe", "ndarray", "zospy_class", "none"]
    name: NotRequired[str | None]
    module: NotRequired[str | None]


def _serialize_analysis_data_type(data: AnalysisData) -> _TypeInfo:
    if data is None:
        return {"data_type": "none"}

    if isinstance(data, pd.DataFrame):
        return {"data_type": "dataframe"}

    if isinstance(data, np.ndarray):
        return {"data_type": "ndarray"}

    if is_dataclass(data) or isinstance(data, BaseModel):
        return {"data_type": "zospy_class", "name": type(data).__name__, "module": type(data).__module__}

    raise ValueError(f"Cannot serialize data type: {type(data)}")


def _deserialize_zospy_class(data: dict, typeinfo: _TypeInfo) -> AnalysisData:
    if typeinfo["module"].startswith("zospy.analyses"):
        try:
            m = import_module(typeinfo["module"])
            t = getattr(m, typeinfo["name"])

            return TypeAdapter(t).validate_python(data)
        except (ModuleNotFoundError, AttributeError):
            return data

    return data


def _deserialize_analysis_data(data: dict | list, typeinfo: _TypeInfo) -> AnalysisData:
    if typeinfo["data_type"] == "none":
        return None

    if typeinfo["data_type"] == "dataframe":
        return pd.DataFrame.from_dict(data, orient="tight")

    if typeinfo["data_type"] == "ndarray":
        return np.array(data)

    if typeinfo["data_type"] == "zospy_class":
        return _deserialize_zospy_class(data, typeinfo)

    raise ValueError(f"Cannot deserialize data type: {typeinfo['data_type']}")


@pydantic.dataclasses.dataclass(frozen=True, config=ConfigDict(ser_json_inf_nan="constants"))
class AnalysisResult(Generic[AnalysisData, AnalysisSettings]):
    """Zemax OpticStudio analysis result.

    Attributes
    ----------
    data : AnalysisData
        The data of the analysis. Can be a `pandas.DataFrame`, `numpy.ndarray`, or an analysis-specific dataclass.
    settings : AnalysisSettings
        The settings of the analysis.
    metadata : AnalysisMetadata
        Metadata of the analysis. Contains the date and time of the analysis, the feature description, the lens file,
        and the lens title.
    header : list[str] | None
        The header data of the analysis. Only available for some analyses.
    messages : list[AnalysisMessage] | None
        Error messages from the analysis.
    """

    data: AnalysisData
    settings: AnalysisSettings
    metadata: AnalysisMetadata
    header: list[str] | None = None
    messages: list[AnalysisMessage] | None = None

    def to_json(self):
        """Convert the result to a JSON string."""
        return RootModel(self).model_dump_json(indent=4)

    @classmethod
    def from_json(cls, data: str):
        """Create a result from a JSON string."""
        return TypeAdapter(cls).validate_json(data)

    @field_serializer("data", mode="wrap", when_used="json")
    def _serialize_data(
        self,
        value: AnalysisData,
        nxt: SerializerFunctionWrapHandler,
        info,  # noqa: ARG002
    ):
        if isinstance(value, pd.DataFrame):
            return TypeAdapter(ValidatedDataFrame, config=ConfigDict(ser_json_inf_nan="constants")).dump_python(
                value, mode="json"
            )

        if isinstance(value, np.ndarray):
            return value.tolist()

        return nxt(value)

    @model_serializer(mode="wrap", when_used="json")
    def _serialize_types(self, nxt: SerializerFunctionWrapHandler):
        data = nxt(self)
        data["__analysis_data__"] = _serialize_analysis_data_type(self.data)
        data["__analysis_settings__"] = {
            "data_type": "zospy_class",
            "name": type(self.settings).__name__,
            "module": type(self.settings).__module__,
        }

        return data

    @model_validator(mode="wrap")
    @classmethod
    def _deserialize_types(cls, data: Any, handler):
        if isinstance(data, dict):
            if "__analysis_data__" in data:
                data["data"] = _deserialize_analysis_data(data["data"], data.pop("__analysis_data__"))
            if "__analysis_settings__" in data:
                data["settings"] = _deserialize_zospy_class(data["settings"], data.pop("__analysis_settings__"))

        return handler(data)


class OnComplete(str, Enum):
    """Action to perform after running an OpticStudio analysis.

    This `Enum` can be passed to analysis methods in `zospy.analyses`.

    Attributes
    ----------
    Close : str
        Close the analysis.
    Release : str
        Keep the analysis open, but not active.
    Sustain : str
        Keep the analysis open and active.

    Examples
    --------
    Run a System Data analysis and keep the analysis open:

    >>> from zospy.analyses import OnComplete
    >>> from zospy.analyses.reports import system_data
    >>> result = system_data(oss, OnComplete.Sustain)
    """

    Close = "Close"
    """Close the analysis."""

    Release = "Release"
    """Keep the analysis open, but not active."""

    Sustain = "Sustain"
    """Keep the analysis open and active."""


class _ValidatedSetter:
    """Wrapper class that only allows to set existing properties."""

    __slots__ = ("_obj",)

    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in self.__slots__:
            super().__setattr__(name, value)
        elif hasattr(self._obj, name):
            setattr(self._obj, name, value)
        else:
            raise AttributeError(f"'{type(self._obj).__name__}' object has no attribute '{name}'")


_ValidatedSetterType = TypeVar("_ValidatedSetterType")


def _validated_setter(obj: _ValidatedSetterType) -> _ValidatedSetterType:
    """Wrap an object to only allow setting existing properties.

    Helper function that retains the original object's type information.

    Parameters
    ----------
    obj : Any
        The object to wrap.
    """
    return _ValidatedSetter(obj)


class Analysis:
    """OpticStudio analysis.

    This class wraps ZOSAPI analysis objects to provide direct access to its settings and results.
    All properties and methods of the ZOSAPI analysis object are available through this class.
    """

    def __init__(self, analysis: _ZOSAPI.Analysis.IA_):
        """Zemax OpticStudio Analysis with full access to its Settings and Results attributes.

        Parameters
        ----------
        analysis : ZOSAPI.Analysis.IA_
            analysis object
        """
        self._analysis = _validated_setter(analysis)

    @property
    def Settings(self) -> _ZOSAPI.Analysis.Settings.IAS_:  # noqa: N802
        """Analysis-specific settings."""
        return _validated_setter(self._analysis.GetSettings())

    @property
    def Results(self) -> _ZOSAPI.Analysis.Data.IAR_:  # noqa: N802
        """Analysis results."""
        return self._analysis.GetResults()

    def get_field(self) -> int | Literal["All"]:
        """Get the field value from the analysis settings.

        Returns
        -------
        int | Literal["All"]
            Either the field number, or 'All' if field was set to 'All'.
        """
        field_number = self.Settings.Field.GetFieldNumber()

        return "All" if field_number == 0 else field_number

    def set_field(self, value: int | Literal["All"]):
        """Set the field value in the analysis settings.

        Parameters
        ----------
        value : int | Literal["All"]
            The value to which the field should be set. Either int or str. Accepts only 'All' as string.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When 'value' is not integer or string. When it is a string, it also raises an error when the string
            does not equal 'All'.
            When 'value' is not accepted by the analysis as field specification.

        Warnings
        --------
        The ZOS-API handles invalid integer values without warning about this:

        - If selecting all fields is not possible, a value of `0` will instead select the first field;
        - If the value is greater than the number of fields, the last field will be selected.
        """
        if value == "All":
            message = self.Settings.Field.UseAllFields()
        elif isinstance(value, int):
            message = self.Settings.Field.SetFieldNumber(value)
        else:
            raise ValueError(f'Field value should be "All" or an integer, got {value}')

        if message is not None:
            raise ValueError(f"Could not set field value to {value}: {message.Text}")

    @property
    def header_data(self) -> list[str]:
        """Obtain the header data from an OpticStudio analysis.

        Returns
        -------
        list
            The header data.
        """
        return list(self.Results.HeaderData.Lines)

    @property
    def messages(self) -> list[AnalysisMessage]:
        """Obtain the messages from the analysis.

        Returns
        -------
        list[AnalysisMessage]
            A list of messages. Each item is a NamedTuple with names (ErrorCode, Message).
        """
        result = []

        for i in range(self.Results.NumberOfMessages):
            message = self.Results.GetMessageAt(i)
            error_code = str(message.ErrorCode)

            result.append(AnalysisMessage(error_code, message.Text))

        return result

    @property
    def metadata(self) -> AnalysisMetadata:
        """Obtain the metadata from the analysis.

        Returns
        -------
        AnalysisMetadata
            A named tuple containing the MetaData including 'DateTime', 'FeatureDescription', 'LensFile'
            and 'LensTitle'.
        """
        return AnalysisMetadata(
            system_datetime_to_datetime(self.Results.MetaData.Date),
            self.Results.MetaData.FeatureDescription,
            self.Results.MetaData.LensFile,
            self.Results.MetaData.LensTitle,
        )

    def get_wavelength(self) -> int | Literal["All"]:
        """Get the wavelength value from the analysis settings.

        Returns
        -------
        int | Literal["All"]
            Either the wavelength number, or 'All' if wavelength was set to 'All'.
        """
        wavelength = self.Settings.Wavelength.GetWavelengthNumber()

        return "All" if wavelength == 0 else wavelength

    def set_wavelength(self, value: int | Literal["All"]):
        """Set the wavelength value in the analysis settings.

        Parameters
        ----------
        value : int | Literal["All"]
            The value to which the wavelength should be set. Either int or str. Accepts only 'All' as string.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When 'value' is not integer or string. When it is a string, it also raises an error when the string does not
            equal 'All'.
            When 'value' is not accepted by the analysis as wavelength specification.

        Warnings
        --------
        The ZOS-API handles invalid integer values without warning about this:

        - If selecting all wavelengths is not possible, a value of `0` will instead select the first wavelength;
        - If the value is greater than the number of wavelengths, the last wavelength will be selected.
        """
        if value == "All":
            message = self.Settings.Wavelength.UseAllWavelengths()
        elif isinstance(value, int):
            message = self.Settings.Wavelength.SetWavelengthNumber(value)
        else:
            raise ValueError('Wavelength value should be "All" or an integer')

        if message is not None:
            raise ValueError(f"Could not set wavelength value to {value}: {message.Text}")

    def set_surface(self, value: int | Literal["Image", "Objective"]):
        """Set the surface value in the analysis settings.

        Parameters
        ----------
        value : int | Literal["Image", "Objective"]
            The value to which the surface should be set. Either int or str. Accepts only 'Image' or 'Objective' as
            string.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When 'value' is not integer or string. When it is a string, it also raises an error when the string does not
            equal 'Image' or 'Objective'.
            When 'value' is not accepted by the analysis as surface specification.

        Warnings
        --------
        The ZOS-API handles invalid integer values without warning about this:

        - If the supplied value is `0`, OpticStudio will base it selection based on the analysis. In some, it will
          select surface 0. In others, it will select a special surface (e.g. 'Image'). If neither is available, it
          selects the first available surface;
        - If the value is greater than the number of surfaces, the last surface will be selected.
        """
        if value == "Image":
            message = self.Settings.Surface.UseImageSurface()
        elif value == "Objective":
            message = self.Settings.Surface.UseObjectiveSurface()
        elif isinstance(value, int):
            message = self.Settings.Surface.SetSurfaceNumber(value)
        else:
            raise ValueError(f'Surface value should be "Image", "Objective" or an integer, got {value}')

        if message is not None:
            raise ValueError(f"Could not set surface value to {value}: {message.Text}")

    def get_text_output(self, txtoutfile: str, encoding: str):
        """Get the text output of the analysis.

        Parameters
        ----------
        txtoutfile : str
            Path to the text output file. The file will be created if it does not exist.
        encoding : str
            The encoding of the text file. The encoding used by OpticStudio can be obtained with
            `zospy.ZOS.get_txtfile_encoding`.
        """
        self.Results.GetTextFile(txtoutfile)

        with open(txtoutfile, encoding=encoding) as f:
            return f.read()

    def __getattr__(self, item):
        """Get an attribute from the analysis object.

        If the attribute is not found, it is retrieved from the ZOSAPI analysis object.
        """
        return getattr(self._analysis, item)

    def __dir__(self):
        """List the attributes of the Analysis wrapper and the ZOSAPI analysis object."""
        return sorted(set(super().__dir__()).union(dir(self._analysis)))


def new_analysis(
    oss: OpticStudioSystem,
    analysis_type: constants.Analysis.AnalysisIDM,
    *,
    settings_first: bool = True,
) -> Analysis:
    """Create a new analysis in OpticStudio.

    Parameters
    ----------
    oss : OpticStudioSystem
        The Zemax OpticStudio system
    analysis_type : zospy.constants.Analysis.AnalysisIDM
        Analysis type from `ZOSAPI.Analysis.AnalysisIDM`
    settings_first : bool
        Do not run the analysis immediately, which allows to adjust settings. Defaults to `True`.

    Returns
    -------
    analysis : Analysis

    Examples
    --------
    >>> import zospy as zp
    >>> new_analysis(oss, zp.constants.Analysis.AnalysisIDM.ZernikeStandardCoefficients)
    """
    analysis = (
        oss.Analyses.New_Analysis_SettingsFirst(analysis_type)
        if settings_first
        else oss.Analyses.New_Analysis(analysis_type)
    )
    return Analysis(analysis)


class BaseAnalysisWrapper(ABC, Generic[AnalysisData, AnalysisSettings]):
    """Base class for analysis wrappers.

    This class provides a common interface for all analysis wrappers. It defines the methods and properties that all
    analysis wrappers should implement.

    Attributes
    ----------
    TYPE : str
        The type of the analysis. This should match the `AnalysisIDM` constant in OpticStudio.
    _needs_config_file : bool
        Flag to indicate if the analysis requires a configuration file.
    _needs_text_output_file : bool
        Flag to indicate if the analysis requires a text output file.
    """

    TYPE: str = None
    MODE: Literal["Sequential", "Nonsequential"] | None = None

    # Flags to indicate if the analysis needs a configuration file or text output file
    _needs_config_file: bool = False
    _needs_text_output_file: bool = False

    def __init__(self, *, settings_kws: dict[str, Any] | None = None):
        """Create a new analysis wrapper.

        Settings can be changed by passing the settings as keyword arguments. Use the `with_settings` method to specify
        the settings using a settings object.

        Parameters
        ----------
        settings_kws : dict[str, Any]
            Arguments to set the settings of the analysis.

        Raises
        ------
        ValueError
            If `settings` is not a dataclass.
        """
        self._settings = self._default_settings()
        self.update_settings(settings_kws=settings_kws)

        self._config_file = None
        self._text_output_file = None

        self._oss = None
        self._analysis = None
        self._remove_config_file = False
        self._remove_text_output_file = False

    def __init_subclass__(
        cls,
        *,
        analysis_type: str | None = None,
        mode: Literal["Sequential", "Nonsequential"] | None = None,
        needs_config_file: bool = False,
        needs_text_output_file: bool = False,
        **kwargs,
    ):
        """Determine the settings type and class-level configuration of the analysis."""
        cls.TYPE = analysis_type
        cls.MODE = mode
        cls._needs_config_file = needs_config_file
        cls._needs_text_output_file = needs_text_output_file

        if not hasattr(cls, "_settings_type"):
            if hasattr(cls, "__orig_bases__"):
                base = cls.__orig_bases__[0]
                cls._settings_type: type[AnalysisSettings] = get_args(base)[1]
            else:
                cls._settings_type = type(None)  # TODO: change to NoneType when dropping support for Python 3.9

        super().__init_subclass__(**kwargs)

    def update_settings(
        self,
        *,
        settings: AnalysisSettings | None = None,
        settings_kws: dict[str, Any] | None = None,
    ) -> None:
        """Update the settings of the analysis using a settings object or keyword arguments.

        Settings can be specified as an object and as keyword arguments. If both are specified, the keyword arguments
        take precedence. If no settings are specified, the default settings are used. Furthermore, instead of using
        a reference to the settings object, a new settings object is created with the specified parameters. This is done
        to avoid modifying the original settings object.

        Parameters
        ----------
        settings : AnalysisSettings
            Analysis settings object.
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
    def _default_settings(cls) -> AnalysisSettings:
        """Get the default settings of the analysis.

        Returns
        -------
        AnalysisSettings
            The default settings.
        """
        return cls._settings_type() if cls._settings_type is not None else None

    @classmethod
    def with_settings(cls, settings: AnalysisSettings):
        """Create a new analysis with the specified settings.

        Parameters
        ----------
        settings : AnalysisSettings
            Settings of the analysis.

        Returns
        -------
        BaseAnalysisWrapper
            The analysis wrapper.
        """
        instance = cls()
        instance.update_settings(settings=settings)

        return instance

    @property
    def settings(self) -> AnalysisSettings:
        """Settings of the analysis."""
        return self._settings

    @property
    def config_file(self) -> Path | None:
        """Path to the temporary configuration file.

        This file is used to store the settings of the analysis and can only be set from the `run` method.

        Returns
        -------
        Path | None
            Path to the temporary configuration file.

        Raises
        ------
        ValueError
            If the analysis does not require a configuration file.
        """
        if not self._needs_config_file:
            raise ValueError("This analysis does not require a configuration file.")

        return self._config_file

    @property
    def text_output_file(self) -> Path | None:
        """Path to the temporary text output file.

        This file is used to store the text output of the analysis and can only be set from the `run` method.

        Returns
        -------
        Path | None
            Path to the temporary text output file.

        Raises
        ------
        ValueError
            If the analysis does not require a text output file.
        """
        if not self._needs_text_output_file:
            raise ValueError("This analysis does not require a text output file.")

        return self._text_output_file

    @property
    def oss(self) -> OpticStudioSystem:
        """The OpticStudio system. This property is set when the analysis is run."""
        if self._oss is None:
            raise ValueError("OpticStudioSystem has not been set.")

        return self._oss

    @property
    def analysis(self) -> Analysis | None:
        """The OpticStudio analysis object. This property is set when the analysis is run."""
        return self._analysis

    def get_text_output(self) -> str:
        """Get the text output of the analysis."""
        self.analysis.Results.GetTextFile(str(self.text_output_file))

        with open(self._text_output_file, encoding=self.oss.ZOS.get_txtfile_encoding()) as f:
            return f.read()

    def _create_analysis(self, *, settings_first=True):
        if self.analysis is not None and str(self.analysis.AnalysisType) == self.TYPE:
            return

        analysis_type = constants.process_constant(constants.Analysis.AnalysisIDM, self.TYPE)
        self._analysis = new_analysis(self.oss, analysis_type, settings_first=settings_first)

    @abstractmethod
    def run_analysis(self, *args, **kwargs) -> AnalysisData:
        """Run the analysis and return the results."""

    def _check_mode(self):
        if self.MODE is None:
            return

        if self.oss.Mode != self.MODE:
            raise ValueError(f"The analysis requires {self.MODE} mode, got {self.oss.Mode}.")

    @staticmethod
    def _create_tempfile(path: Path | None, suffix: str) -> (Path, bool):
        if path is None:
            fd, path = mkstemp(suffix=suffix, prefix="zospy_")
            os.close(fd)
            clean_file = True
        else:
            if not path.suffix == suffix:
                raise ValueError(f"File path should end with '{suffix}'.")

            clean_file = False

        return Path(path), clean_file

    def _complete(self, oncomplete: OnComplete = OnComplete.Close) -> None:
        """Completes the analysis by either closing, releasing or sustaining it."""
        if oncomplete == OnComplete.Close:
            self.analysis.Close()
            self._analysis = None
        elif oncomplete == OnComplete.Release:
            self.analysis.Release()
            self._analysis = None
        elif oncomplete == OnComplete.Sustain:
            return
        else:
            raise ValueError(f"oncomplete should be a member of zospy.analyses.base.OnComplete, got {oncomplete}")

    def run(
        self,
        oss: OpticStudioSystem,
        config_file: str | Path | None = None,
        text_output_file: str | Path | None = None,
        oncomplete: OnComplete | Literal["Close", "Release", "Sustain"] = "Close",
    ) -> AnalysisResult[AnalysisData, AnalysisSettings]:
        """Run the analysis and return the results.

        This method opens the analysis in OpticStudio and creates temporary files if needed. After running the analysis,
        the temporary files are removed and the analysis is closed, released, or sustained based on `oncomplete`.

        The `config_file` is ignored if self._needs_config_file is `False`.
        The `text_output_file` is ignored if self._needs_text_output_file is `False`.

        Parameters
        ----------
        oss : OpticStudioSystem
            The OpticStudio system.
        config_file : str | Path | None
            Path to the configuration file. If `None`, a temporary file will be created.
        text_output_file : str | Path | None
            Path to the text output file. If `None`, a temporary file will be created.
        oncomplete : OnComplete | Literal["Close", "Release", "Sustain"]
            Action to perform after running the analysis. If "Close", the analysis will be closed. If "Release", the
            analysis will be kept open but not active. If "Sustain", the analysis will be kept open and active.

        Returns
        -------
        AnalysisResult
            The analysis results.
        """
        self._oss = weakref.proxy(oss)
        self._check_mode()
        self._create_analysis()

        if self._needs_config_file:
            self._config_file, self._remove_config_file = self._create_tempfile(config_file, ".CFG")

        if self._needs_text_output_file:
            self._text_output_file, self._remove_text_output_file = self._create_tempfile(text_output_file, ".txt")

        data = self.run_analysis()

        result = AnalysisResult(
            data,
            settings=self.settings,
            metadata=self.analysis.metadata,
            header=self.analysis.header_data,
            messages=self.analysis.messages,
        )

        if self._remove_config_file:
            os.remove(self._config_file)

        if self._remove_text_output_file:
            os.remove(self._text_output_file)

        self._complete(OnComplete(oncomplete))

        return result

    def parse_output(
        self,
        grammar: str,
        transformer: type[Transformer],
        result_type: type[AnalysisData],
    ) -> AnalysisData:
        """Parse the text output of the analysis."""
        parser = load_grammar(grammar)
        parse_result = parse(self.get_text_output(), parser, transformer)

        return cast(result_type, result_type(**parse_result))

    @staticmethod
    def _process_data_series_or_grid(data: list[pd.DataFrame]) -> pd.DataFrame | None:
        if len(data) == 0:
            return None

        if len(data) == 1:
            return data[0]

        return pd.concat(data, axis=1)

    def get_data_series(self) -> pd.DataFrame | None:
        """Get the data series from the analysis result.

        Returns
        -------
        pd.Series | None
            The data series from the analysis result, or None if there are no data series.
        """
        data = [
            zputils.unpack_dataseries(self.analysis.Results.DataSeries[i])
            for i in range(self.analysis.Results.NumberOfDataSeries)
        ]

        return self._process_data_series_or_grid(data)

    def get_data_grid(self, cell_origin: Literal["bottom_left", "center"] = "bottom_left") -> pd.DataFrame | None:
        """Get the data grids from the analysis result.

        Parameters
        ----------
        cell_origin : Literal["bottom_left", "center"]
            Defines how minx and miny are handled to determine coordinates. Either 'bottom_left' indicating that they
            are defining the bottom left of the grd cell, or 'center', indicating that they provide the center of the
            grid cell. Defaults to 'bottom_left'.

        Returns
        -------
        pd.DataFrame | None
            The data grids from the analysis result, or None if there are no data grids.
        """
        data = [
            zputils.unpack_datagrid(self.analysis.Results.DataGrids[i], cell_origin=cell_origin)
            for i in range(self.analysis.Results.NumberOfDataGrids)
        ]

        return self._process_data_series_or_grid(data)

    def __call__(self, oss: OpticStudioSystem, *args, **kwargs):
        """Run the analysis and return the results."""
        return self.run(oss, *args, **kwargs)
