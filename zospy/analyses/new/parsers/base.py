"""Base classes and functions for OpticStudio analysis output parsers."""

from __future__ import annotations

import importlib.resources
import sys
from functools import lru_cache
from typing import Any

from lark import Lark, Transformer
from lark.visitors import merge_transformers

from zospy.analyses.new.parsers.transformers import ZospyTransformer

if sys.version_info < (3, 10):
    GRAMMARS = importlib.resources.files("zospy.analyses.new.parsers").joinpath("grammars")
else:
    GRAMMARS = importlib.resources.files("zospy.analyses.new.parsers.grammars")


@lru_cache
def load_grammar(name: str) -> Lark:
    """Load a grammar file and return a Lark parser.

    Grammars are loaded from `zospy.analyses.new.parsers.grammars` package.
    Grammar file names must end with `.lark`.

    Parameters
    ----------
    name : str
        The name of the grammar file to load, without the `.lark` extension.

    Returns
    -------
    Lark
        A Lark parser object.

    Raises
    ------
    FileNotFoundError
        If the grammar file is not found.
    """
    grammar_file = GRAMMARS.joinpath(f"{name}.lark")

    if not grammar_file.is_file():
        raise FileNotFoundError(f"Grammar file {name}.lark not found")

    return Lark.open(str(grammar_file), start="start", parser="earley")


def parse(text: str, parser: Lark, transformer: type[Transformer]) -> dict[str, dict[list[int | float], Any]]:
    """Parse text using a Lark parser and a transformer.

    Parameters
    ----------
    text : str
        The text to parse.
    parser : Lark
        The Lark parser object. Use `load_grammar` to load a grammar file.
    transformer : type[Transformer]
        The transformer class to use.

    Returns
    -------
    dict[str, dict[list[int | float], Any]]
        The text output parsed into a dictionary.
    """
    merged_transformer = merge_transformers(transformer(), zospy=ZospyTransformer())

    return merged_transformer.transform(parser.parse(text))
