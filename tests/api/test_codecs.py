import clr
import pytest
from System.Reflection import Assembly

import zospy as zp
from zospy.api.codecs import OpticStudioInterfaceEncoder

# ruff: noqa: SLF001


class TestOpticStudioInterfaceEncoder:
    """Test automatic downcasting of generic interfaces to specific interfaces using `OpticStudioInterfaceEncoder`.

    Each test tests a specific scenario which fails is codecs are not used.
    """

    @pytest.fixture(scope="module")
    def zosapi_interfaces(self, zos):  # noqa: ARG002
        return Assembly.LoadFile(clr.FindAssembly("ZOSAPI_Interfaces"))

    def test_types_exist(self, zosapi_interfaces):
        """Test if all types in `OpticStudioInterfaceEncoder._interfaces` exist."""
        zosapi_type_names = [t.FullName for t in zosapi_interfaces.GetTypes()]

        assert OpticStudioInterfaceEncoder._interfaces.issubset(zosapi_type_names)

    def test_types_are_interfaces(self, zosapi_interfaces):
        """Test if all types in `OpticStudioInterfaceEncoder._interfaces` are interfaces."""
        assert all(zosapi_interfaces.GetType(t).IsInterface for t in OpticStudioInterfaceEncoder._interfaces)

    def test_register_interfaces_single(self, monkeypatch):
        # Temporarily overwrite OpticStudioInterfaceEncoder._interfaces and restore it after the test
        monkeypatch.setattr(OpticStudioInterfaceEncoder, "_interfaces", frozenset())

        interface = "ZOSAPI.Editors.NCE.IObjectScatteringSettings"

        assert interface not in OpticStudioInterfaceEncoder._interfaces

        OpticStudioInterfaceEncoder.register_interfaces(interface)

        assert interface in OpticStudioInterfaceEncoder._interfaces

    def test_register_interfaces_multiple(self, monkeypatch):
        # Temporarily overwrite OpticStudioInterfaceEncoder._interfaces and restore it after the test
        monkeypatch.setattr(OpticStudioInterfaceEncoder, "_interfaces", frozenset())

        interfaces = ["ZOSAPI.Editors.NCE.IObjectScatteringSettings", "ZOSAPI.Editors.NCE.IVolumePhysicsModelSettings"]

        assert all(i not in OpticStudioInterfaceEncoder._interfaces for i in interfaces)

        OpticStudioInterfaceEncoder.register_interfaces(interfaces)

        assert all(i in OpticStudioInterfaceEncoder._interfaces for i in interfaces)

    def test_analysis_settings_ias(self, oss):
        """Test downcasting for `ZOSAPI.Analysis.Settings.IAS_`."""
        analysis = oss.Analyses.New_Analysis_SettingsFirst(
            zp.constants.Analysis.AnalysisIDM.ZernikeStandardCoefficients
        )

        analysis.GetSettings().MaximumNumberOfTerms = 37

        assert analysis.GetSettings().MaximumNumberOfTerms == 37

    def test_editors_nce_iobject(self, nsc_simple_system):
        """Test downcasting for `ZOSAPI.Editors.NCE.IObject`."""
        object_data = nsc_simple_system.NCE.GetObjectAt(2).ObjectData

        assert object_data.Radius1 == 20

    def test_editors_lde_isurface(self, polarized_system):
        """Test downcasting for `ZOSAPI.Editors.LDE.ISurface`."""
        surface_data = polarized_system.LDE.GetSurfaceAt(2).SurfaceData

        assert surface_data.Ar == 1
        assert surface_data.Dr == 0

    def test_editors_lde_isurfaceaperturetype(self, simple_system):
        """Test downcasting for `ZOSAPI.Editors.LDE.ISurfaceApertureType`."""
        stop_surface = simple_system.LDE.GetSurfaceAt(simple_system.LDE.StopSurface)

        spider_aperture = stop_surface.ApertureData.CreateApertureTypeSettings(
            zp.constants.Editors.LDE.SurfaceApertureTypes.Spider
        )
        spider_aperture.NumberOfArms = 10
        stop_surface.ApertureData.ChangeApertureTypeSettings(spider_aperture)

        assert stop_surface.ApertureData.CurrentTypeSettings.NumberOfArms == 10

    def test_editors_lde_isurfacescatteringtype(self, simple_system):
        """Test downcasting for `ZOSAPI.Editors.LDE.ISurfaceScatteringType`."""
        lens_front = simple_system.LDE.GetSurfaceAt(2)

        gaussian_scattering = lens_front.ScatteringData.CreateScatteringTypeSettings(
            zp.constants.Editors.LDE.SurfaceScatteringTypes.Gaussian
        )
        gaussian_scattering.ScatterFraction = 0.5
        lens_front.ScatteringData.ChangeScatteringTypeSettings(gaussian_scattering)

        assert lens_front.ScatteringData.CurrentTypeSettings.ScatterFraction == 0.5

    def test_tools_isystemtool(self, oss):
        """Test downcasting for `ZOSAPI.Tools.ISystemTool`."""
        local_optimization = oss.Tools.OpenLocalOptimization()
        local_optimization.NumberOfCores = 5

        assert oss.Tools.CurrentTool.NumberOfCores == 5
