"""Transformers and helper classes for parsing OpticStudio analysis output.

Provides the `ZospyTransformer` class for transforming common OpticStudio constructs into dictionaries.
"""

from __future__ import annotations

from itertools import groupby
from typing import Any, NamedTuple, TypedDict, TypeVar

from lark import Discard, Transformer

from zospy.utils.pyutils import atox

FieldValue = TypeVar("FieldValue")


class SimpleField(NamedTuple):
    """A simple field with a name and a value."""

    name: str
    value: FieldValue


class ParametricField(NamedTuple):
    """A field with parameters and a value.

    Should be used as a value for a `SimpleField`.
    """

    parameters: int | float | tuple[int | float, ...]
    value: FieldValue


class UnitField(TypedDict):
    """A field with a unit.

    Should be used as a value for a `SimpleField`.
    """

    value: float
    unit: str


def group_parametric_fields(
    parametric_fields: list[SimpleField[ParametricField]],
) -> dict[str, dict[list[int | float], Any]]:
    """Convert a list of parametric fields into a dictionary of dictionaries."""
    result = {}

    for name, fields in groupby(parametric_fields, lambda field: field.name):
        result[name] = {field.value.parameters: field.value.value for field in fields}

    return result


class ZospyTransformer(Transformer):
    """Parse tree transformations for common constructs in OpticStudio analysis output."""

    DATE = str
    WORD = str

    def INT(self, i: str) -> int:  # noqa: N802
        """Integer number."""
        return atox(i, int)

    def UINT(self, i: str) -> int:  # noqa: N802
        """Unsigned integer number."""
        return atox(i, int)

    def FLOAT(self, f: str) -> float:  # noqa: N802
        """Floating point number with localized decimal separator."""
        return atox(f, float)

    multi_string = " ".join

    def string_list(self, args) -> list[str]:
        """List of whitespace-separated strings."""
        return list(map(str, args))

    list = list

    def dict(self, args):
        """Transform a key-value mapping."""
        keys = (f.name for f in args)

        result = {}

        for is_parametric, fields in groupby(args, lambda field: isinstance(field.value, ParametricField)):
            if is_parametric:
                result.update(group_parametric_fields(fields))
            else:
                result.update({field.name: field.value for field in fields})

        return {k: result[k] for k in keys}

    def start(self, args):
        """Transform the root of the parse tree."""
        return dict(args)

    def table(self, args):
        """Transform a table with a header and one or more rows."""
        header, *rows = args

        return (header, rows)

    def tuple(self, args):
        """Transform a tuple of values."""
        return tuple(args)

    def field_group(self, args):
        """Transform a group of fields under a common key to a SimpleField."""
        name, fields = args

        return SimpleField(name, fields)

    def simple_field(self, args) -> SimpleField:
        """Transform a simple field with a name and a value."""
        if len(args) == 2:
            name, value = args
            return SimpleField(str(name), value)

        if len(args) == 1:
            return SimpleField(str(args[0]), None)

        return args

    def parametric_unit_field(self, args) -> SimpleField[ParametricField[UnitField]]:
        """Transform a field with parameters and a unit."""
        name, parameters, value, unit = args

        return SimpleField(str(name), ParametricField(parameters, UnitField(value=value, unit=unit)))

    def unit_field(self, args) -> SimpleField[UnitField]:
        """Transform a field with a unit."""
        name, value, unit = args

        return SimpleField(str(name), UnitField(value=value, unit=unit))

    def unit(self, args) -> str:
        """Transform a unit of measurement."""
        return " ".join(args)

    def parametric_field(self, args) -> SimpleField[ParametricField]:
        """Transform a field with parameters."""
        name, parameters, value = args

        return SimpleField(str(name), ParametricField(parameters, value))

    def field_name(self, name) -> str:
        """Transform a field name."""
        return " ".join(name)

    def field_value(self, value):
        """Transform a field value."""
        (value,) = value
        return value

    def field_parameters(self, args):
        """Transform field parameters."""
        if len(args) == 1:
            return args[0]

        return tuple(args)

    def text(self, args):  # noqa: ARG002
        """Discard text that can be ignored."""
        return Discard
