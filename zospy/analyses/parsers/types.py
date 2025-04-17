"""Data types for analysis result and settings objects."""

from __future__ import annotations

import logging
from operator import attrgetter
from typing import TYPE_CHECKING, Annotated, Any, Generic, Literal, NamedTuple, Optional, TypeVar, Union

from numpy import array, ndarray
from pandas import DataFrame
from pydantic import Field
from pydantic.dataclasses import dataclass
from pydantic_core import CoreSchema, PydanticCustomError, core_schema

from zospy.api import constants

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler

__all__ = ("UnitField", "ValidatedDataFrame", "ValidatedNDArray", "WavelengthNumber", "FieldNumber", "ZOSAPIConstant")


Value = TypeVar("Value")


@dataclass
class UnitField(Generic[Value]):
    """A field with a unit."""

    value: Value
    unit: str


class ValidatedDataFrameAnnotation:
    """Pydantic validation and serialization for Pandas DataFrames."""

    @staticmethod
    def _validate_dataframe(value: dict | DataFrame) -> DataFrame:
        if isinstance(value, dict):
            try:
                return DataFrame.from_dict(value, orient="tight")
            # Pandas can raise a KeyError if the dictionary was created with a different `orient`
            except (KeyError, ValueError) as e:
                raise PydanticCustomError(
                    "invalid_dataframe",
                    "Cannot convert dictionary to DataFrame: {value}",
                    {"value": value},
                ) from e

        return value

    @staticmethod
    def _serialize_dataframe(value: DataFrame) -> dict:
        return value.to_dict(orient="tight")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        schema = core_schema.json_or_python_schema(
            json_schema=core_schema.dict_schema(),
            python_schema=core_schema.union_schema(
                [core_schema.is_instance_schema(DataFrame), core_schema.dict_schema()]
            ),
        )

        serializer = core_schema.plain_serializer_function_ser_schema(
            cls._serialize_dataframe, when_used="json-unless-none"
        )

        return core_schema.no_info_after_validator_function(
            cls._validate_dataframe,
            schema,
            serialization=serializer,
        )


ValidatedDataFrame = Annotated[DataFrame, ValidatedDataFrameAnnotation]


class ValidatedNDArrayAnnotation:
    """Pydantic validation and serialization for Numpy arrays."""

    @staticmethod
    def _serialize_ndarray(value: ndarray) -> list:
        return value.tolist()

    @staticmethod
    def _validate_ndarray(value: list | ndarray) -> ndarray:
        if isinstance(value, list):
            try:
                return array(value)
            except ValueError as e:
                raise PydanticCustomError(
                    "invalid_ndarray",
                    "Cannot convert list to ndarray: {value}",
                    {"value": value},
                ) from e

        return value

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        schema = core_schema.json_or_python_schema(
            json_schema=core_schema.list_schema(),
            python_schema=core_schema.union_schema(
                [core_schema.is_instance_schema(ndarray), core_schema.list_schema()]
            ),
        )

        serializer = core_schema.plain_serializer_function_ser_schema(
            cls._serialize_ndarray, when_used="json-unless-none"
        )

        return core_schema.no_info_after_validator_function(
            cls._validate_ndarray,
            schema,
            serialization=serializer,
        )


ValidatedNDArray = Annotated[ndarray, ValidatedNDArrayAnnotation]

ZospyConstantType = TypeVar("ZospyConstantType")


class ZOSAPIConstantAnnotation:
    """Pydantic validation and serialization for ZOSAPI constants."""

    def __init__(self, enum: str):
        self.enum = enum

    def _validate_constant(self, value: ZospyConstantType | str) -> ZospyConstantType:
        try:
            constant = attrgetter(self.enum)(constants)
        except AttributeError:
            logging.warning(f"Constant {self.enum} not found in zospy.constants")
            return None

        return constants.process_constant(constant, value)

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> any:
        """Validate ZOSAPI constants."""
        schema = core_schema.json_or_python_schema(
            json_schema=core_schema.any_schema(),
            python_schema=core_schema.any_schema(),
        )

        serializer = core_schema.plain_serializer_function_ser_schema(str, when_used="json-unless-none")

        return core_schema.no_info_after_validator_function(self._validate_constant, schema, serialization=serializer)


def ZOSAPIConstant(enum: str) -> type[str]:  # noqa: N802
    """Pydantic validation and serialization for ZOSAPI constants."""
    return Annotated[Optional[str], ZOSAPIConstantAnnotation(enum)]


WavelengthNumber = Union[Literal["All"], Annotated[int, Field(gt=0)]]
FieldNumber = Union[Literal["All"], Annotated[int, Field(gt=0)]]


class Coordinate(NamedTuple):
    """Two-dimensional coordinate.

    Attributes
    ----------
    x : float
        X coordinate.
    y : float
        Y coordinate.
    """

    x: float
    y: float
