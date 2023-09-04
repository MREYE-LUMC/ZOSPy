"""Base functionality for analyses."""

from __future__ import annotations

import copy
import json
from collections.abc import MutableMapping
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from enum import Enum
from importlib import import_module
from types import SimpleNamespace
from typing import Any

import numpy as np
import pandas as pd

from zospy.api import _ZOSAPI, constants
from zospy.utils.clrutils import system_datetime_to_datetime
from zospy.zpcore import OpticStudioSystem


def _pprint(d, indent=0):
    """Pretty print an attribute dict."""
    items = []
    for key, value in sorted(d.items(), key=lambda x: str(x[0])):
        if isinstance(key, str):
            strkey = f"'{key}'"
        else:
            strkey = str(key)
        if isinstance(value, MutableMapping):
            items.append(" " * indent + strkey + ":")
            items.extend(_pprint(value, indent + 2))
        else:
            items.append(" " * indent + strkey + ": " + repr(value))
    return items


def _convert_dicttype(dictionary, newtype=dict, convert_nested=True, method="deepcopy"):
    """Packs a nested dictionary to a one-level dictionary with tuple keys.

    Parameters
    ----------
    dictionary: dict
        A dictionary or dictionary subtype, optionally with nested dictionaries
    newtype: type
        The new dictionary (sub)type
    convert_nested: bool
        Whether nested dictionaries should be converted as well. Defaults to True
    method: str
        The method used to copy values. One of 'deepcopy', 'copy' and 'assign'. Defaults to 'deepcopy'

    Returns
    -------
    object
        The converted dictionary type
    """
    ret = newtype()
    for key, value in dictionary.items():
        if convert_nested and isinstance(value, dict):
            ret[key] = _convert_dicttype(value, newtype=newtype, convert_nested=convert_nested, method=method)
        else:
            if method == "deepcopy":
                ret[key] = copy.deepcopy(value)
            elif method == "copy":
                ret[key] = copy.copy(value)
            elif method == "assign":
                ret[key] = value
            else:
                raise ValueError()
    return ret


class _AnalysisResultJSONEncoder(json.JSONEncoder):
    """Serializes an `AnalysisResult` object to JSON."""

    def __init__(self, sort_keys=False, indent=4, **kwargs):
        super().__init__(sort_keys=sort_keys, indent=indent, **kwargs)

    def default(self, o: Any) -> Any:
        if isinstance(o, pd.DataFrame):
            return {"__type__": self._type_name(o), "data": o.to_dict(orient="tight")}

        if isinstance(o, pd.Series):
            if isinstance(o.index, pd.MultiIndex):
                return {
                    "__type__": self._type_name(o),
                    "data": o.to_frame().to_dict(orient="tight"),
                    "__multi_index__": True,
                }

            return {"__type__": self._type_name(o), "data": o.to_dict()}

        if isinstance(o, np.ndarray):
            return {"__type__": self._type_name(o), "data": o.tolist()}

        if is_dataclass(o):
            return {
                "__type__": "dataclass",
                "__type_name__": self._type_name(o),
                "__type_module__": type(o).__module__,
                "data": asdict(o),
            }

        if isinstance(o, datetime):
            return {"__type__": self._type_name(o), "data": o.isoformat()}

        return super().default(o)

    def encode(self, o: Any) -> str:
        if isinstance(o, AttrDict):
            o = self._process_attrdict(o)

        return super().encode(o)

    def _process_attrdict(self, o: AttrDict) -> dict:
        object_type = self._type_name(o)

        if any(isinstance(v, AttrDict) for v in o.values()):
            o = {k: (self._process_attrdict(v) if isinstance(v, AttrDict) else v) for k, v in o.items()}

        return {"__type__": object_type, "data": dict(o)}

    @staticmethod
    def _type_name(o: Any) -> str:
        return type(o).__name__


class _AnalysisResultJSONDecoder(json.JSONDecoder):
    """Reconstructs an `AnalysisResult` object from its JSON representation."""

    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    @staticmethod
    def object_hook(o: dict) -> Any:
        if object_type := o.get("__type__"):
            if object_type == "DataFrame":
                return pd.DataFrame.from_dict(o["data"], orient="tight")

            if object_type == "Series":
                if "__multi_index__" in o:
                    return pd.DataFrame.from_dict(o["data"], orient="tight").iloc[:, 0]

                return pd.Series(o["data"])

            if object_type == "ndarray":
                return np.array(o["data"])

            if object_type == "dataclass":
                return _AnalysisResultJSONDecoder._process_dataclass(o)

            if object_type == "AttrDict":
                return AttrDict.from_dict(o["data"])

            if object_type == "datetime":
                return datetime.fromisoformat(o["data"])

            return o["data"]

        return o

    @staticmethod
    def _process_dataclass(o: dict) -> Any:
        module = o["__type_module__"]
        name = o["__type_name__"]

        if module.startswith("zospy.analyses"):
            try:
                m = import_module(module)
                return getattr(m, name)(**o["data"])
            except (ModuleNotFoundError, AttributeError):
                return SimpleNamespace(**o["data"])

        return SimpleNamespace(**o["data"])


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


class AttrDict(dict):
    """Basically a dict with attribute access.

    Equal to scipy's OptimizeResult (https://github.com/scipy/scipy/blob/v1.6.3/scipy/optimize/optimize.py#L82-L138).
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            return "\n".join(_pprint(self))
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list([key for key in self.keys() if str(key).isidentifier()]) + dir(dict)

    def to_dict(self, convert_nested=True, method="deepcopy"):
        """Convert the AttrDict to a standard dict.

        Parameters
        ----------
        convert_nested: bool
            Whether nested dictionaries should be converted as well. Defaults to True
        method: str
            The method used to copy values. One of 'deepcopy', 'copy' and 'assign'. Defaults to 'deepcopy'

        Returns
        -------
        dict
            The AttrDict as standard Dict
        """
        return _convert_dicttype(self, newtype=dict, convert_nested=convert_nested, method=method)

    @classmethod
    def from_dict(cls, dictionary, convert_nested=True, method="deepcopy"):
        """Create an AttrDict from a standard dict.

        Parameters
        ----------
        dictionary: dict
            The dictionary that is to be converted
        convert_nested: bool
            Whether nested dictionaries should be converted as well. Defaults to True
        method: str
            The method used to copy values. One of 'deepcopy', 'copy' and 'assign'. Defaults to 'deepcopy'

        Returns
        -------
        AttrDict
            The converted AttrDict
        """
        return _convert_dicttype(dictionary, newtype=cls, convert_nested=convert_nested, method=method)


class AnalysisResult(AttrDict):
    def __init__(
        self,
        analysistype: str,
        data: Any = None,
        settings: pd.Series = None,
        metadata: AnalysisMetadata = None,
        headerdata: list[str] = None,
        messages: list[AnalysisMessage] = None,
        **kwargs,
    ):
        """A class designed to hold an OpticStudio analysis.

        The class is basically a dict with attribute level access. However, for an AnalysisResult, certain keys are
        often present and thus automatically set.

        Parameters
        ----------
        analysistype: str
            The type of analysis that has been performed. Will be assigned to AnalysisResult.AnalysisType (also
            available through AnalysisResult['AnalysisType'].
        data: Any, optional
            The analysis data, can be any of the native python datatypes, a pd.Series, pd.DataFrame, np.ndarray or
            AnalysisData. Will be assigned to AnalysisResult.Data (also available through AnalysisResult['Data'].
            Defaults to None.
        settings: pd.Series, optional
            The analysis settings. Will be assigned to AnalysisResult.Settings (also available through
            AnalysisResult['Settings']. Defaults to None.
        metadata: AnalysisMetadata, optional
            The analysis metadata. Will be assigned to AnalysisResult.MetaData (also available through
            AnalysisResult['MetaData']. Defaults to None.
        headerdata: list[str], optional
            The analysis headerdata. Will be assigned to AnalysisResult.HeaderData (also available through
            AnalysisResult['HeaderData']. Defaults to None.
        messages: list[AnalysisMessage], optional:
            The analysis messages. Will be assigned to AnalysisResult.Messages (also available through
            AnalysisResult['Messages']. Defaults to None.
        kwargs:
            Any supplied kwarg will be assigned as an attribute (also available as AnalysisResult[kwarg]. Note that
            'AnalysisType', 'Data', 'Settings' 'MetaData', 'HeaderData' and 'Messages' are not available to be set.


        Returns
        -------
        AnalysisResult:
            A dict with attribute-like access

        Raises
        ------
        SyntaxError:
            If any of the following kwargs is specified 'AnalysisType', 'Data', 'Settings' 'MetaData', 'HeaderData' or
            'Messages'. These are to be set through the default arguments.
        """
        super().__init__(
            AnalysisType=analysistype,
            Data=data,
            Settings=settings,
            MetaData=metadata,
            HeaderData=headerdata,
            Messages=messages,
            **kwargs,
        )

    def to_json(self) -> str:
        """Serializes the analysis result to JSON.

        Returns
        -------
        json_string: str
            A JSON representation of the analysis result.
        """
        return _AnalysisResultJSONEncoder().encode(self)

    @classmethod
    def from_json(cls, json_string: str) -> AnalysisResult:
        """Creates an `AnalysisResult` object from a JSON string.

        This method should only be used with JSON strings created with `AnalysisResult.to_json`.

        Known limitations
        =================

        - Pandas `Series` with a numeric index are not compatible with JSON, which only allows string keys. The
        reconstructed value will therefore not equal the original value. Use string indices Numpy arrays where possible.
        - Support for custom attributes is limited and requires

        Parameters
        ----------
        json_string : str
            JSON representation of an `AnalysisResult` object, created with `to_json`.

        Returns
        -------
        result : AnalysisResult
            The reconstructed `AnalysisResult`.
        """
        parsed_json = _AnalysisResultJSONDecoder().decode(json_string)

        result = cls(analysistype="")
        result.update(parsed_json)

        return result


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
        self._analysis = analysis.__implementation__

    @property
    def Settings(self) -> _ZOSAPI.Analysis.Settings.IAS_:
        """Analysis-specific settings."""
        return self._analysis.GetSettings().__implementation__

    @property
    def Results(self) -> _ZOSAPI.Analysis.Data.IAR_:
        """Analysis results."""
        return self._analysis.GetResults().__implementation__

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
            result.Analysis = self
            return result

        raise ValueError(f"oncomplete should be a member of zospy.analyses.base.OnComplete, got {oncomplete}")

    def set_field(self, value: int | str):
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

    def get_field(self) -> int | str:
        """Gets the wavelength value of the analysis.

        Returns
        -------
        int | str
            Either the field number, or 'All' if field was set to 'All'.

        """
        field_number = self.Settings.Field.GetFieldNumber()

        return "All" if field_number == 0 else field_number

    def get_header_data(self) -> list[str]:
        """Obtains the header data from an OpticStudio analysis.

        Returns
        -------
        list
            The header data.
        """
        return list(self.Results.HeaderData.Lines)

    def get_messages(self) -> list[AnalysisMessage]:
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

    def get_metadata(self) -> AnalysisMetadata:
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

    def set_wavelength(self, value: int | str):
        """Sets the wavelength value for the analysis.

        Parameters
        ----------
        value: int | str
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

    def get_wavelength(self) -> int | str:
        """Gets the wavelength value of the analysis.

        Returns
        -------
        int | str
            Either the wavelength number, or 'All' if wavelength was set to 'All'.

        """
        wavelength = self.Settings.Wavelength.GetWavelengthNumber()

        return "All" if wavelength == 0 else wavelength

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

    def __getattr__(self, item):
        return getattr(self._analysis, item)


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
    >>> new_analysis(oss, zp.constants.Analysis.AnalysisIDM.ZernikeStandardCoefficients)
    """
    analysis = (
        oss.Analyses.New_Analysis_SettingsFirst(analysis_type)
        if settings_first
        else oss.Analyses.New_Analysis(analysis_type)
    )
    return Analysis(analysis)
