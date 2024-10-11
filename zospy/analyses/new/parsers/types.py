"""Data types for analysis result objects."""

from typing import Generic, TypeVar

from pydantic.dataclasses import dataclass

__all__ = ("UnitField",)


Value = TypeVar("Value")


@dataclass
class UnitField(Generic[Value]):
    value: Value
    unit: str
