import pytest

from zospy.analyses.old.reports import (
    cardinal_points,
    cardinal_points_fromcfg,
    surface_data,
    surface_data_fromcfg,
    system_data,
)

pytestmark = pytest.mark.old_analyses


class TestSurfaceData:
    def test_can_run_surface_data(self, simple_system):
        result = surface_data(simple_system, 3)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = surface_data(simple_system, 3)

        assert result.from_json(result.to_json())

    def test_can_run_surface_data_fromcfg(self, simple_system, cfg_file):
        result = surface_data_fromcfg(simple_system, str(cfg_file))

        assert result.Data is not None

    def test_surface_data_fromcfg_loads_config_correctly(self, simple_system, cfg_file):
        result = surface_data_fromcfg(simple_system, str(cfg_file))

        # Check if the correct surface thickness is returned
        assert result.Data.Surface.Thickness == 19.792

    def test_surface_data_returns_correct_result(self, simple_system, expected_data):
        result = surface_data(simple_system, surface=2)

        assert all(result.Data.Surface == expected_data.Data.Surface)
        assert all(result.Data.IndexOfRefraction == expected_data.Data.IndexOfRefraction)
        assert all(result.Data.IndexOfRefractionPerWavelength == expected_data.Data.IndexOfRefractionPerWavelength)
        assert all(result.Data.Other == expected_data.Data.Other)
        assert all(result.Data.SurfacePowerAsSituated == expected_data.Data.SurfacePowerAsSituated)
        assert all(result.Data.SurfacePowerInAir == expected_data.Data.SurfacePowerInAir)

    def test_surface_data_matches_reference_data(self, simple_system, reference_data):
        result = surface_data(simple_system, surface=2)

        assert all(result.Data.Surface == reference_data.Data.Surface)
        assert all(result.Data.IndexOfRefraction == reference_data.Data.IndexOfRefraction)
        assert all(result.Data.IndexOfRefractionPerWavelength == reference_data.Data.IndexOfRefractionPerWavelength)
        assert all(result.Data.Other == reference_data.Data.Other)
        assert all(result.Data.SurfacePowerAsSituated == reference_data.Data.SurfacePowerAsSituated)
        assert all(result.Data.SurfacePowerInAir == reference_data.Data.SurfacePowerInAir)


class TestSystemData:
    def test_can_run_system_data(self, simple_system):
        result = system_data(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = system_data(simple_system)

        assert result.from_json(result.to_json())

    def test_system_data_returns_correct_result(self, simple_system, expected_data):
        result = system_data(simple_system)

        assert all(result.Data.Fields.Data == expected_data.Data.Fields.Data)
        assert all(result.Data.Fields.Info == expected_data.Data.Fields.Info)
        assert all(result.Data.GeneralLensData == expected_data.Data.GeneralLensData)
        assert all(result.Data.PredictedCoordinateABCDMatrix == expected_data.Data.PredictedCoordinateABCDMatrix)
        assert all(result.Data.VignettingFactors == expected_data.Data.VignettingFactors)
        assert all(result.Data.Wavelengths.Data == expected_data.Data.Wavelengths.Data)
        assert all(result.Data.Wavelengths.Info == expected_data.Data.Wavelengths.Info)

    def test_system_data_matches_reference_data(self, simple_system, reference_data):
        result = system_data(simple_system)

        assert all(result.Data.Fields.Data == reference_data.Data.Fields.Data)
        assert all(result.Data.Fields.Info == reference_data.Data.Fields.Info)
        assert all(result.Data.GeneralLensData == reference_data.Data.GeneralLensData)
        assert all(result.Data.PredictedCoordinateABCDMatrix == reference_data.Data.PredictedCoordinateABCDMatrix)
        assert all(result.Data.VignettingFactors == reference_data.Data.VignettingFactors)
        assert all(result.Data.Wavelengths.Data == reference_data.Data.Wavelengths.Data)
        assert all(result.Data.Wavelengths.Info == reference_data.Data.Wavelengths.Info)


class TestCardinalPoints:
    def test_can_run_cardinal_points(self, simple_system):
        result = cardinal_points(simple_system, 2, 3)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = cardinal_points(simple_system, 2, 3)

        assert result.from_json(result.to_json())

    def test_can_run_cardinal_points_fromcfg(self, simple_system, cfg_file):
        result = cardinal_points_fromcfg(simple_system, str(cfg_file))

        assert result.Data is not None

    def test_cardinal_points_fromcfg_loads_config_correctly(self, simple_system, cfg_file):
        result = cardinal_points_fromcfg(simple_system, str(cfg_file))

        assert result.Data.Surface["Starting surface"] == 2
        assert result.Data.Surface["Ending surface"] == 3

    def test_cardinal_points_returns_correct_result(self, simple_system, expected_data):
        result = cardinal_points(simple_system, 2, 3)

        assert result.Data.General.Wavelength == expected_data.Data.General.Wavelength
        assert result.Data.General.Orientation == expected_data.Data.General.Orientation
        assert all(result.Data["Object Space"] == expected_data.Data["Object Space"])
        assert all(result.Data["Image Space"] == expected_data.Data["Image Space"])

    def test_cardinal_points_matches_reference_data(self, simple_system, reference_data):
        result = cardinal_points(simple_system, 2, 3)

        assert result.Data.General.Wavelength == reference_data.Data.General.Wavelength
        assert result.Data.General.Orientation == reference_data.Data.General.Orientation
        assert all(result.Data["Object Space"] == reference_data.Data["Object Space"])
        assert all(result.Data["Image Space"] == reference_data.Data["Image Space"])
