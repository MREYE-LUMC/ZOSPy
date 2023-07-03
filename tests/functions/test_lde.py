import pytest

from zospy.functions.lde import find_surface_by_comment


@pytest.mark.parametrize(
    "comment,case_sensitive,expected_indices",
    [
        ("Abcd", True, [0]),  # When using .SurfaceNumber, the returned value matches the LDE numbering (starting at 0)
        ("Abcd", False, [0, 1, 2, 3]),
        ("ABcd", True, [1]),
        ("ABCD", True, []),
        ("ABCD", False, [0, 1, 2, 3]),
        ("efgh", True, []),
        ("efgh", False, []),
    ],
)
def test_can_find_surface_by_comment(simple_system, comment, case_sensitive, expected_indices):
    simple_system.LDE.GetSurfaceAt(0).Comment = "Abcd"
    simple_system.LDE.GetSurfaceAt(1).Comment = "ABcd"
    simple_system.LDE.GetSurfaceAt(2).Comment = "ABCd"
    simple_system.LDE.GetSurfaceAt(3).Comment = "ABCd"

    result = find_surface_by_comment(simple_system.LDE, comment=comment, case_sensitive=case_sensitive)

    indices = [surface.SurfaceNumber for surface in result]

    assert indices == expected_indices
