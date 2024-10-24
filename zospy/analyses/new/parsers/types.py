"""Data types for analysis result objects."""
from __future__ import annotations

from typing import Annotated, Generic, TypeVar

from numpy import array, ndarray
from pandas import DataFrame
from pydantic import GetCoreSchemaHandler
from pydantic.dataclasses import dataclass

__all__ = ("UnitField", "ValidatedDataFrame", "ValidatedNDArray")

from pydantic_core import CoreSchema, PydanticCustomError, core_schema

Value = TypeVar("Value")


@dataclass
class UnitField(Generic[Value]):
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
    def __get_pydantic_core_schema__(cls, source_type: any, handler: GetCoreSchemaHandler) -> CoreSchema:
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
    def __get_pydantic_core_schema__(cls, source_type: any, handler: GetCoreSchemaHandler) -> CoreSchema:
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
