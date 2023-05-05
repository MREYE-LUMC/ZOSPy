from pathlib import Path

import pytest

import zospy as zp


def pytest_addoption(parser):
    parser.addoption("--extension", action="store_true", help="Connect to Zemax OpticStudio as extension")

    parser.addoption("--output-directory", type=Path)


def pytest_runtest_makereport(item, call):
    if any(m.name == "must_pass" for m in item.iter_markers()):
        if call.excinfo is not None:
            pytest.exit(f"Aborting because a must pass test failed: {item.name}", 1)


@pytest.fixture(scope="session")
def connection_mode(request):
    return "extension" if request.config.getoption("--extension") else "standalone"


@pytest.fixture(scope="session")
def system_save_file(request):
    output_directory = request.config.getoption("--output-directory")

    if output_directory:
        save_file = output_directory / f"{request.fspath.basename}-{request.node.name}.zos"
        return save_file.absolute()
    else:
        return None


@pytest.fixture(scope="session")
def zos() -> zp.ZOS:
    zos = zp.ZOS()
    zos.wakeup()

    return zos


@pytest.fixture
def oss(zos: zp.ZOS, connection_mode) -> zp.zpcore.OpticStudioSystem:
    if connection_mode == "extension":
        connected = zos.connect_as_extension()
    else:
        connected = zos.create_new_application()

    oss = zos.get_primary_system()

    yield oss

    # Close the system
    if connected:
        zos.Application.CloseApplication()


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
