from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from zospy.functions.tools import open_tool

if TYPE_CHECKING:
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
