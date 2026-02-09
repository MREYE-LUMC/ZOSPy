from __future__ import annotations

from inspect import signature
from typing import TYPE_CHECKING, Any, ClassVar

import pytest

from zospy.functions.lde import (
    _APERTURE_FILE,  # noqa: PLC2701
    _APERTURE_X_DECENTER,  # noqa: PLC2701
    _APERTURE_Y_DECENTER,  # noqa: PLC2701
    _APERTURETYPE_USED_SETTINGS,  # noqa: PLC2701
    _MAXIMUM_RADIUS,  # noqa: PLC2701
    _MINIMUM_RADIUS,  # noqa: PLC2701
    _NUMBER_OF_ARMS,  # noqa: PLC2701
    _UDA_SCALE,  # noqa: PLC2701
    _WIDTH_OF_ARMS,  # noqa: PLC2701
    _X_HALF_WIDTH,  # noqa: PLC2701
    _Y_HALF_WIDTH,  # noqa: PLC2701
    find_surface_by_comment,
    surface_change_aperturetype,
)

if TYPE_CHECKING:
    from zospy.zpcore import OpticStudioSystem


@pytest.mark.parametrize(
    "comment,case_sensitive,expected_indices",
    [
        ("Abcd", True, [0]),  # When using .SurfaceNumber, the returned value matches the LDE numbering (starting at 0)
        ("Abcd", False, [0, 1, 2, 3]),
        ("ABcd", True, [1]),
        ("ABCD", True, []),
        ("ABCD", False, [0, 1, 2, 3]),
        ("efgh", True, []),
        ("efgh", False, []),
    ],
)
def test_can_find_surface_by_comment(simple_system, comment, case_sensitive, expected_indices):
    simple_system.LDE.GetSurfaceAt(0).Comment = "Abcd"
    simple_system.LDE.GetSurfaceAt(1).Comment = "ABcd"
    simple_system.LDE.GetSurfaceAt(2).Comment = "ABCd"
    simple_system.LDE.GetSurfaceAt(3).Comment = "ABCd"

    result = find_surface_by_comment(simple_system.LDE, comment=comment, case_sensitive=case_sensitive)

    indices = [surface.SurfaceNumber for surface in result]

    assert indices == expected_indices


class TestSurfaceChangeApertureType:
    APERTURE_TYPE_PARAMETERS: ClassVar[dict[str, tuple[str, Any]]] = {
        _APERTURE_FILE: ("aperture_file", "square.uda"),
        _APERTURE_X_DECENTER: ("aperture_x_decenter", 0.123),
        _APERTURE_Y_DECENTER: ("aperture_y_decenter", 0.123),
        _MAXIMUM_RADIUS: ("maximum_radius", 1.23),
        _MINIMUM_RADIUS: ("minimum_radius", 0.12),
        _NUMBER_OF_ARMS: ("number_of_arms", 5),
        _UDA_SCALE: ("uda_scale", 2),
        _WIDTH_OF_ARMS: ("width_of_arms", 0.5),
        _X_HALF_WIDTH: ("x_half_width", 0.25),
        _Y_HALF_WIDTH: ("y_half_width", 0.25),
    }

    def test_change_aperturetype_accepts_parameters(self):
        parameters = signature(surface_change_aperturetype).parameters
        for param, _ in self.APERTURE_TYPE_PARAMETERS.values():
            assert param in parameters

    @pytest.mark.parametrize("aperture_type,accepted_parameters", _APERTURETYPE_USED_SETTINGS.items())
    def test_update_aperture_type(self, simple_system: OpticStudioSystem, aperture_type, accepted_parameters):
        surface = simple_system.LDE.GetSurfaceAt(simple_system.LDE.StopSurface)
        parameters = {
            function_param: value
            for api_param, (function_param, value) in self.APERTURE_TYPE_PARAMETERS.items()
            if api_param in accepted_parameters
        }

        surface_change_aperturetype(surface, new_type=aperture_type, **parameters)

        assert str(surface.ApertureData.CurrentType) == aperture_type

        for param in accepted_parameters:
            expected_value = self.APERTURE_TYPE_PARAMETERS[param][1]
            assert getattr(surface.ApertureData.CurrentTypeSettings, param) == expected_value

    @pytest.mark.parametrize("aperture_type,accepted_parameters", _APERTURETYPE_USED_SETTINGS.items())
    def test_change_aperturetype_warns_for_invalid_parameter(
        self, simple_system: OpticStudioSystem, aperture_type, accepted_parameters
    ):
        surface = simple_system.LDE.GetSurfaceAt(simple_system.LDE.StopSurface)

        invalid_parameters = {
            function_param: value
            for api_param, (function_param, value) in self.APERTURE_TYPE_PARAMETERS.items()
            if api_param not in accepted_parameters
        }

        for param, value in invalid_parameters.items():
            with pytest.warns(
                UserWarning, match=rf"Aperture type {aperture_type!s} does not support the specification of \w+"
            ):
                surface_change_aperturetype(surface, new_type=aperture_type, **{param: value})
