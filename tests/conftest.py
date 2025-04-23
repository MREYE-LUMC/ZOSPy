from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest
from semver.version import Version

import zospy as zp


def pytest_addoption(parser):
    parser.addoption("--extension", action="store_true", help="Connect to Zemax OpticStudio as extension")
    parser.addoption("--output-directory", type=Path)
    parser.addoption("--update-ui", type=bool, default=False)
    parser.addoption(
        "--opticstudio-directory", type=Path, default=None, help="Path to the OpticStudio installation directory"
    )
    parser.addoption("--old-analyses", action="store_true", help="Run tests for old analyses")


def pytest_runtest_makereport(item, call):
    if any(m.name == "must_pass" for m in item.iter_markers()) and call.excinfo is not None:
        pytest.exit(f"Aborting because a must pass test failed: {item.name}", 1)


def _get_old_analyses(items):
    return [item for item in items if item.get_closest_marker("old_analyses")]


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(config, items):
    """Customize test selection.

    Customizing test selection allows to hide results from the test output instead of marking them as skipped.
    Current customizations:
    - Skip tests for old analyses if the `--old-analyses` option is not set.
    - Run must_pass tests first.
    """
    yield

    # Deselect tests for old analyses if --old-analyses is not set
    if not config.getoption("--old-analyses"):
        deselected = _get_old_analyses(items)
        items[:] = [item for item in items if item not in deselected]
        config.hook.pytest_deselected(items=deselected)

    # Run must_pass tests first
    must_pass_tests = [item for item in items if item.get_closest_marker("must_pass")]
    for test in must_pass_tests:
        items.remove(test)
        items.insert(0, test)


@pytest.fixture(scope="session")
def connection_mode(request) -> Literal["extension", "standalone"]:
    return "extension" if request.config.getoption("--extension") else "standalone"


@pytest.fixture(autouse=True)
def skip_by_connection_mode(request, connection_mode):
    if request.node.get_closest_marker("require_mode"):
        required_mode = request.node.get_closest_marker("require_mode").args[0]
        if required_mode != connection_mode:
            pytest.skip(f"Test is only applicable in {required_mode} mode.")


@pytest.fixture(autouse=True)
def skip_for_opticstudio_versions(request, optic_studio_version):
    if request.node.get_closest_marker("skip_for_opticstudio_versions"):
        conditions, reason = request.node.get_closest_marker("skip_for_opticstudio_versions").args[:2]

        if isinstance(conditions, str):
            conditions = [conditions]

        for condition in conditions:
            if optic_studio_version.match(condition):
                pytest.skip(reason=reason)


@pytest.fixture(autouse=True)
def xfail_for_opticstudio_versions(request, optic_studio_version):
    if request.node.get_closest_marker("xfail_for_opticstudio_versions"):
        conditions, reason = request.node.get_closest_marker("xfail_for_opticstudio_versions").args[:2]

        if isinstance(conditions, str):
            conditions = [conditions]

        for condition in conditions:
            if optic_studio_version.match(condition):
                request.node.add_marker(pytest.mark.xfail(True, reason=reason, raises=AssertionError))


@pytest.fixture(autouse=True)
def skip_old_analysis_tests(request):
    if request.node.get_closest_marker("old_analyses") and not request.config.getoption("--old-analyses"):
        pytest.skip("Skipping tests for old analyses")


@pytest.fixture(scope="session")
def system_save_file(request):
    output_directory = request.config.getoption("--output-directory")

    if output_directory:
        save_file = output_directory / f"{request.fspath.basename}-{request.node.name}.zos"
        return save_file.absolute()
    return None


@pytest.fixture(scope="session")
def opticstudio_directory(request) -> Path | None:
    path = request.config.getoption("--opticstudio-directory")

    if path is not None:
        return Path(path).resolve(strict=True)

    return None


@pytest.fixture(scope="session")
def zos(opticstudio_directory) -> zp.ZOS:
    return zp.ZOS(opticstudio_directory=str(opticstudio_directory)) if opticstudio_directory is not None else zp.ZOS()


@pytest.fixture
def oss(zos: zp.ZOS, connection_mode, request) -> zp.zpcore.OpticStudioSystem:
    oss = zos.connect(connection_mode)

    if connection_mode == "extension":
        # Disable UI updates using command line option, making the tests run faster
        zos.Application.ShowChangesInUI = request.config.getoption("--update-ui")

    yield oss

    # Close the system
    if zos.Connection.IsAlive:
        zos.Application.CloseApplication()
        zos.Application = None


@pytest.fixture(scope="session")
def optic_studio_version(zos, connection_mode) -> Version:
    zos.connect(connection_mode)

    version = Version(
        major=zos.Application.ZOSMajorVersion, minor=zos.Application.ZOSMinorVersion, patch=zos.Application.ZOSSPVersion
    )

    zos.Application.CloseApplication()
    zos.Application = None

    return version


@pytest.fixture
def empty_system(oss, system_save_file) -> zp.zpcore.OpticStudioSystem:
    oss.new()
    oss.make_sequential()

    yield oss

    if system_save_file:
        oss.save_as(str(system_save_file))


@pytest.fixture
def simple_system(empty_system) -> zp.zpcore.OpticStudioSystem:
    oss = empty_system

    oss.SystemData.Aperture.ApertureType = zp.constants.SystemData.ZemaxApertureType.FloatByStopSize
    oss.SystemData.Wavelengths.GetWavelength(1).Wavelength = 0.543

    surface_object = oss.LDE.GetSurfaceAt(0)
    surface_object.Thickness = float("inf")

    surface_stop = oss.LDE.GetSurfaceAt(1)
    surface_stop.SemiDiameter = 1

    lens_front = oss.LDE.InsertNewSurfaceAt(2)
    lens_front.Comment = "lens front"
    lens_front.Radius = 20
    lens_front.Thickness = 1
    zp.solvers.material_model(lens_front.MaterialCell, refractive_index=1.5)

    lens_back = oss.LDE.InsertNewSurfaceAt(3)
    lens_back.Comment = "lens back"
    lens_back.Radius = -20
    lens_back.Thickness = 19.792  # System is in focus

    return oss


@pytest.fixture
def polarized_system(simple_system) -> zp.zpcore.OpticStudioSystem:
    """Simple system with a polarizing front lens surface."""
    oss = simple_system

    lens_front = oss.LDE.GetSurfaceAt(2)

    # Change surface to Jones Matrix
    zp.functions.lde.surface_change_type(lens_front, zp.constants.Editors.LDE.SurfaceType.JonesMatrix)

    # Set Jones Matrix elements to horizontal polarization
    lens_front.GetCellAt(12).DoubleValue = 1  # A real
    lens_front.GetCellAt(18).DoubleValue = 0  # D real

    return oss


@pytest.fixture
def coordinate_break_system(simple_system: zp.zpcore.OpticStudioSystem) -> zp.zpcore.OpticStudioSystem:
    """Simple system with a coordinate break behind the lens."""
    oss = simple_system

    coordinate_break = oss.LDE.InsertNewSurfaceAt(4)
    zp.functions.lde.surface_change_type(coordinate_break, zp.constants.Editors.LDE.SurfaceType.CoordinateBreak)
    coordinate_break.SurfaceData.Decenter_X = 2

    return oss


@pytest.fixture
def decentered_system(simple_system) -> zp.zpcore.OpticStudioSystem:
    """Simple system with incoming rays at a non-zero angle."""
    oss = simple_system

    field = oss.SystemData.Fields.GetField(1)
    field.X = 10
    field.Y = 20

    return oss


@pytest.fixture
def object_height_system(simple_system) -> zp.zpcore.OpticStudioSystem:
    """Decentered system with object height field type."""
    oss = simple_system

    # Use a finite object distance
    oss.LDE.GetSurfaceAt(0).Thickness = 10

    oss.SystemData.Fields.SetFieldType(zp.constants.SystemData.FieldType.ObjectHeight)
    oss.SystemData.Fields.GetField(1).X = 1.0
    oss.SystemData.Fields.GetField(1).Y = 2.0

    return oss


@pytest.fixture
def nsc_empty_system(oss, system_save_file) -> zp.zpcore.OpticStudioSystem:
    oss.new()
    oss.make_nonsequential()

    yield oss

    if system_save_file:
        oss.save_as(str(system_save_file))


@pytest.fixture
def nsc_simple_system(nsc_empty_system) -> zp.zpcore.OpticStudioSystem:
    oss = nsc_empty_system

    oss.SystemData.Wavelengths.GetWavelength(1).Wavelength = 0.543

    source_object = oss.NCE.GetObjectAt(1)
    zp.functions.nce.object_change_type(source_object, zp.constants.Editors.NCE.ObjectType.SourceEllipse)
    source_object.GetCellAt(11).IntegerValue = 100  # Layout Rays
    source_object.GetCellAt(12).IntegerValue = 100  # Analysis Rays
    source_object.GetCellAt(16).DoubleValue = 1  # X Half Width
    source_object.GetCellAt(17).DoubleValue = 1  # Y Half Width

    lens_object = oss.NCE.InsertNewObjectAt(2)
    zp.functions.nce.object_change_type(lens_object, zp.constants.Editors.NCE.ObjectType.StandardLens)
    lens_object.ZPosition = 10
    lens_object.GetCellAt(11).DoubleValue = 20  # Radius front
    lens_object.GetCellAt(13).DoubleValue = 2  # Semi diameter front
    lens_object.GetCellAt(15).DoubleValue = 1  # Thickness
    lens_object.GetCellAt(16).DoubleValue = -20
    lens_object.GetCellAt(18).DoubleValue = 2  # Semi diameter back

    zp.solvers.material_model(lens_object.MaterialCell, refractive_index=1.5)

    detector_object = oss.NCE.InsertNewObjectAt(3)
    zp.functions.nce.object_change_type(detector_object, zp.constants.Editors.NCE.ObjectType.DetectorSurface)
    detector_object.ZPosition = 10 + 1 + 19.792
    return oss
