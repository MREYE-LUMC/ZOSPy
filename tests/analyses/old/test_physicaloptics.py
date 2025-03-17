import numpy as np
import pytest

from zospy.analyses.old.physicaloptics import (
    physical_optics_propagation,
    pop_create_beam_parameter_dict,
    pop_create_fiber_parameter_dict,
)

pytestmark = pytest.mark.old_analyses


class TestPhysicalOpticsPropagation:
    def test_can_run_physical_optics_propagation(self, simple_system):
        result = physical_optics_propagation(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = physical_optics_propagation(simple_system)

        assert result.from_json(result.to_json())

    def test_can_create_beam_parameter_dict(self, simple_system):
        param_dict = pop_create_beam_parameter_dict(simple_system)

        assert isinstance(param_dict, dict)

    @pytest.mark.parametrize(
        "beam_type,expected_parameters",
        [
            (
                "GaussianWaist",
                {"Waist X", "Waist Y", "Decenter X", "Decenter Y", "Aperture X", "Aperture Y", "Order X", "Order Y"},
            ),
            ("GaussianSizeAngle", {"Size X", "Size Y", "Angle X (deg)", "Angle Y (deg)", "Decenter X:", "Decenter Y:"}),
            ("TopHat", {"Waist X", "Waist Y", "Decenter X", "Decenter Y"}),
            (
                "AstigmaticGaussian",
                {"Waist X", "Waist Y", "Waist Position X", "Waist Position Y", "Decenter X:", "Decenter Y:"},
            ),
            # TODO: create bug report regarding colons in decenter x and y
        ],
    )
    def test_create_beam_parameter_dict_returns_correct_parameters(self, simple_system, beam_type, expected_parameters):
        parameter_dict = pop_create_beam_parameter_dict(simple_system, beam_type=beam_type)

        assert set(parameter_dict.keys()) == expected_parameters

    def test_can_create_fiber_parameter_dict(self, simple_system):
        param_dict = pop_create_fiber_parameter_dict(simple_system)

        assert isinstance(param_dict, dict)

    @pytest.mark.parametrize(
        "fiber_type,expected_parameters",
        [
            (
                "GaussianWaist",
                {"Waist X", "Waist Y", "Decenter X", "Decenter Y", "Aperture X", "Aperture Y", "Order X", "Order Y"},
            ),
            ("GaussianSizeAngle", {"Size X", "Size Y", "Angle X (deg)", "Angle Y (deg)", "Decenter X:", "Decenter Y:"}),
            ("TopHat", {"Waist X", "Waist Y", "Decenter X", "Decenter Y"}),
            (
                "AstigmaticGaussian",
                {"Waist X", "Waist Y", "Waist Position X", "Waist Position Y", "Decenter X:", "Decenter Y:"},
            ),
            # TODO: create bug report regarding colons in decenter x and y
        ],
    )
    def test_create_fiber_parameter_dict_returns_correct_parameters(
        self, simple_system, fiber_type, expected_parameters
    ):
        parameter_dict = pop_create_fiber_parameter_dict(simple_system, fiber_type=fiber_type)

        assert set(parameter_dict.keys()) == expected_parameters

    @pytest.mark.parametrize(
        "compute_fiber_coupling_integral,fiber_type,fiber_parameters",
        [
            (False, "TopHat", None),
            (True, "TopHat", None),
            (
                True,
                "GaussianWaist",
                {
                    "Waist X": 0.03,
                    "Waist Y": 0.03,
                    "Decenter X": 0.0,
                    "Decenter Y": 0.0,
                    "Aperture X": 0.0,
                    "Aperture Y": 0.0,
                    "Order X": 0.0,
                    "Order Y": 0.0,
                },
            ),
        ],
    )
    @pytest.mark.parametrize(
        "beam_type,beam_parameters,auto_calculate_beam_sampling",
        [
            ("GaussianWaist", None, False),
            (
                "GaussianWaist",
                {
                    "Waist X": 1.5,
                    "Waist Y": 1.5,
                    "Decenter X": 0.1,
                    "Decenter Y": 0.1,
                    "Aperture X": 0.0,
                    "Aperture Y": 0.0,
                    "Order X": 0.0,
                    "Order Y": 0.0,
                },
                False,
            ),
            ("TopHat", {"Waist X": 0.5, "Waist Y": 0.5, "Decenter X": 0.0, "Decenter Y": 0.0}, False),
            ("TopHat", {"Waist X": 0.5, "Waist Y": 0.5, "Decenter X": 0.0, "Decenter Y": 0.0}, True),
        ],
    )
    @pytest.mark.parametrize(
        "surface_to_beam,data_type,use_total_power,use_peak_irradiance",
        [
            (0.0, "Irradiance", True, False),
            (1.0, "Irradiance", True, False),
            (0.0, "Irradiance", False, True),
            (0.0, "Phase", True, False),
        ],
    )
    def test_physical_optics_propagation_returns_correct_result(
        self,
        simple_system,
        surface_to_beam,
        beam_type,
        beam_parameters,
        use_total_power,
        use_peak_irradiance,
        data_type,
        compute_fiber_coupling_integral,
        fiber_type,
        fiber_parameters,
        auto_calculate_beam_sampling,
        expected_data,
    ):
        result = physical_optics_propagation(
            simple_system,
            surface_to_beam=surface_to_beam,
            beam_type=beam_type,
            beam_parameters=beam_parameters,
            use_total_power=use_total_power,
            use_peak_irradiance=use_peak_irradiance,
            data_type=data_type,
            compute_fiber_coupling_integral=compute_fiber_coupling_integral,
            fiber_type=fiber_type,
            fiber_parameters=fiber_parameters,
            auto_calculate_beam_sampling=auto_calculate_beam_sampling,
        )

        assert np.allclose(result.Data.astype(float), expected_data.Data.astype(float), rtol=1e-3)

    @pytest.mark.parametrize(
        "compute_fiber_coupling_integral,fiber_type,fiber_parameters",
        [
            (False, "TopHat", None),
            (True, "TopHat", None),
            (
                True,
                "GaussianWaist",
                {
                    "Waist X": 0.03,
                    "Waist Y": 0.03,
                    "Decenter X": 0.0,
                    "Decenter Y": 0.0,
                    "Aperture X": 0.0,
                    "Aperture Y": 0.0,
                    "Order X": 0.0,
                    "Order Y": 0.0,
                },
            ),
        ],
    )
    @pytest.mark.parametrize(
        "beam_type,beam_parameters,auto_calculate_beam_sampling",
        [
            ("GaussianWaist", None, False),
            (
                "GaussianWaist",
                {
                    "Waist X": 1.5,
                    "Waist Y": 1.5,
                    "Decenter X": 0.1,
                    "Decenter Y": 0.1,
                    "Aperture X": 0.0,
                    "Aperture Y": 0.0,
                    "Order X": 0.0,
                    "Order Y": 0.0,
                },
                False,
            ),
            ("TopHat", {"Waist X": 0.5, "Waist Y": 0.5, "Decenter X": 0.0, "Decenter Y": 0.0}, False),
            ("TopHat", {"Waist X": 0.5, "Waist Y": 0.5, "Decenter X": 0.0, "Decenter Y": 0.0}, True),
        ],
    )
    @pytest.mark.parametrize(
        "surface_to_beam,data_type,use_total_power,use_peak_irradiance",
        [
            (0.0, "Irradiance", True, False),
            (1.0, "Irradiance", True, False),
            (0.0, "Irradiance", False, True),
            (0.0, "Phase", True, False),
        ],
    )
    def test_physical_optics_propagation_matches_reference_data(
        self,
        simple_system,
        surface_to_beam,
        beam_type,
        beam_parameters,
        use_total_power,
        use_peak_irradiance,
        data_type,
        compute_fiber_coupling_integral,
        fiber_type,
        fiber_parameters,
        auto_calculate_beam_sampling,
        reference_data,
    ):
        result = physical_optics_propagation(
            simple_system,
            surface_to_beam=surface_to_beam,
            beam_type=beam_type,
            beam_parameters=beam_parameters,
            use_total_power=use_total_power,
            use_peak_irradiance=use_peak_irradiance,
            data_type=data_type,
            compute_fiber_coupling_integral=compute_fiber_coupling_integral,
            fiber_type=fiber_type,
            fiber_parameters=fiber_parameters,
            auto_calculate_beam_sampling=auto_calculate_beam_sampling,
        )

        assert np.allclose(result.Data.astype(float), reference_data.Data.astype(float), rtol=1e-3)

    @pytest.mark.parametrize(
        "use_total_power,use_peak_irradiance",
        [
            (True, True),
            (False, False),
        ],
    )
    def test_physical_optics_propagation_with_matching_use_total_power_and_peak_irradiance_raises_exception(
        self, simple_system, use_total_power, use_peak_irradiance
    ):
        with pytest.raises(
            ValueError,
            match="Either use_total_power or use_peak_irradiance should be True, they cannot both be True or False",
        ):
            physical_optics_propagation(
                simple_system, use_total_power=use_total_power, use_peak_irradiance=use_peak_irradiance
            )

    def test_physical_optics_propagation_with_wrong_beam_parameter_raises_exception(self, simple_system):
        with pytest.raises(ValueError, match="The following .+ parameters are specified but not accepted"):
            physical_optics_propagation(simple_system, beam_type="GaussianWaist", beam_parameters={"WrongName": 1})

    def test_physical_optics_propagation_with_wrong_fiber_parameter_raises_exception(self, simple_system):
        with pytest.raises(ValueError, match="The following .+ parameters are specified but not accepted"):
            physical_optics_propagation(
                simple_system,
                compute_fiber_coupling_integral=True,
                fiber_type="GaussianWaist",
                fiber_parameters={"WrongName": 1},
            )
