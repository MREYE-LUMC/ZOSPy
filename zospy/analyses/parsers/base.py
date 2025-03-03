"""Base classes and functions for OpticStudio analysis output parsers."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from lark import Lark, Transformer
from lark.visitors import merge_transformers

from zospy.analyses.parsers.transformers import ZospyTransformer


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
    try:
        return Lark.open_from_package("zospy.analyses.parsers.grammars", f"{name}.lark", parser="earley", start="start")
    except (FileNotFoundError, OSError) as e:
        raise FileNotFoundError(f"Grammar file {name}.lark not found") from e


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
