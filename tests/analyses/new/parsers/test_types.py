import gc
import json

import numpy as np
import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal
from pydantic import TypeAdapter, ValidationError

from zospy.analyses.new.parsers.types import ValidatedDataFrame, ValidatedNDArray, ZOSAPIConstantAnnotation
from zospy.api import constants

validated_dataframe = TypeAdapter(ValidatedDataFrame)
validated_ndarray = TypeAdapter(ValidatedNDArray)


class TestValidatedDataFrame:
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    @staticmethod
    def dataframe_to_json(df):
        return json.dumps(df.to_dict(orient="tight"))

    def test_validated_dataframe_to_json(self):
        json_data = validated_dataframe.dump_json(self.df).decode("utf-8")

        assert json.loads(json_data) == json.loads(self.dataframe_to_json(self.df))

    def test_validated_dataframe_from_dict(self):
        dictionary = self.df.to_dict(orient="tight")
        df = validated_dataframe.validate_python(dictionary)

        assert_frame_equal(df, self.df)

    def test_validated_dataframe_from_json(self):
        json_data = self.dataframe_to_json(self.df)
        df = validated_dataframe.validate_json(json_data)

        assert_frame_equal(df, self.df)

    def test_validated_dataframe_invalid_dict(self):
        with pytest.raises(ValidationError, match="type=invalid_dataframe"):
            # Dictionary is formatted incorrectly
            validated_dataframe.validate_python({"a": [1, 2, 3], "b": [4, 5]})

    def test_validated_dataframe_invalid_json(self):
        with pytest.raises(ValidationError, match="type=invalid_dataframe"):
            # JSON is formatted incorrectly
            validated_dataframe.validate_json(self.df.to_json(orient="split"))

    def test_validated_dataframe_invalid_type(self):
        with pytest.raises(ValidationError):
            validated_dataframe.validate_python("not a dataframe or dictionary")


class TestValidatedNDArray:
    array = np.array([[1, 2, 3], [4, 5, 6]])

    @staticmethod
    def array_to_json(array):
        return json.dumps(array.tolist())

    def test_validated_ndarray_to_json(self):
        json_data = validated_ndarray.dump_json(self.array).decode("utf-8")

        assert json.loads(json_data) == json.loads(self.array_to_json(self.array))

    def test_validated_ndarray_from_list(self):
        array = validated_ndarray.validate_python(self.array.tolist())

        assert np.array_equal(array, self.array)

    def test_validated_ndarray_from_json(self):
        json_data = self.array_to_json(self.array)
        array = validated_ndarray.validate_json(json_data)

        assert np.array_equal(array, self.array)

    def test_validated_ndarray_invalid_list(self):
        with pytest.raises(ValidationError, match="type=invalid_ndarray"):
            # List is formatted incorrectly
            validated_ndarray.validate_python([[1, 2, 3], [4, 5]])


class TestZOSAPIConstant:
    @staticmethod
    def _get_instances():
        return [obj for obj in gc.get_objects() if isinstance(obj, ZOSAPIConstantAnnotation)]

    @staticmethod
    def _hasattr(obj, attr):
        for name in attr.split("."):
            if not hasattr(obj, name):
                return False

            obj = getattr(obj, name)

        return True

    @pytest.mark.parametrize("annotation", _get_instances())
    def test_constant_exists(self, zos, annotation):  # noqa: ARG002
        assert self._hasattr(constants, annotation.enum)
