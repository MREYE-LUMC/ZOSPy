import numpy as np
import pytest

from zospy.analyses.old.extendedscene import geometric_image_analysis

pytestmark = pytest.mark.old_analyses


class TestGeometricImageAnalysis:
    def test_can_run_geometric_image_analysis(self, simple_system):
        result = geometric_image_analysis(simple_system)

        assert result.Data is not None

    def test_to_json(self, simple_system):
        result = geometric_image_analysis(simple_system)

        assert result.from_json(result.to_json())

    @pytest.mark.parametrize(
        "show_as,field_size,total_watts,rays_x_1000",
        [
            ("Surface", 0, 1, 100000),
            ("Surface", 10, 1, 100000),
            ("Surface", 10, 100, 100000),
            ("Surface", 0, 100, 100000),
            ("CrossX", 0, 1, 100000),
            ("CrossX", 10, 1, 100000),
            ("CrossX", 10, 100, 100000),
            ("CrossX", 0, 100, 100000),
        ],
    )
    def test_geometric_image_analysis_returns_correct_result(
        self, simple_system, show_as, field_size, total_watts, rays_x_1000, expected_data
    ):
        result = geometric_image_analysis(
            simple_system, show_as=show_as, field_size=field_size, total_watts=total_watts, rays_x_1000=rays_x_1000
        )

        # Data in result.Data
        # rtol lower than normal due to randomness in calculated rays
        assert np.allclose(
            result.Data.to_numpy(dtype=float), expected_data.Data.to_numpy(dtype=float), equal_nan=True, rtol=1e-2
        )

    @pytest.mark.parametrize(
        "show_as,field_size,total_watts,rays_x_1000",
        [
            ("Surface", 0, 1, 100000),
            ("Surface", 10, 1, 100000),
            ("Surface", 10, 100, 100000),
            ("Surface", 0, 100, 100000),
            ("CrossX", 0, 1, 100000),
            ("CrossX", 10, 1, 100000),
            ("CrossX", 10, 100, 100000),
            ("CrossX", 0, 100, 100000),
        ],
    )
    def test_geometric_image_analysis_matches_reference_data(
        self, simple_system, show_as, field_size, total_watts, rays_x_1000, reference_data
    ):
        result = geometric_image_analysis(
            simple_system, show_as=show_as, field_size=field_size, total_watts=total_watts, rays_x_1000=rays_x_1000
        )

        # Data in result.Data
        # rtol lower than normal due to randomness in calculated rays
        assert np.allclose(
            result.Data.to_numpy(dtype=float), reference_data.Data.to_numpy(dtype=float), equal_nan=True, rtol=1e-2
        )
