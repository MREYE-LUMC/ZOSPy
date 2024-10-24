from __future__ import annotations

import os
import weakref
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from enum import Enum
from importlib import import_module
from pathlib import Path
from tempfile import mkstemp
from typing import TYPE_CHECKING, Generic, Literal, TypedDict, TypeVar, cast

import numpy as np
import pandas as pd
import pydantic
from pydantic import (
    RootModel,
    TypeAdapter,
    field_serializer,
    model_serializer,
    model_validator,
)
from pydantic_core.core_schema import SerializerFunctionWrapHandler

from zospy.analyses.new.parsers import load_grammar, parse
from zospy.analyses.new.parsers.types import ValidatedDataFrame
from zospy.api import _ZOSAPI, constants
from zospy.utils.clrutils import system_datetime_to_datetime
from zospy.zpcore import OpticStudioSystem

if TYPE_CHECKING:
    from lark import Transformer


__all__ = ("Analysis", "AnalysisResult", "AnalysisWrapper", "OnComplete", "new_analysis")


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
    data_type: Literal["dataframe", "ndarray", "dataclass"]
    name: str | None = None
    module: str | None = None


def _serialize_analysis_data_type(data: AnalysisData) -> _TypeInfo:
    if isinstance(data, pd.DataFrame):
        return {"data_type": "dataframe"}

    if isinstance(data, np.ndarray):
        return {"data_type": "ndarray"}

    if is_dataclass(data):
        return {"data_type": "dataclass", "name": type(data).__name__, "module": type(data).__module__}

    raise ValueError(f"Cannot serialize data type: {type(data)}")


def _deserialize_dataclass(data: dict, typeinfo: _TypeInfo) -> AnalysisData:
    if typeinfo["module"].startswith("zospy.analyses"):
        try:
            m = import_module(typeinfo["module"])
            t = getattr(m, typeinfo["name"])

            return TypeAdapter(t).validate_python(data)
        except (ModuleNotFoundError, AttributeError):
            return data

    return data


def _deserialize_analysis_data(data: dict | list, typeinfo: _TypeInfo) -> AnalysisData:
    if typeinfo["data_type"] == "dataframe":
        return pd.DataFrame.from_dict(data, orient="tight")

    if typeinfo["data_type"] == "ndarray":
        return np.array(data)

    if typeinfo["data_type"] == "dataclass":
        return _deserialize_dataclass(data, typeinfo)

    raise ValueError(f"Cannot deserialize data type: {typeinfo['data_type']}")


@pydantic.dataclasses.dataclass(frozen=True)
class AnalysisResult(Generic[AnalysisData, AnalysisSettings]):
    """Zemax OpticStudio analysis result."""

    data: AnalysisData
    settings: AnalysisSettings
    metadata: AnalysisMetadata
    header: list[str] | None = None
    messages: list[AnalysisMessage] | None = None

    def to_json(self):
        return RootModel(self).model_dump_json(indent=4)

    @classmethod
    def from_json(cls, data: str):
        return TypeAdapter(cls).validate_json(data)

    @field_serializer("data", mode="wrap", when_used="json")
    def _serialize_data(self, value: AnalysisData, nxt: SerializerFunctionWrapHandler, info):
        if isinstance(value, pd.DataFrame):
            return TypeAdapter(ValidatedDataFrame).dump_python(value, mode="json")

        if isinstance(value, np.ndarray):
            return value.tolist()

        return nxt(value)

    @model_serializer(mode="wrap", when_used="json")
    def _serialize_types(self, nxt: SerializerFunctionWrapHandler):
        data = nxt(self)
        data["__analysis_data__"] = _serialize_analysis_data_type(self.data)
        data["__analysis_settings__"] = {
            "data_type": "dataclass",
            "name": type(self.settings).__name__,
            "module": type(self.settings).__module__,
        }

        return data

    @model_validator(mode="wrap")
    @classmethod
    def _deserialize_types(cls, data: any, handler):
        if isinstance(data, dict):
            if "__analysis_data__" in data:
                data["data"] = _deserialize_analysis_data(data["data"], data.pop("__analysis_data__"))
            if "__analysis_settings__" in data:
                data["settings"] = _deserialize_dataclass(data["settings"], data.pop("__analysis_settings__"))

        return handler(data)


class OnComplete(str, Enum):
    """
    Action to perform after running an OpticStudio analysis.

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


class Analysis:
    def __init__(self, analysis: _ZOSAPI.Analysis.IA_):
        """
        Zemax OpticStudio Analysis with full access to its Settings and Results attributes.

        Parameters
        ----------
        analysis: ZOSAPI.Analysis.IA_
            analysis object
        """
        self._analysis = analysis

    @property
    def Settings(self) -> _ZOSAPI.Analysis.Settings.IAS_:
        """Analysis-specific settings."""
        return self._analysis.GetSettings()

    @property
    def Results(self) -> _ZOSAPI.Analysis.Data.IAR_:
        """Analysis results."""
        return self._analysis.GetResults()

    def complete(self, oncomplete: OnComplete | str, result: AnalysisResult) -> AnalysisResult:
        """Completes the analysis by either closing, releasing or sustaining it.

        Parameters
        ----------
        oncomplete: OnComplete | str
            Action to perform on completion.
        result: AnalysisResult
            Result of the analysis.

        Returns
        -------
        `result` if the analysis is closed or released, `result` extended with the `Analysis` object if the analysis
        is sustained.
        """
        oncomplete = OnComplete(oncomplete)

        if oncomplete == OnComplete.Close:
            self._analysis.Close()
            return result

        if oncomplete == OnComplete.Release:
            self._analysis.Release()
            return result

        if oncomplete == OnComplete.Sustain:
            raise NotImplementedError("Sustaining an analysis still needs to be implemented.")
            result.Analysis = self
            return result

        raise ValueError(f"oncomplete should be a member of zospy.analyses.base.OnComplete, got {oncomplete}")

    @property
    def field(self) -> int | str:
        """Gets the wavelength value of the analysis.

        Returns
        -------
        int | str
            Either the field number, or 'All' if field was set to 'All'.
        """
        field_number = self.Settings.Field.GetFieldNumber()

        return "All" if field_number == 0 else field_number

    @field.setter
    def field(self, value: int | str):
        """Sets the field value for the analysis.

        Parameters
        ----------
        value: int or str
            The value to which the field should be set. Either int or str. Accepts only 'All' as string.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When 'value' is not integer or string. When it is a string, it also raises an error when the string
            does not
            equal 'All'.
        """
        if value == "All":
            self.Settings.Field.UseAllFields()
        elif isinstance(value, int):
            self.Settings.Field.SetFieldNumber(value)
        else:
            raise ValueError(f'Field value should be "All" or an integer, got {value}')

    @property
    def header_data(self) -> list[str]:
        """Obtains the header data from an OpticStudio analysis.

        Returns
        -------
        list
            The header data.
        """
        return list(self.Results.HeaderData.Lines)

    @property
    def messages(self) -> list[AnalysisMessage]:
        """Obtains the messages from the analysis.

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
        """Obtains the metadata from the analysis.

        Returns
        -------
        AnalysisMetadata
            A named tuple containing the MetaData including 'DateTime', 'FeatureDescription', 'LensFile'
            and 'LensTitle'.
        """
        result = AnalysisMetadata(
            system_datetime_to_datetime(self.Results.MetaData.Date),
            self.Results.MetaData.FeatureDescription,
            self.Results.MetaData.LensFile,
            self.Results.MetaData.LensTitle,
        )

        return result

    @property
    def wavelength(self) -> int | Literal["All"]:
        """Gets the wavelength value of the analysis.

        Returns
        -------
        int | str
            Either the wavelength number, or 'All' if wavelength was set to 'All'.

        """
        wavelength = self.Settings.Wavelength.GetWavelengthNumber()

        return "All" if wavelength == 0 else wavelength

    @wavelength.setter
    def wavelength(self, value: int | Literal["All"]):
        """Sets the wavelength value for the analysis.

        Parameters
        ----------
        value: int | Literal["All"]
            The value to which the wavelength should be set. Either int or str. Accepts only 'All' as string.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            When 'value' is not integer or string. When it is a string, it also raises an error when the string does not
            equal 'All'.

        """
        if value == "All":
            self.Settings.Wavelength.UseAllWavelengths()
        elif isinstance(value, int):
            self.Settings.Wavelength.SetWavelengthNumber(value)
        else:
            raise ValueError('Wavelength value should be "All" or an integer')

    def set_surface(self, value: int | str):
        """Sets the surface value for the analysis.

        Parameters
        ----------
        value: int or str
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

        """
        if value == "Image":
            self.Settings.Surface.UseImageSurface()
        elif value == "Objective":
            self.Settings.Surface.UseObjectiveSurface()
        elif isinstance(value, int):
            self.Settings.Surface.SetSurfaceNumber(value)
        else:
            raise ValueError(f'Surface value should be "Image", "Objective" or an integer, got {value}')

    def get_text_output(self, txtoutfile: str, encoding: str):
        self.Results.GetTextFile(txtoutfile)

        with open(txtoutfile, "r", encoding=encoding) as f:
            output = f.read()

        return output

    def __getattr__(self, item):
        return getattr(self._analysis, item)

    def __dir__(self):
        return sorted(set(super().__dir__()).union(dir(self._analysis)))


def new_analysis(
    oss: OpticStudioSystem, analysis_type: constants.Analysis.AnalysisIDM, settings_first: bool = True
) -> Analysis:
    """
    Creates a new analysis in Zemax.

    Parameters
    ----------
    oss: OpticStudioSystem
        The Zemax OpticStudio system
    analysis_type: zospy.constants.Analysis.AnalysisIDM
        Analysis type from `ZOSAPI.Analysis.AnalysisIDM`
    settings_first: bool
        Do not run the analysis immediately, which allows to adjust settings. Defaults to `True`.

    Returns
    -------
    analysis: Analysis

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


class AnalysisWrapper(ABC, Generic[AnalysisData, AnalysisSettings]):
    TYPE: str = None

    # Flags to indicate if the analysis needs a configuration file or text output file
    _needs_config_file: bool = False
    _needs_text_output_file: bool = False

    def __init__(self, settings: AnalysisSettings, settings_arguments: dict[str, any]):
        self._init_settings(settings, settings_arguments)

        self._config_file = None
        self._text_output_file = None

        self._oss = None
        self._analysis = None
        self._remove_config_file = False
        self._remove_text_output_file = False

    def _init_settings(self, settings: AnalysisSettings, parameters: dict[str, any]):
        self._settings = settings

        if not is_dataclass(settings):
            raise ValueError("settings should be a dataclass.")

        for field in fields(settings):
            if field.name in parameters:
                setattr(self.settings, field.name, parameters[field.name])

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
        if self._oss is None:
            raise ValueError("OpticStudioSystem has not been set.")

        return self._oss

    @property
    def analysis(self) -> Analysis | None:
        return self._analysis

    def get_text_output(self) -> str:
        self.analysis.Results.GetTextFile(str(self.text_output_file))

        with open(self._text_output_file, "r", encoding=self.oss._ZOS.get_txtfile_encoding()) as f:
            output = f.read()

        return output

    def _create_analysis(self):
        if self.analysis is not None and self.analysis.TypeName == self.TYPE:
            return

        analysis_type = constants.process_constant(constants.Analysis.AnalysisIDM, self.TYPE)
        self._analysis = new_analysis(self.oss, analysis_type)

    @abstractmethod
    def run_analysis(self, *args, **kwargs) -> AnalysisData:
        pass

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
        self._oss = weakref.proxy(oss)
        self._create_analysis()

        if self._needs_config_file:
            self._config_file, self._remove_config_file = self._create_tempfile(config_file, ".CFG")

        if self._needs_text_output_file:
            self._text_output_file, self._remove_text_output_file = self._create_tempfile(text_output_file, ".txt")

        data = self.run_analysis(oss)

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
        self, grammar: str, transformer: type[Transformer], result_type: type[AnalysisData]
    ) -> AnalysisData:
        parser = load_grammar(grammar)
        parse_result = parse(self.get_text_output(), parser, transformer)

        return cast(result_type, result_type(**parse_result))

    def __call__(self, oss: OpticStudioSystem, *args, **kwargs):
        return self.run(oss, *args, **kwargs)
