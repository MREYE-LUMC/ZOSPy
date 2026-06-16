"""Quick Focus Tool."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from zospy.analyses.decorators import analysis_settings
from zospy.analyses.parsers.types import ZOSAPIConstant  # noqa: TC001
from zospy.api import constants
from zospy.api.constants import process_constant
from zospy.tools.base import BaseToolWrapper

if TYPE_CHECKING:
    from collections.abc import Callable

    from zospy.api import _ZOSAPI

__all__ = ("QuickFocus", "QuickFocusSettings")


@analysis_settings
class QuickFocusSettings:
    """Settings for the Quick Focus tool.

    Attributes
    ----------
    criterion : constants.Tools.General.QuickFocusCriterion | str
        The criterion to use for quick focusing. Defaults to 'SpotSizeRadial'.
    use_centroid : bool
        Reference all calculations to the image centroid rather than the chief ray. Defaults to True.
    """

    criterion: ZOSAPIConstant("Tools.General.QuickFocusCriterion") = Field(default="SpotSizeRadial")
    use_centroid: bool = Field(default=True)


class QuickFocus(BaseToolWrapper[None, QuickFocusSettings]):
    """Wrapper for the Quick Focus tool."""

    def __init__(
        self,
        *,
        criterion: str | constants.Tools.General.QuickFocusCriterion = "SpotSizeRadial",
        use_centroid: bool = True,
    ) -> None:
        """Initialize the Quick Focus tool.

        See Also
        --------
        QuickFocusSettings : Settings for the Quick Focus tool.
        """
        super().__init__(settings_kws=locals())

    def _get_tool_opener(self, oss) -> Callable[[], _ZOSAPI.Tools.General.IQuickFocus]:
        """Get a callable that opens the Quick Focus tool in OpticStudio and returns the tool object."""
        return oss.Tools.OpenQuickFocus

    def _run_tool(self, tool: _ZOSAPI.Tools.General.IQuickFocus) -> None:
        """Run the Quick Focus tool."""
        tool.Criterion = process_constant(constants.Tools.General.QuickFocusCriterion, self.settings.criterion)
        tool.UseCentroid = self.settings.use_centroid

        tool.RunAndWaitForCompletion()
