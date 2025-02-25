"""Shaded Model viewer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from zospy.analyses.decorators import analysis_settings
from zospy.analyses.systemviewers.base import ImageSize, SystemViewerWrapper

if TYPE_CHECKING:
    from zospy.api import _ZOSAPI

__all__ = ("ShadedModel", "ShadedModelSettings")


@analysis_settings
class ShadedModelSettings:
    """Settings for the Shaded Model viewer.

    Notes
    -----
    Not all settings available in OpticStudio are supported yet.
    """

    image_size: ImageSize = Field(default=(800, 600), description="Image size")


class ShadedModel(SystemViewerWrapper[ShadedModelSettings], analysis_type="ShadedModel", mode="Sequential"):
    """Shaded Model viewer."""

    def __init__(self, *, image_size: tuple[int, int] = (800, 600)):
        """Initialize the Shaded Model viewer.

        See Also
        --------
        ShadedModelSettings : Settings for the Shaded Model viewer.
        """
        super().__init__(settings_kws=locals())

    def configure_layout_tool(
        self,
    ) -> _ZOSAPI.Tools.Layouts.IShadedModelExport:
        """Configure the shaded model viewer."""
        layout_tool = self.oss.Tools.Layouts.OpenShadedModelExport()

        layout_tool.OutputPixelWidth, layout_tool.OutputPixelHeight = self.settings.image_size

        return layout_tool
