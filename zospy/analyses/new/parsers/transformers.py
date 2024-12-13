from __future__ import annotations

from itertools import groupby
from typing import Any, NamedTuple, TypedDict, TypeVar

from lark import Discard, Transformer

from zospy.utils.pyutils import atox

FieldValue = TypeVar("FieldValue")


class SimpleField(NamedTuple):
    name: str
    value: FieldValue


class ParametricField(NamedTuple):
    parameters: int | float | tuple[int | float, ...]
    value: FieldValue


class UnitField(TypedDict):
    value: float
    unit: str


def atof(s: str) -> float:
    return float(s.replace(",", "."))


def group_parametric_fields(
    fields: list[SimpleField[ParametricField]],
) -> dict[str, dict[list[int | float], Any]]:
    result = {}

    for name, fields in groupby(fields, lambda field: field.name):
        result[name] = {field.value.parameters: field.value.value for field in fields}

    return result


class ZospyTransformer(Transformer):
    DATE = str
    INT = int
    UINT = int
    WORD = str

    def FLOAT(self, f: str) -> float:
        """Floating point number with localized decimal separator."""
        return atox(f, float)

    multi_string = " ".join

    def string_list(self, args) -> list[str]:
        """List of whitespace-separated strings."""
        return list(map(str, args))

    list = list

    def dict(self, args):
        """Kay-value mapping."""
        keys = map(lambda f: f.name, args)

        result = {}

        for is_parametric, fields in groupby(args, lambda field: isinstance(field.value, ParametricField)):
            if is_parametric:
                result.update(group_parametric_fields(fields))
            else:
                result.update({field.name: field.value for field in fields})

        return {k: result[k] for k in keys}

    def start(self, args):
        """The root of the parse tree."""
        return dict(args)

    def table(self, args):
        """A table with a header and one or more rows."""
        header, *rows = args

        return (header, rows)

    def field_group(self, args):
        """A group of fields under a common key."""
        name, fields = args

        return SimpleField(name, fields)

    def simple_field(self, args) -> SimpleField:
        """A simple field with a name and a value."""
        if len(args) == 2:
            return SimpleField(*args)

        if len(args) == 1:
            return SimpleField(args[0], None)

        return args

    def parametric_unit_field(self, args) -> SimpleField[ParametricField[UnitField]]:
        """A field with parameters and a unit."""
        name, parameters, value, unit = args

        return SimpleField(str(name), ParametricField(parameters, UnitField(value=value, unit=unit)))

    def unit_field(self, args) -> SimpleField[UnitField]:
        """A field with a unit."""
        name, value, unit = args

        return SimpleField(str(name), UnitField(value=value, unit=unit))

    def unit(self, args) -> str:
        """Unit of measurement."""
        return " ".join(args)

    def parametric_field(self, args) -> SimpleField[ParametricField]:
        """A field with parameters."""
        name, parameters, value = args

        return SimpleField(str(name), ParametricField(parameters, value))

    def field_name(self, name) -> str:
        """Field name."""
        return " ".join(name)

    def field_value(self, value):
        """Field value."""
        (value,) = value
        return value

    def field_parameters(self, args):
        """Field parameters."""
        if len(args) == 1:
            return args[0]

        return tuple(args)

    def text(self, args):
        """Text that can be ignored."""
        return Discard
