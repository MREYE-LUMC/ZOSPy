from __future__ import annotations

import inspect
import json
from dataclasses import dataclass, fields
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import numpy as np
import pytest
from pandas import DataFrame
from pydantic import Field
from pydantic.fields import FieldInfo

from tests.helpers import _all_subclasses
from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import ValidatedDataFrame
from zospy.tools import open_tool
from zospy.tools.base import BaseToolWrapper, ToolResult, ToolSettings
from zospy.tools.quick_focus import QuickFocusSettings

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_mock import MockerFixture

    from zospy.zpcore import OpticStudioSystem


class TestOpenTool:
    def test_open_tool(self, oss: OpticStudioSystem):
        assert oss.Tools.CurrentTool is None

        with open_tool(oss, oss.Tools.OpenBatchRayTrace) as tool:
            assert oss.Tools.CurrentTool == tool

        assert oss.Tools.CurrentTool is None

    def test_close_current(self, oss: OpticStudioSystem):
        assert oss.Tools.CurrentTool is None

        oss.Tools.OpenLocalOptimization()

        with open_tool(oss, oss.Tools.OpenBatchRayTrace, close_current=True) as tool:
            # Testing that the previous tool was closed messes up the OpticStudio connection,
            # but since only one tool can be open at a time, this should be sufficient to verify that the previous tool was closed.
            assert oss.Tools.CurrentTool == tool

        assert oss.Tools.CurrentTool is None

    def test_no_close_current(self, oss: OpticStudioSystem):
        assert oss.Tools.CurrentTool is None

        local_optimization = oss.Tools.OpenLocalOptimization()

        with (
            pytest.raises(RuntimeError, match="Cannot open tool because another tool is already open"),
            open_tool(oss, oss.Tools.OpenBatchRayTrace, close_current=False),
        ):
            pass

        assert oss.Tools.CurrentTool == local_optimization

    def test_closes_after_exception(self, oss: OpticStudioSystem):
        assert oss.Tools.CurrentTool is None

        with (
            pytest.raises(ValueError, match="An error occurred while using the tool"),
            open_tool(oss, oss.Tools.OpenBatchRayTrace),
        ):
            raise ValueError("An error occurred while using the tool")

        assert oss.Tools.CurrentTool is None

    def test_does_not_close_if_already_closed(self, oss: OpticStudioSystem, mocker: MockerFixture):
        assert oss.Tools.CurrentTool is None

        with open_tool(oss, oss.Tools.OpenBatchRayTrace) as tool:
            tool.Close()

            spy = mocker.spy(tool, "Close")

        assert oss.Tools.CurrentTool is None
        spy.assert_not_called()

    def test_does_not_close_other_tool(self, oss: OpticStudioSystem):
        assert oss.Tools.CurrentTool is None

        with open_tool(oss, oss.Tools.OpenBatchRayTrace) as tool:
            tool.Close()

            tool2 = oss.Tools.OpenLocalOptimization()

        assert oss.Tools.CurrentTool == tool2


@dataclass
class MockToolOutputData:
    int_data: int = 1
    string_data: str = "a"


@analysis_settings
class MockToolSettings:
    int_setting: int = Field(default=1, description="An integer setting")
    string_setting: str = Field(default="a", description="A string setting")


class MockTool(BaseToolWrapper[MockToolOutputData, MockToolSettings]):
    def __init__(
        self,
        *,
        int_setting: int = 1,
        string_setting: str = "a",
    ):
        super().__init__(settings_kws=locals())

    def _get_tool_opener(self, oss: OpticStudioSystem) -> Callable[[], Any]:  # noqa: ARG002
        return lambda: SimpleNamespace(
            Close=lambda: None, ErrorMessage=None
        )  # This tool does not actually open anything in OpticStudio

    def _run_tool(self) -> MockToolOutputData:
        return MockToolOutputData()


_tool_wrapper_classes = [c for c in _all_subclasses(BaseToolWrapper) if c not in {MockTool}]


@pytest.fixture(scope="module", params=_tool_wrapper_classes)
def tool_wrapper_class(request):
    return request.param


class TestToolWrapper:
    @staticmethod
    def get_settings_defaults(settings_class):
        result = {}

        for field in fields(settings_class):
            if isinstance(field.default, FieldInfo):
                result[field.name] = field.default.default
            else:
                result[field.name] = field.default

        return result

    def test_get_settings_type(self):
        assert MockTool._settings_type == MockToolSettings  # noqa: SLF001

    def test_settings_type_is_specified(self):
        assert MockTool._settings_type is not ToolSettings  # noqa: SLF001

    def test_tools_correct_tool_opener(self, oss: OpticStudioSystem, tool_wrapper_class):
        instance = tool_wrapper_class()

        try:
            instance._get_tool_opener(oss)  # noqa: SLF001
        except Exception:  # noqa: BLE001
            pytest.fail(f"{tool_wrapper_class.__name__} does not implement _get_tool_opener correctly.")

    def test_init_all_keyword_only_parameters(self, tool_wrapper_class):
        assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(tool_wrapper_class).parameters.values())

    def test_init_contains_all_settings(self, tool_wrapper_class):
        if tool_wrapper_class().settings is None:
            return

        init_signature = inspect.signature(tool_wrapper_class.__init__)
        settings_fields = fields(tool_wrapper_class().settings)

        assert all(field.name in init_signature.parameters for field in settings_fields)

    def test_tools_default_values(self, tool_wrapper_class):
        if tool_wrapper_class().settings is None:
            return

        settings_defaults = self.get_settings_defaults(type(tool_wrapper_class().settings))
        init_signature = inspect.signature(tool_wrapper_class.__init__)

        for field_name, default_value in settings_defaults.items():
            assert field_name in init_signature.parameters
            assert init_signature.parameters[field_name].default == default_value

    def test_change_settings_from_parameters(self):
        tool = MockTool(int_setting=2, string_setting="b")

        assert tool.settings.int_setting == 2
        assert tool.settings.string_setting == "b"

    def test_change_settings_from_object(self):
        settings = MockToolSettings(int_setting=2, string_setting="b")
        tool = MockTool().with_settings(settings)

        assert tool.settings.int_setting == 2
        assert tool.settings.string_setting == "b"

    def test_settings_object_is_copied(self):
        settings = MockToolSettings(int_setting=2, string_setting="b")
        tool = MockTool().with_settings(settings)

        assert tool.settings is not settings
        assert tool.settings == settings

    def test_update_settings_object(self):
        tool = MockTool(int_setting=1, string_setting="a")

        tool.update_settings(settings=MockToolSettings(int_setting=2, string_setting="b"))

        assert tool.settings.int_setting == 2
        assert tool.settings.string_setting == "b"

    def test_update_settings_dictionary(self):
        tool = MockTool(int_setting=1, string_setting="a")

        tool.update_settings(settings_kws={"int_setting": 2, "string_setting": "b"})

        assert tool.settings.int_setting == 2
        assert tool.settings.string_setting == "b"

    def test_update_settings_object_and_dictionary(self):
        tool = MockTool(int_setting=1, string_setting="a")

        tool.update_settings(
            settings=MockToolSettings(int_setting=2, string_setting="a"), settings_kws={"string_setting": "b"}
        )

        assert tool.settings.int_setting == 2
        assert tool.settings.string_setting == "b"

    def test_update_settings_no_dataclass_raises_type_error(self):
        with pytest.raises(TypeError, match="settings should be a dataclass"):
            MockTool().update_settings(settings=123)


class TestAnalysisResultJSONConversion:
    # Only test for non-dataclass results, because dataclass results are tested separately in the corresponding
    # analysis' tests.
    @pytest.mark.parametrize(
        "result_type,result_value,type_info",
        [
            (DataFrame, DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}), {"data_type": "dataframe"}),
            (np.ndarray, np.array([1, 2, 3]), {"data_type": "ndarray"}),
        ],
    )
    def test_data_to_json(self, result_type, result_value, type_info):
        result = ToolResult[result_type, MockToolSettings](
            data=result_value,
            settings=MockToolSettings(),
            error_message=None,
        )

        result_json = result.to_json()
        result_dict = json.loads(result_json)

        assert "__tool_data__" in result_dict
        assert result_dict["__tool_data__"] == type_info

    def test_settings_to_json(self):
        result = ToolResult[ValidatedDataFrame, MockToolSettings](
            data=DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}),
            settings=MockToolSettings(),
            error_message=None,
        )

        result_json = result.to_json()
        result_dict = json.loads(result_json)

        assert "__tool_settings__" in result_dict
        assert result_dict["__tool_settings__"] == {
            "data_type": "zospy_class",
            "name": "MockToolSettings",
            "module": "tests.tools.test_base",
        }

    @pytest.mark.parametrize(
        "result_type,result_value",
        [
            (ValidatedDataFrame, DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})),
            (np.ndarray, np.array([1, 2, 3])),
        ],
    )
    def test_roundtrip(self, result_type, result_value):
        result = ToolResult[result_type, QuickFocusSettings](
            data=result_value,
            settings=QuickFocusSettings(),
            error_message=None,
        )

        result_json = result.to_json()

        result_roundtrip = ToolResult.from_json(result_json)
        assert all(result_roundtrip.data == result.data)
        assert str(result_roundtrip.settings.criterion) == str(result.settings.criterion)
        assert result_roundtrip.settings.use_centroid == result.settings.use_centroid
        assert result_roundtrip.error_message == result.error_message
