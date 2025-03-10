from types import SimpleNamespace

from zospy.utils.zputils import unpack_datagrid

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
