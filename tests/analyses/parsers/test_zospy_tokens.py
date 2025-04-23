from typing import Any

import pytest
from lark import Lark
from lark.load_grammar import FromPackageLoader
from lark.visitors import merge_transformers

from zospy.analyses.parsers.transformers import ParametricField, SimpleField, UnitField, ZospyTransformer
from zospy.api import config

zospy_grammar_loader = FromPackageLoader("zospy", ["analyses/parsers/grammars"])


class SingleTokenZospyTransformer(ZospyTransformer):
    def start(self, args):
        return args[0]


transformer = merge_transformers(SingleTokenZospyTransformer(), zospy=ZospyTransformer())


def load_token(token: str) -> Lark:
    grammar = f"""start: {token}

%import common.WS_INLINE
%import zospy.{token}
%ignore WS_INLINE
"""
    return Lark(grammar, parser="earley", start="start", import_paths=[zospy_grammar_loader])


def parse_token(token: str, text: str) -> Any:
    parser = load_token(token)

    return transformer.transform(parser.parse(text))


@pytest.mark.parametrize(
    "value",
    ["01-01-2021", "01/01/2024", "05.12.1234"],
)
def test_date(value):
    # Dates are returned as is
    assert parse_token("DATE", value) == value


@pytest.mark.parametrize(
    "value,expected,decimal_point",
    [
        # Point as decimal separator
        ("1.23", 1.23, "."),
        (".23", 0.23, "."),
        ("+1.234", 1.234, "."),
        ("-1.234", -1.234, "."),
        ("1.234e-2", 1.234e-2, "."),
        ("1.234e+2", 1.234e2, "."),
        ("1.234E-2", 1.234e-2, "."),
        ("1.234E+2", 1.234e2, "."),
        ("-1.234e-2", -1.234e-2, "."),
        ("-1.234e+2", -1.234e2, "."),
        ("-1.234E-2", -1.234e-2, "."),
        ("-1.234E+2", -1.234e2, "."),
        # Comma as decimal separator
        ("1,23", 1.23, ","),
        (",23", 0.23, ","),
        ("+1,234", 1.234, ","),
        ("-1,234", -1.234, ","),
        ("1,234e-2", 1.234e-2, ","),
        ("1,234e+2", 1.234e2, ","),
        ("1,234E-2", 1.234e-2, ","),
        ("1,234E+2", 1.234e2, ","),
        ("-1,234e-2", -1.234e-2, ","),
        ("-1,234e+2", -1.234e2, ","),
        ("-1,234E-2", -1.234e-2, ","),
        ("-1,234E+2", -1.234e2, ","),
        ("infinity", float("inf"), "."),
    ],
)
def test_float(value, expected, decimal_point, monkeypatch):
    monkeypatch.setattr(config, "DECIMAL_POINT", decimal_point)
    monkeypatch.setattr(config, "THOUSANDS_SEPARATOR", "")

    result = parse_token("FLOAT", value)
    assert isinstance(result, float)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("1", 1),
        ("+1", 1),
        ("-1", -1),
        ("1.23", 1.23),
        ("+1.23", 1.23),
        ("-1.23", -1.23),
        ("1.23e-2", 1.23e-2),
        ("1.23e+2", 1.23e2),
        ("1.23E-2", 1.23e-2),
        ("1.23E+2", 1.23e2),
        ("-1.23e-2", -1.23e-2),
        ("-1.23e+2", -1.23e2),
        ("-1.23E-2", -1.23e-2),
        ("-1.23E+2", -1.23e2),
    ],
)
def test_number(value, expected, monkeypatch):
    monkeypatch.setattr(config, "DECIMAL_POINT", ".")
    monkeypatch.setattr(config, "THOUSANDS_SEPARATOR", "")

    result = parse_token("_number", value)

    assert result == expected
    assert type(result) is type(expected)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Alice Bob Charlie", "Alice Bob Charlie"),
        ("Multiple  spaces", "Multiple spaces"),
        (" Leading space", "Leading space"),
        ("Trailing space ", "Trailing space"),
        ("  Leading and  trailing  spaces  ", "Leading and trailing spaces"),
        ("Tabs\tand\ttabs", "Tabs and tabs"),
    ],
)
def test_multi_string(value, expected):
    result = parse_token("multi_string", value)
    assert result == expected


def test_string_list():
    grammar = """start: value

!value: "abc" "def" /Test with space/ "ghi" -> string_list

%import common.WS_INLINE
%ignore WS_INLINE
"""

    parser = Lark(grammar, parser="earley", start="start")
    result = transformer.transform(parser.parse("abc def Test with space ghi"))

    assert result == ["abc", "def", "Test with space", "ghi"]


def test_list():
    grammar = """start: value

    value: INT+ -> list

    %import common.WS_INLINE
    %import zospy.INT
    %ignore WS_INLINE
    """

    parser = Lark(grammar, parser="earley", start="start", import_paths=[zospy_grammar_loader])
    result = transformer.transform(parser.parse("1 2 3 4 5"))

    assert result == [1, 2, 3, 4, 5]


@pytest.mark.parametrize(
    "value,decimal_point,expected",
    [
        ("1, 2", ",", (1, 2)),
        ("1,000, 1,000", ",", (1.000, 1.000)),
        ("1.2, 2.3", ".", (1.2, 2.3)),
        ("1,212, 2,30", ",", (1.212, 2.30)),
        ("1, 2, 3, 4", ".", (1, 2, 3, 4)),
        ("1, 2, 3, 4", ",", (1, 2, 3, 4)),
    ],
)
def test_tuple(value, decimal_point, expected, monkeypatch):
    monkeypatch.setattr(config, "DECIMAL_POINT", decimal_point)
    monkeypatch.setattr(config, "THOUSANDS_SEPARATOR", "")

    grammar = """start: tuple

    %import common.WS_INLINE
    %import zospy.tuple
    %ignore WS_INLINE
    """

    parser = Lark(grammar, parser="earley", start="start", import_paths=[zospy_grammar_loader])
    result = transformer.transform(parser.parse(value))

    assert result == expected


@pytest.fixture
def setup_field_test(monkeypatch):
    monkeypatch.setattr(config, "DECIMAL_POINT", ".")
    monkeypatch.setattr(config, "THOUSANDS_SEPARATOR", "")

    def setup(value):
        if not value.endswith("\n"):
            value += "\n"

        return value

    return setup


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Name: value", SimpleField("Name", "value")),
        ("Name with spaces: 123", SimpleField("Name with spaces", 123)),
        ("Name_with_underscores: 1.23", SimpleField("Name_with_underscores", 1.23)),
        ("Name-with-dashes: multi string", SimpleField("Name-with-dashes", "multi string")),
        ("Name (with parentheses): -1.23E-5", SimpleField("Name (with parentheses)", -1.23e-5)),
        ("Space before colon : 1.23", SimpleField("Space before colon", 1.23)),
        ("Tabs around colon\t:\t01-01-1970", SimpleField("Tabs around colon", "01-01-1970")),
        ("Dot-separated date: 01.01.1970", SimpleField("Dot-separated date", "01.01.1970")),
    ],
)
def test_simple_field(value, expected, setup_field_test):
    value = setup_field_test(value)

    result = parse_token("simple_field", value)

    assert result == expected
    assert isinstance(result.value, type(expected.value))


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Name 123: 1.23", SimpleField("Name", ParametricField(123, 1.23))),
        ("Double parameters 123 4.56: 7.89", SimpleField("Double parameters", ParametricField((123, 4.56), 7.89))),
        (
            "Negative parameters -3.14 -2: a meaningless string",
            SimpleField("Negative parameters", ParametricField((-3.14, -2), "a meaningless string")),
        ),
    ],
)
def test_parametric_field(value, expected, setup_field_test):
    value = setup_field_test(value)

    result: SimpleField[ParametricField] = parse_token("parametric_field", value)

    assert result == expected
    assert isinstance(result.value.value, type(expected.value.value))

    if isinstance(result.value.parameters, tuple):
        for r, e in zip(result.value.parameters, expected.value.parameters):
            assert isinstance(r, type(e))
    else:
        assert isinstance(result.value.parameters, type(expected.value.parameters))


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Length: 10m", SimpleField("Length", UnitField(value=10, unit="m"))),
        ("Weight: 5 kg", SimpleField("Weight", UnitField(value=5, unit="kg"))),
        (
            "Temperature: 100 space separated unit",
            SimpleField("Temperature", UnitField(value=100, unit="space separated unit")),
        ),
        ("Wavelength: 0.543 µm", SimpleField("Wavelength", UnitField(value=0.543, unit="µm"))),
        ("Something: 30 (parenthesized)", SimpleField("Something", UnitField(value=30, unit="parenthesized"))),
    ],
)
def test_unit_field(value, expected, setup_field_test):
    value = setup_field_test(value)

    result = parse_token("unit_field", value)

    assert result == expected
    assert isinstance(result.value, type(expected.value))


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "Transmission 123: 456 mm",
            SimpleField("Transmission", ParametricField(123, UnitField(value=456, unit="mm"))),
        ),
        ("Length 1 2: 3 m", SimpleField("Length", ParametricField((1, 2), UnitField(value=3, unit="m")))),
    ],
)
def test_parametric_unit_field(value, expected, setup_field_test):
    value = setup_field_test(value)

    result = parse_token("parametric_unit_field", value)

    assert result == expected
    assert isinstance(result.value.value, type(expected.value.value))

    if isinstance(result.value.parameters, tuple):
        for r, e in zip(result.value.parameters, expected.value.parameters):
            assert isinstance(r, type(e))
    else:
        assert isinstance(result.value.parameters, type(expected.value.parameters))


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Simple field : 1.23", SimpleField("Simple field", 1.23)),
        ("Parametric field 1 2: 3.14", SimpleField("Parametric field", ParametricField((1, 2), 3.14))),
        ("Unit field: 10 m", SimpleField("Unit field", UnitField(value=10, unit="m"))),
        (
            "Parametric unit field 1 2: 3 m",
            SimpleField("Parametric unit field", ParametricField((1, 2), UnitField(value=3, unit="m"))),
        ),
    ],
)
def test_field(value, expected, setup_field_test):
    value = setup_field_test(value)

    result = parse_token("_field", value)

    assert result == expected
    assert isinstance(result.value, type(expected.value))


FIELD_GROUP_VALUE = """Group key:
    Simple field : 1.23
    Parametric field 1 2: 3.14
    Parametric unit field 3.14 : 1.23 m
"""

FIELD_GROUP_GRAMMAR = r"""start: _fg

_fg: field_group{name, fields}
!name: "Group" "key" -> field_name
fields: _field+ -> dict

%import zospy (_field, field_group)
%import common.WS_INLINE
%ignore WS_INLINE
"""


def test_field_group(setup_field_test):  # noqa: ARG001
    parser = Lark(FIELD_GROUP_GRAMMAR, parser="earley", start="start", import_paths=[zospy_grammar_loader])

    result = transformer.transform(parser.parse(FIELD_GROUP_VALUE))

    assert result == SimpleField(
        "Group key",
        {
            "Simple field": 1.23,
            "Parametric field": {(1, 2): 3.14},
            "Parametric unit field": {3.14: {"value": 1.23, "unit": "m"}},
        },
    )


TABLE_VALUE = """Alice Bob Charlie
1 2.3 4 5.6
7 8.9 10 11.12
"""

TABLE_GRAMMAR = r"""start: _table

_table: table{header, row}
!header: "Alice" "Bob" "Charlie" -> string_list
row: _numbers -> list

%import zospy (_field, field_group, _numbers, table)
%import common.NEWLINE -> _NEWLINE
%import common.WS_INLINE
%ignore WS_INLINE
"""


def test_table(setup_field_test):  # noqa: ARG001
    parser = Lark(TABLE_GRAMMAR, parser="earley", start="start", import_paths=[zospy_grammar_loader])

    result = transformer.transform(parser.parse(TABLE_VALUE))

    assert result == (["Alice", "Bob", "Charlie"], [[1, 2.3, 4, 5.6], [7, 8.9, 10, 11.12]])


@pytest.mark.parametrize(
    "value, expected, tokens, expected_token",
    [
        ("1.23", 1.23, ["STRING", "FLOAT"], "FLOAT"),
        ("01-02-2023", "01-02-2023", ["STRING", "DATE"], "DATE"),
        ("01.02.2923", "01.02.2923", ["STRING", "DATE", "FLOAT"], "DATE"),
        ("Simple field : 123\n", SimpleField("Simple field", 123), ["STRING", "simple_field"], "simple_field"),
    ],
)
def test_token_precedence(value, expected, tokens, expected_token, setup_field_test):  # noqa: ARG001
    grammar = f"""start: _value _NEWLINE?

_value: {" | ".join(tokens)}

%import common.NEWLINE -> _NEWLINE
%import common.WS_INLINE
%import zospy ({", ".join(tokens)})
%ignore WS_INLINE
"""

    parser = Lark(grammar, parser="earley", start="start", import_paths=[zospy_grammar_loader])
    parse_result = parser.parse(value)
    result = transformer.transform(parse_result)

    assert result == expected
    if expected_token.isupper():
        # Token is a terminal
        assert parse_result.children[0].type == expected_token
    else:
        # Token is a rule
        assert str(parse_result.children[0].data) == expected_token
