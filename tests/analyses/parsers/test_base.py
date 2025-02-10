from pathlib import Path

import pytest

from zospy.analyses.parsers import base

available_grammars = [
    g.stem for g in Path(base.__file__).parent.joinpath("grammars").glob("*.lark") if g.stem != "zospy"
]


@pytest.mark.parametrize("grammar", available_grammars)
def test_load_grammar(grammar: str):
    grammar = base.load_grammar(grammar)
    assert grammar is not None


def test_load_nonexistent_grammar():
    with pytest.raises(FileNotFoundError, match="Grammar file nonexistent.lark not found"):
        base.load_grammar("nonexistent")
