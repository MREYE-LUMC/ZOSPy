from pathlib import Path

import pytest

import zospy as zp


def pytest_addoption(parser):
    parser.addoption("--extension", action="store_true", help="Connect to Zemax OpticStudio as extension")

    parser.addoption("--legacy-connection-setup", action="store_true", help="Use legacy method to setup connection")

    parser.addoption("--output-directory", type=Path)


def pytest_runtest_makereport(item, call):
    if any(m.name == "must_pass" for m in item.iter_markers()):
        if call.excinfo is not None:
            pytest.exit(f"Aborting because a must pass test failed: {item.name}", 1)


@pytest.fixture(scope="session")
def connection_mode(request):
    return "extension" if request.config.getoption("--extension") else "standalone"


@pytest.fixture(autouse=True)
def skip_by_connection_mode(request, connection_mode):
    if request.node.get_closest_marker("require_mode"):
        required_mode = request.node.get_closest_marker("require_mode").args[0]
        if required_mode != connection_mode:
            pytest.skip(f"Test is only applicable in {required_mode} mode.")


@pytest.fixture(scope="session")
def legacy_connection_setup(request):
    return request.config.getoption("--legacy-connection-setup")


@pytest.fixture(scope="session")
def system_save_file(request):
    output_directory = request.config.getoption("--output-directory")

    if output_directory:
        save_file = output_directory / f"{request.fspath.basename}-{request.node.name}.zos"
        return save_file.absolute()
    else:
        return None


@pytest.fixture(scope="session")
def zos(legacy_connection_setup) -> zp.ZOS:
    if not legacy_connection_setup:
        zos = zp.ZOS(zosapi_nethelper="C:\Program Files\Ansys Zemax OpticStudio 2023 R1.03")
    else:
        zos = zp.ZOS()
        zos.wakeup()

    return zos


def _oss(zos: zp.ZOS, connection_mode) -> zp.zpcore.OpticStudioSystem:
    if connection_mode == "extension":
        oss = zos.connect_as_extension(return_primary_system=True)
    else:
        oss = zos.create_new_application(return_primary_system=True)

    yield oss

    # Close the system
    if zos.Connection.IsAlive:
        zos.Application.CloseApplication()


def _oss_legacy(zos: zp.ZOS, connection_mode) -> zp.zpcore.OpticStudioSystem:
    if connection_mode == "extension":
        connected = zos.connect_as_extension()
    else:
        connected = zos.create_new_application()

    oss = zos.get_primary_system()

    yield oss

    # Close the system
    if connected:
        zos.Application.CloseApplication()


@pytest.fixture
def oss(zos: zp.ZOS, connection_mode, legacy_connection_setup) -> zp.zpcore.OpticStudioSystem:
    if not legacy_connection_setup:
        yield from _oss(zos=zos, connection_mode=connection_mode)
    else:
        yield from _oss_legacy(zos=zos, connection_mode=connection_mode)


@pytest.fixture(scope="session")
def optic_studio_version(zos, connection_mode) -> str:
    if connection_mode == "extension":
        zos.connect_as_extension()
    else:
        zos.create_new_application()

    application = zos.Application

    version = f"{application.ZOSMajorVersion}.{application.ZOSMinorVersion}.{application.ZOSSPVersion}"

    zos.Application.CloseApplication()

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
    """Simple system with a polarizing front lens surface"""
    oss = simple_system

    lens_front = oss.LDE.GetSurfaceAt(2)

    # Change surface to Jones Matrix
    zp.functions.lde.surface_change_type(lens_front, zp.constants.Editors.LDE.SurfaceType.JonesMatrix)

    # Set Jones Matrix elements to horizontal polarization
    lens_front.GetCellAt(12).DoubleValue = 1  # A real
    lens_front.GetCellAt(18).DoubleValue = 0  # D real

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
