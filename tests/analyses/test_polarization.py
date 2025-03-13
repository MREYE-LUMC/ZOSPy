import pytest

from tests.helpers import assert_dataclass_equal
from zospy.analyses.polarization import PolarizationPupilMap, PolarizationTransmission


class TestPolarizationTransmission:
    def test_can_run(self, simple_system):
        result = PolarizationTransmission().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = PolarizationTransmission().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "sampling,unpolarized,jx,jy,x_phase,y_phase",
        [
            ("32x32", False, 1, 0, 0, 0),
            ("32x32", False, 0, 1, 0, 0),
            ("32x32", False, 1, 1, 0, 0),
            ("32x32", False, 0.001, 1, 0, 0),
            ("64x64", False, 1, 1, 45, 90),
            ("64x64", True, 1, 0, 0, 0),
        ],
    )
    def test_transmission_returns_correct_result(
        self, polarized_system, sampling, unpolarized, jx, jy, x_phase, y_phase, expected_data
    ):
        result = PolarizationTransmission(
            sampling=sampling, unpolarized=unpolarized, jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase
        ).run(polarized_system)

        assert_dataclass_equal(result.data, expected_data.data)

    @pytest.mark.parametrize(
        "sampling,unpolarized,jx,jy,x_phase,y_phase",
        [
            ("32x32", False, 1, 0, 0, 0),
            ("32x32", False, 0, 1, 0, 0),
            ("32x32", False, 1, 1, 0, 0),
            ("32x32", False, 0.001, 1, 0, 0),
            ("64x64", False, 1, 1, 45, 90),
            ("64x64", True, 1, 0, 0, 0),
        ],
    )
    def test_transmission_matches_reference_data(
        self, polarized_system, sampling, unpolarized, jx, jy, x_phase, y_phase, reference_data
    ):
        result = PolarizationTransmission(
            sampling=sampling, unpolarized=unpolarized, jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase
        ).run(polarized_system)

        assert_dataclass_equal(result.data, reference_data.data)


XFAIL_REASON = "Intentionally skipped for this OpticStudio version. See https://zospy.readthedocs.io/compatibility."


class TestPolarizationPupilMap:
    def test_can_run(self, simple_system):
        result = PolarizationPupilMap().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = PolarizationPupilMap().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "jx,jy,x_phase,y_phase,surface,sampling",
        [
            (1, 0, 0, 0, "Image", "11x11"),
            (1, 1, 0, 0, 2, "11x11"),
            (0, 1, 0, 0, "Image", "11x11"),
            (1, 1, 45, 90, "Image", "17x17"),
        ],
    )
    def test_polarization_pupil_map_returns_correct_result(
        self, polarized_system, jx, jy, x_phase, y_phase, surface, sampling, expected_data
    ):
        result = PolarizationPupilMap(
            jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase, surface=surface, sampling=sampling
        ).run(polarized_system)

        assert_dataclass_equal(result.data, expected_data.data)

    @pytest.mark.parametrize(
        "jx,jy,x_phase,y_phase,surface,sampling",
        [
            pytest.param(
                1,
                0,
                0,
                0,
                "Image",
                "11x11",
                marks=pytest.mark.xfail_for_opticstudio_versions(["20.3.2"], XFAIL_REASON),
            ),
            (1, 1, 0, 0, 2, "11x11"),
            (0, 1, 0, 0, "Image", "11x11"),
            pytest.param(
                1,
                1,
                45,
                90,
                "Image",
                "17x17",
                marks=pytest.mark.xfail_for_opticstudio_versions(["20.3.2"], XFAIL_REASON),
            ),
        ],
    )
    def test_polarization_pupil_map_matches_reference_data(
        self, polarized_system, jx, jy, x_phase, y_phase, surface, sampling, reference_data
    ):
        result = PolarizationPupilMap(
            jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase, surface=surface, sampling=sampling
        ).run(polarized_system)

        assert_dataclass_equal(result.data, reference_data.data)
