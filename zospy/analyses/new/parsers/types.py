"""Data types for analysis result objects."""

from pydantic.dataclasses import dataclass
from typing import TypeVar, Generic


__all__ = ("UnitField",)


Value = TypeVar("Value")


@dataclass
class UnitField(Generic[Value]):
    value: Value
    unit: str
