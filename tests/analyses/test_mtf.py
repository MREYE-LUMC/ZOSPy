from typing import ClassVar

import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.mtf import FFTThroughFocusMTF, HuygensMTF


class TestFFTThroughFocusMTF:
    def test_can_run(self, simple_system):
        result = FFTThroughFocusMTF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = FFTThroughFocusMTF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "fieldx,fieldy", [(0, 0), (5.5, 0), (0, 5.5), (5.5, 5.5), (-5.5, 0), (0, -5.5), (-5.5, -5.5)]
    )
    def test_field_parsing(self, fieldx, fieldy, simple_system):
        field1 = simple_system.SystemData.Fields.GetField(1)
        field1.X = fieldx
        field1.Y = fieldy
        result = FFTThroughFocusMTF().run(simple_system)

        assert result.data[0].field_coordinate.value[0] == fieldx
        assert result.data[0].field_coordinate.value[1] == fieldy

    @pytest.mark.parametrize("fields", [[(5.5, -5.5)], [(0, 0), (0.0, 5.5), (5.5, 0.0), (5.5, -5.5)]])
    def test_to_dataframe(self, fields, simple_system):
        field1 = simple_system.SystemData.Fields.GetField(1)
        field1.X = fields[0][0]
        field1.Y = fields[0][1]

        for f in fields[1:]:
            simple_system.SystemData.Fields.AddField(f[0], f[1], 1.0)

        result = FFTThroughFocusMTF().run(simple_system)

        df = result.data.to_dataframe()

        for r in result.data:
            assert_frame_equal(
                df.loc[
                    (df["FieldX"] == r.field_coordinate.value[0]) & (df["FieldY"] == r.field_coordinate.value[1]),
                    r.data.reset_index(drop=False).columns,
                ].reset_index(drop=True),
                r.data.reset_index(drop=False),
            )

    @pytest.mark.parametrize(
        "sampling,delta_focus,frequency,number_of_steps,mtf_type",
        [("64x64", 0.1, 0, 5, "Modulation"), ("128x128", 0.3, 3, 10, "Imaginary")],
    )
    def test_fft_through_focus_mtf_returns_correct_result(
        self, simple_system, sampling, delta_focus, frequency, number_of_steps, mtf_type, expected_data
    ):
        result = FFTThroughFocusMTF(
            sampling=sampling,
            delta_focus=delta_focus,
            frequency=frequency,
            number_of_steps=number_of_steps,
            mtf_type=mtf_type,
        ).run(simple_system)

        for i in range(len(result.data)):
            assert_frame_equal(result.data[i].data, expected_data.data[i].data)

    @pytest.mark.parametrize(
        "sampling,delta_focus,frequency,number_of_steps,mtf_type",
        [("64x64", 0.1, 0, 5, "Modulation"), ("128x128", 0.3, 3, 10, "Imaginary")],
    )
    def test_fft_through_focus_mtf_matches_reference_data(
        self, simple_system, sampling, delta_focus, frequency, number_of_steps, mtf_type, reference_data
    ):
        result = FFTThroughFocusMTF(
            sampling=sampling,
            delta_focus=delta_focus,
            frequency=frequency,
            number_of_steps=number_of_steps,
            mtf_type=mtf_type,
        ).run(simple_system)

        for i in range(len(result.data)):
            assert_frame_equal(result.data[i].data, reference_data.data[i].data)

    _FFT_THROUGH_FOCUS_MTF_MTFTYPE_EXPECTED_RETURN: ClassVar = {
        # The expected return does not match constants.Analysis.Settings.Mtf.MtfTypes for fft_through_focus_mtf
        "Modulation": "5",
        "Real": "6",
        "Imaginary": "7",
        "Phase": "8",
        "SquareWave": "9",
    }

    @pytest.mark.parametrize(
        "mtf_type",
        ["Modulation", "Real", "Imaginary", "Phase", "SquareWave"],
    )
    def test_fft_through_focus_mtf_sets_mtftype_correctly(self, simple_system, mtf_type):
        analysis = FFTThroughFocusMTF(mtf_type=mtf_type)
        analysis.run(simple_system, oncomplete="Sustain")

        assert str(analysis.analysis.Settings.Type) == self._FFT_THROUGH_FOCUS_MTF_MTFTYPE_EXPECTED_RETURN[mtf_type]


class TestHuygensMTF:
    def test_can_run(self, simple_system):
        result = HuygensMTF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = HuygensMTF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,mtf_type,maximum_frequency",
        [
            ("64x64", "64x64", 0.0, "Modulation", 150.0),
            ("32x32", "64x64", 1.0, "Modulation", 450.0),
            ("128x128", "128x128", 0.0, "Modulation", 314.5),
            ("32x32", "32x32", 0.0, "Modulation", 150.0),
        ],
    )
    def test_huygens_mtf_returns_correct_result(
        self, simple_system, pupil_sampling, image_sampling, image_delta, mtf_type, maximum_frequency, expected_data
    ):
        result = HuygensMTF(
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            mtf_type=mtf_type,
            maximum_frequency=maximum_frequency,
        ).run(simple_system)

        assert_frame_equal(result.data, expected_data.data)

    @pytest.mark.parametrize(
        "pupil_sampling,image_sampling,image_delta,mtf_type,maximum_frequency",
        [
            ("64x64", "64x64", 0.0, "Modulation", 150.0),
            ("32x32", "64x64", 1.0, "Modulation", 450.0),
            ("128x128", "128x128", 0.0, "Modulation", 314.5),
            ("32x32", "32x32", 0.0, "Modulation", 150.0),
        ],
    )
    def test_huygens_mtf_matches_reference_data(
        self, simple_system, pupil_sampling, image_sampling, image_delta, mtf_type, maximum_frequency, reference_data
    ):
        result = HuygensMTF(
            pupil_sampling=pupil_sampling,
            image_sampling=image_sampling,
            image_delta=image_delta,
            mtf_type=mtf_type,
            maximum_frequency=maximum_frequency,
        ).run(simple_system)

        assert_frame_equal(result.data, reference_data.data)
