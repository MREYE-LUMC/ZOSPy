from __future__ import annotations

from functools import lru_cache
from typing import Any

from lark import Lark, Transformer
from lark.visitors import merge_transformers
from pydantic.dataclasses import dataclass

from zospy.analyses.new.parsers.transformers import ZospyTransformer


@lru_cache
def load_grammar(name: str) -> Lark:
    try:
        return Lark.open_from_package(
            "zospy.analyses.new.parsers.grammars", f"{name}.lark", parser="earley", start="start"
        )
    except (FileNotFoundError, OSError, IOError) as e:
        raise FileNotFoundError(f"Grammar file {name}.lark not found") from e


def parse(text: str, parser: Lark, transformer: type[Transformer]) -> dict[str, dict[list[int | float], Any]]:
    merged_transformer = merge_transformers(transformer(), zospy=ZospyTransformer())

    return merged_transformer.transform(parser.parse(text))


@dataclass
class UnitField:
    value: float
    unit: str
