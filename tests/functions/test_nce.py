import pytest

from zospy.functions.nce import find_object_by_comment


@pytest.mark.parametrize(
    "comment,case_sensitive,expected_indices",
    [
        ("Abc", True, [1]),  # When using .ObjectNumber, the returned value matches the NCE numbering (starting at 1)
        ("Abc", False, [1, 2, 3]),
        ("ABc", True, [2, 3]),
        ("ABC", True, []),
        ("ABC", False, [1, 2, 3]),
        ("efg", True, []),
        ("efg", False, []),
    ],
)
def test_can_find_object_by_comment(nsc_simple_system, comment, case_sensitive, expected_indices):
    nsc_simple_system.NCE.GetObjectAt(1).Comment = "Abc"
    nsc_simple_system.NCE.GetObjectAt(2).Comment = "ABc"
    nsc_simple_system.NCE.GetObjectAt(3).Comment = "ABc"

    result = find_object_by_comment(nsc_simple_system.NCE, comment=comment, case_sensitive=case_sensitive)

    indices = [obj.ObjectNumber for obj in result]

    assert indices == expected_indices
