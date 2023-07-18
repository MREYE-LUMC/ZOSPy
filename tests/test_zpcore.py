import pytest


@pytest.mark.must_pass
@pytest.mark.parametrize(
        "oss_fixture",
        ['oss_legacy', 'oss'],
    )
def test_can_connect(oss_fixture, request):
    oss = request.getfixturevalue(oss_fixture)
    assert oss._System is not None


@pytest.mark.must_pass
def test_create_simple_system(simple_system):
    assert simple_system.LDE.NumberOfSurfaces == 5


def test_version(optic_studio_version):
    assert optic_studio_version


def test_new(simple_system):
    # Replace with a new system
    simple_system.new()

    assert simple_system.LDE.NumberOfSurfaces == 3


def test_save_as(simple_system, tmp_path):
    save_path = tmp_path / "TEST.ZOS"

    simple_system.save_as(str(save_path.absolute()))

    assert save_path.exists()


def test_get_system(zos, oss, connection_mode):
    system = zos.get_system(0)

    assert system._System is not None
    assert system.SystemID == oss.SystemID


def test_create_new_system(zos, oss, connection_mode):
    if connection_mode == "extension":
        pytest.skip("Test is only applicable in standalone mode")

    new_system = zos.create_new_system()

    assert zos.Application.NumberOfOpticalSystems == 2
    assert oss.SystemID != new_system.SystemID


def test_create_new_system_raises_valueerror(zos, simple_system, connection_mode):
    if connection_mode == "standalone":
        pytest.skip("Test is only applicable in extension mode")

    with pytest.raises(ValueError):
        zos.create_new_system()
