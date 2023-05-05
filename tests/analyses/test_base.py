from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from zospy.analyses.base import (
    AnalysisMessage,
    AnalysisMetadata,
    AnalysisResult,
    AttrDict,
    OnComplete,
    _AnalysisResultJSONDecoder,
    _AnalysisResultJSONEncoder,
)


def test_oncomplete():
    assert OnComplete.Close == "Close"
    assert OnComplete.Sustain == "Sustain"
    assert OnComplete.Release == "Release"

    with pytest.raises(ValueError):
        OnComplete("NonExistentValue")


class TestToJSON:
    @pytest.fixture(scope="class")
    def example_analysis_result(self):
        metadata = AnalysisMetadata(
            DateTime=datetime.now(),
            LensFile="C:\\Path\\To\\Lens\\File.ZOS",
            LensTitle="LensTitle",
            FeatureDescription="",
        )
        messages = [AnalysisMessage(ErrorCode="EC", Message="message")]

        return AnalysisResult(
            analysistype="DummyAnalysis",
            data=AttrDict(
                a=pd.Series(dict(b=1, c=2, d=3, e=4)),
                f=pd.DataFrame(dict(g=[5.6, 7.8, 9.10, 11.12], h=["i", "j", "k", "l"])),
                m="a useless string",
            ),
            metadata=metadata,
            messages=messages,
        )

    def test_restore_metadata(self, example_analysis_result):
        restored_result = AnalysisResult.from_json(example_analysis_result.to_json())

        assert isinstance(restored_result.MetaData, AnalysisMetadata)
        assert example_analysis_result.MetaData == restored_result.MetaData

    def test_restore_messages(self, example_analysis_result):
        restored_result = AnalysisResult.from_json(example_analysis_result.to_json())

        assert isinstance(restored_result.Messages[0], AnalysisMessage)
        assert example_analysis_result.Messages == restored_result.Messages

    def test_restore_attrdict(self, example_analysis_result):
        restored_result = AnalysisResult.from_json(example_analysis_result.to_json())

        assert isinstance(restored_result.Data, AttrDict)

    def test_restore_pandas_series(self):
        series = pd.Series(dict(a=1, b=2, c=3), dtype=float)

        restored_series = _AnalysisResultJSONDecoder().decode(_AnalysisResultJSONEncoder().encode(series))

        assert isinstance(restored_series, pd.Series)
        assert all(restored_series == series)

    def test_restore_pandas_multi_index_series(self):
        index = pd.MultiIndex.from_product((["a", "b"], [1, 2]))
        series = pd.Series([123, 456, 345, 678], index=index)

        restored_series = _AnalysisResultJSONDecoder().decode(_AnalysisResultJSONEncoder().encode(series))

        assert isinstance(restored_series, pd.Series)
        assert isinstance(restored_series.index, pd.MultiIndex)
        assert all(restored_series == series)

    def test_restore_pandas_dataframe(self):
        dataframe = pd.DataFrame(
            dict(
                int_column=[1, 2, 3, 4],
                float_column=[1.2, 3.4, 5.6, 7.8],
                str_column=["this", "ain't", "string", "theory"],
            )
        )

        restored_dataframe = _AnalysisResultJSONDecoder().decode(_AnalysisResultJSONEncoder().encode(dataframe))

        assert isinstance(restored_dataframe, pd.DataFrame)
        assert all(restored_dataframe == dataframe)

    def test_restore_numpy_ndarray(self):
        array = np.array([1.2345, 2.3456, 3.4567, 4.5678])

        restored_array = _AnalysisResultJSONDecoder().decode(_AnalysisResultJSONEncoder().encode(array))

        assert isinstance(restored_array, np.ndarray)
        assert all(restored_array == array)

    def test_restore_datetime(self):
        test_datetime = datetime(year=2023, month=4, day=17, hour=10, minute=41, second=42, microsecond=43)

        restored_datetime = _AnalysisResultJSONDecoder().decode(_AnalysisResultJSONEncoder().encode(test_datetime))

        assert isinstance(restored_datetime, datetime)
        assert restored_datetime == test_datetime
