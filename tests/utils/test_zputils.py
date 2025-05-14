from contextlib import nullcontext as does_not_raise
from types import SimpleNamespace

import pytest

from zospy.utils.zputils import standardize_sampling, unpack_datagrid

mock_datagrid = SimpleNamespace(
    Values=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    MinX=-1.5,
    MinY=-1.5,
    Nx=3,
    Ny=3,
    Dx=1,
    Dy=1,
    XLabel="x",
    YLabel="y",
)


def test_unpack_datagrid_bottom_left():
    result = unpack_datagrid(mock_datagrid, cell_origin="bottom_left")

    assert all(result.columns == [-1, 0, 1])
    assert all(result.index == [-1, 0, 1])


def test_unpack_datagrid_center():
    result = unpack_datagrid(mock_datagrid, cell_origin="center")

    assert all(result.columns == [-1.5, -0.5, 0.5])
    assert all(result.index == [-1.5, -0.5, 0.5])


class TestStandardizeSampling:
    @pytest.mark.parametrize(
        "value,output,expectation",
        [
            (1, 1, does_not_raise()),
            ("32x32", "S_32x32", does_not_raise()),
            ("S_32x32", "S_32x32", does_not_raise()),
            ("S32x32", None, pytest.raises(ValueError, match="Cannot interpret sampling pattern")),
            ("64x32", None, pytest.raises(ValueError, match="Cannot interpret sampling pattern")),
            ("32x32x32", None, pytest.raises(ValueError, match="Cannot interpret sampling pattern")),
            (2.25, None, pytest.raises(TypeError, match="sampling should be int or string")),
        ],
    )
    def test_standardize_sampling(self, value, output, expectation):
        with expectation:
            result = standardize_sampling(value)

            assert result == output

    @pytest.mark.parametrize(
        "value,prefix,output,expectation",
        [
            (1, "S", 1, does_not_raise()),
            ("32x32", "PsfS", "PsfS_32x32", does_not_raise()),
            ("PsfS_32x32", "PsfS", "PsfS_32x32", does_not_raise()),
            ("S_32x32", "PsfS", None, pytest.raises(ValueError, match="Cannot interpret sampling pattern")),
        ],
    )
    def test_prefix(self, value, prefix, output, expectation):
        with expectation:
            result = standardize_sampling(value, prefix=prefix)

            assert result == output
