# ruff: noqa: RUF069
from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from types import SimpleNamespace

import numpy as np
import pytest

from zospy.utils.zputils import standardize_sampling, unpack_datagrid


class TestUnpackDatagrid:
    @pytest.fixture
    def mock_datagrid(self):
        return SimpleNamespace(
            Values=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            MinX=-1.5,
            MinY=-1.5,
            Nx=3,
            Ny=3,
            Dx=1,
            Dy=1,
            XLabel="xlabel",
            YLabel="ylabel",
        )

    def test_unpack_datagrid_bottom_left(self, mock_datagrid):
        result = unpack_datagrid(mock_datagrid, cell_origin="bottom_left")

        assert np.all(result.values == mock_datagrid.Values)
        assert np.all(result.columns == [-1, 0, 1])
        assert np.all(result.index == [-1, 0, 1])
        assert result.columns.name == mock_datagrid.XLabel
        assert result.index.name == mock_datagrid.YLabel

    def test_unpack_datagrid_center(self, mock_datagrid):
        result = unpack_datagrid(mock_datagrid, cell_origin="center")

        assert np.all(result.values == mock_datagrid.Values)
        assert np.all(result.columns == [-1.5, -0.5, 0.5])
        assert np.all(result.index == [-1.5, -0.5, 0.5])
        assert result.columns.name == mock_datagrid.XLabel
        assert result.index.name == mock_datagrid.YLabel

    def test_unpack_datagrid_invalid_cell_origin(self, mock_datagrid):
        with pytest.raises(ValueError, match="Cannot process the cell origin 'invalid'"):
            unpack_datagrid(mock_datagrid, cell_origin="invalid")

    def test_unpack_datagrid_custom_spacing_and_origin_bottom_left(self, mock_datagrid):
        minx = miny = -2
        dx = dy = 0.5

        result = unpack_datagrid(mock_datagrid, cell_origin="bottom_left", minx=minx, miny=miny, dx=dx, dy=dy)

        assert np.all(result.columns == [-1.75, -1.25, -0.75])
        assert np.all(result.index == [-1.75, -1.25, -0.75])
        assert result.columns[0] == minx + 0.5 * dx
        assert result.index[0] == miny + 0.5 * dy
        assert result.columns[1] - result.columns[0] == dx
        assert result.index[1] - result.index[0] == dy

    def test_unpack_datagrid_custom_spacing_and_origin_center(self, mock_datagrid):
        minx = miny = -2
        dx = dy = 0.5

        result = unpack_datagrid(mock_datagrid, cell_origin="center", minx=minx, miny=miny, dx=dx, dy=dy)

        assert np.all(result.columns == [-2, -1.5, -1])
        assert np.all(result.index == [-2, -1.5, -1])
        assert result.columns[0] == minx
        assert result.index[0] == miny
        assert result.columns[1] - result.columns[0] == dx
        assert result.index[1] - result.index[0] == dy


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
