from __future__ import annotations

import importlib.resources
import sys
from functools import lru_cache
from typing import Any

from lark import Lark, Transformer
from lark.visitors import merge_transformers
from pydantic.dataclasses import dataclass

from zospy.analyses.new.parsers.transformers import ZospyTransformer

if sys.version_info < (3, 10):
    GRAMMARS = importlib.resources.files("zospy.analyses.new.parsers").joinpath("grammars")
else:
    GRAMMARS = importlib.resources.files("zospy.analyses.new.parsers.grammars")


@lru_cache
def load_grammar(name: str) -> Lark:
    grammar_file = GRAMMARS.joinpath(f"{name}.lark")

    if not grammar_file.is_file():
        raise FileNotFoundError(f"Grammar file {name}.lark not found")

    return Lark.open(str(grammar_file), start="start", parser="earley")


def parse(text: str, parser: Lark, transformer: type[Transformer]) -> dict[str, dict[list[int | float], Any]]:
    merged_transformer = merge_transformers(transformer(), zospy=ZospyTransformer())

    return merged_transformer.transform(parser.parse(text))


@dataclass
class UnitField:
    value: float
    unit: str
