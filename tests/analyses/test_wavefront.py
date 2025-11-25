from __future__ import annotations

from contextlib import nullcontext as does_not_raise

import pytest
from pandas.testing import assert_frame_equal
from pydantic_core import ValidationError

from tests.helpers import assert_dataclass_equal
from zospy.analyses.wavefront import WavefrontMap, ZernikeStandardCoefficients
from zospy.analyses.wavefront.zernike_coefficients_vs_field import (
    ZernikeCoefficientsVsField,
    ZernikeCoefficientsVsFieldSettings,
)


class TestWavefrontMap:
    def test_can_run(self, simple_system):
        result = WavefrontMap().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = WavefrontMap().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "sampling,use_exit_pupil", [("64x64", True), ("64x64", False), ("128x128", True), ("128x128", False)]
    )
    def test_wavefront_map_returns_correct_result(self, simple_system, sampling, use_exit_pupil, expected_data):
        result = WavefrontMap(sampling=sampling, use_exit_pupil=use_exit_pupil).run(simple_system)

        assert_frame_equal(result.data, expected_data.data)


class TestZernikeStandardCoefficients:
    def test_can_run(self, simple_system):
        result = ZernikeStandardCoefficients().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = ZernikeStandardCoefficients().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_returns_correct_result(
        self, simple_system, sampling, maximum_term, expected_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(simple_system)

        assert_dataclass_equal(
            result.data,
            expected_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_decentered_returns_correct_result(
        self, decentered_system, sampling, maximum_term, expected_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(decentered_system)

        assert_dataclass_equal(
            result.data,
            expected_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_object_height_returns_correct_result(
        self, object_height_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(object_height_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_matches_reference_data(
        self, simple_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(simple_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_decentered_matches_reference_data(
        self, decentered_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(decentered_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )

    @pytest.mark.parametrize("sampling,maximum_term", [("64x64", 37), ("128x128", 64)])
    def test_zernike_standard_coefficients_object_height_matches_reference_data(
        self, object_height_system, sampling, maximum_term, reference_data
    ):
        result = ZernikeStandardCoefficients(sampling=sampling, maximum_term=maximum_term).run(object_height_system)

        assert_dataclass_equal(
            result.data,
            reference_data.data,
        )


class TestZernikeCoefficientsVsField:
    @pytest.mark.parametrize(
        "coefficients,expectation",
        [
            ("1-15", does_not_raise()),
            ("1,3,5,7,9", does_not_raise()),
            ("1-5,10-15", does_not_raise()),
            ("1,2-8,10,12-16", does_not_raise()),
            ("a-b", pytest.raises(ValidationError)),
            ("1-kaas", pytest.raises(ValidationError)),
            ("", pytest.raises(ValidationError)),
        ],
    )
    def test_settings_validates_coefficients(self, coefficients, expectation):
        with expectation:
            settings = ZernikeCoefficientsVsFieldSettings(coefficients=coefficients)

            assert settings.coefficients == coefficients

    def test_can_run(self, simple_system):
        result = ZernikeCoefficientsVsField().run(simple_system)
        assert result is not None

    def test_to_json(self, simple_system):
        result = ZernikeCoefficientsVsField().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "coefficients,coefficients_type,field_scan,field_density,sampling,obscuration,minimum_plot_scale,maximum_plot_scale",
        [
            ("1-8", "Standard", "+y", 20, "64x64", 0.5, 0, 0),
            ("2", "Standard", "-y", 10, "32x32", 0.5, 0, 0),
            ("1,3,5", "Standard", "+x", 5, "32x32", 0.5, 0, 1),
            ("1-15", "Fringe", "-x", 15, "128x128", 0.5, 1, 5),
            ("1-2,3,5-7", "Annular", "Plus_Y", 1, "32x32", 0.5, 0, 0),
            ("1-2,3,5-7", "Annular", "Minus_Y", 1, "32x32", 0.1, 0, 0),
            ("1-2,3,5-7", "Standard", "Plus_X", 1, "32x32", 0.5, 1, 5),
            ("1-2,3,5-7", "Standard", "Minus_X", 1, "32x32", 0.5, 0, 0),
        ],
    )
    def test_zernike_coefficients_vs_field_returns_correct_result(
        self,
        coefficients,
        coefficients_type,
        field_scan,
        field_density,
        sampling,
        obscuration,
        minimum_plot_scale,
        maximum_plot_scale,
        simple_system,
        expected_data,
    ):
        result = ZernikeCoefficientsVsField(
            coefficients=coefficients,
            coefficients_type=coefficients_type,
            field_scan=field_scan,
            field_density=field_density,
            sampling=sampling,
            obscuration=obscuration,
            minimum_plot_scale=minimum_plot_scale,
            maximum_plot_scale=maximum_plot_scale,
        ).run(simple_system)

        assert_frame_equal(result.data, expected_data.data)

    @pytest.mark.parametrize(
        "coefficients,coefficients_type,field_scan,field_density,sampling,obscuration,minimum_plot_scale,maximum_plot_scale",
        [
            ("1-8", "Standard", "+y", 20, "64x64", 0.5, 0, 0),
            ("2", "Standard", "-y", 10, "32x32", 0.5, 0, 0),
            ("1,3,5", "Standard", "+x", 5, "32x32", 0.5, 0, 1),
            ("1-15", "Fringe", "-x", 15, "128x128", 0.5, 1, 5),
            ("1-2,3,5-7", "Annular", "Plus_Y", 1, "32x32", 0.5, 0, 0),
            ("1-2,3,5-7", "Annular", "Minus_Y", 1, "32x32", 0.1, 0, 0),
            ("1-2,3,5-7", "Standard", "Plus_X", 1, "32x32", 0.5, 1, 5),
            ("1-2,3,5-7", "Standard", "Minus_X", 1, "32x32", 0.5, 0, 0),
        ],
    )
    def test_zernike_coefficients_vs_field_matches_reference_data(
        self,
        coefficients,
        coefficients_type,
        field_scan,
        field_density,
        sampling,
        obscuration,
        minimum_plot_scale,
        maximum_plot_scale,
        simple_system,
        reference_data,
    ):
        result = ZernikeCoefficientsVsField(
            coefficients=coefficients,
            coefficients_type=coefficients_type,
            field_scan=field_scan,
            field_density=field_density,
            sampling=sampling,
            obscuration=obscuration,
            minimum_plot_scale=minimum_plot_scale,
            maximum_plot_scale=maximum_plot_scale,
        ).run(simple_system)

        assert_frame_equal(result.data, reference_data.data)
