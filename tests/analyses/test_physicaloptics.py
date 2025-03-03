import pytest
from numpy.testing import assert_almost_equal

from zospy.analyses.physicaloptics import (
    PhysicalOpticsPropagation,
    create_beam_parameter_dict,
    create_fiber_parameter_dict,
)


class TestPhysicalOpticsPropagation:
    def test_can_run(self, simple_system):
        result = PhysicalOpticsPropagation().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = PhysicalOpticsPropagation().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    def test_can_create_beam_parameter_dict(self, simple_system):
        param_dict = create_beam_parameter_dict(simple_system)

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
        parameter_dict = create_beam_parameter_dict(simple_system, beam_type=beam_type)

        assert set(parameter_dict.keys()) == expected_parameters

    def test_can_create_fiber_parameter_dict(self, simple_system):
        param_dict = create_fiber_parameter_dict(simple_system)

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
        parameter_dict = create_fiber_parameter_dict(simple_system, fiber_type=fiber_type)

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
        result = PhysicalOpticsPropagation(
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
        ).run(simple_system)

        # Check index and columns separately due to rounding errors
        assert_almost_equal(result.data.values, expected_data.data.values, decimal=5)
        assert_almost_equal(result.data.index.values, expected_data.data.index.values, decimal=5)
        assert_almost_equal(result.data.columns.values, expected_data.data.columns.values, decimal=5)

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
        result = PhysicalOpticsPropagation(
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
        ).run(simple_system)

        # Check index and columns separately due to rounding errors
        assert_almost_equal(result.data.values, reference_data.data.values, decimal=5)
        assert_almost_equal(result.data.index.values, reference_data.data.index.values, decimal=5)
        assert_almost_equal(result.data.columns.values, reference_data.data.columns.values, decimal=5)

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
            PhysicalOpticsPropagation(use_total_power=use_total_power, use_peak_irradiance=use_peak_irradiance).run(
                simple_system
            )

    def test_physical_optics_propagation_with_wrong_beam_parameter_raises_exception(self, simple_system):
        with pytest.raises(ValueError, match="The following .+ parameters are specified but not accepted"):
            PhysicalOpticsPropagation(beam_type="GaussianWaist", beam_parameters={"WrongName": 1}).run(simple_system)

    def test_physical_optics_propagation_with_wrong_fiber_parameter_raises_exception(self, simple_system):
        with pytest.raises(ValueError, match="The following .+ parameters are specified but not accepted"):
            PhysicalOpticsPropagation(
                compute_fiber_coupling_integral=True,
                fiber_type="GaussianWaist",
                fiber_parameters={"WrongName": 1},
            ).run(simple_system)
