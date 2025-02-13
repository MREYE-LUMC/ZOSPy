import pytest
from pandas.testing import assert_frame_equal

from zospy.analyses.new.mtf import FFTThroughFocusMTF, HuygensMTF


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


class TestHuygensMTF:
    def test_can_run(self, simple_system):
        result = HuygensMTF().run(simple_system)
        assert result.data is not None

    def test_to_json(self, simple_system):
        result = HuygensMTF().run(simple_system)
        assert result.from_json(result.to_json()).to_json() == result.to_json()
