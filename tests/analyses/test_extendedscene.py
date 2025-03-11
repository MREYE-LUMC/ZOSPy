import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.extendedscene import GeometricImageAnalysis


class TestGeometricImageAnalysis:
    def test_can_run(self, simple_system):
        result = GeometricImageAnalysis().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = GeometricImageAnalysis().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "image_size,expected_minx,expected_miny",
        [
            (1, -0.5, -0.5),
            (1.4, -0.7, -0.7),
            (2.5, -1.25, -1.25),
            (20, -10, -10),
        ],
    )
    def test_geometric_image_analysis_returns_correct_origin(
        self, simple_system, image_size, expected_minx, expected_miny
    ):
        number_of_pixels = 100
        result = GeometricImageAnalysis(image_size=image_size, number_of_pixels=number_of_pixels).run(simple_system)

        pixel_width = image_size / number_of_pixels
        pixel_height = image_size / number_of_pixels

        # Adjust expected_minx and expected_miny with respectively 0.5 * pixel_width and 0.5 * pixel_height as the
        # columns and index from result.data provide the pixel center rather than the bottom left corner of the pixel,
        # while expected_minx and expected_miny point to that bottom left corner.
        assert result.data.columns[0] == (expected_minx + 0.5 * pixel_width)
        assert result.data.index[0] == (expected_miny + 0.5 * pixel_height)

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
        result = GeometricImageAnalysis(
            show_as=show_as, field_size=field_size, total_watts=total_watts, rays_x_1000=rays_x_1000
        ).run(simple_system)

        # Data in result.Data
        # rtol lower than normal due to randomness in calculated rays
        assert_frame_equal(result.data, expected_data.data, rtol=1e-2)

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
        result = GeometricImageAnalysis(
            show_as=show_as, field_size=field_size, total_watts=total_watts, rays_x_1000=rays_x_1000
        ).run(simple_system)

        # Data in result.Data
        # rtol lower than normal due to randomness in calculated rays
        assert_frame_equal(result.data, reference_data.data, rtol=1e-2)
