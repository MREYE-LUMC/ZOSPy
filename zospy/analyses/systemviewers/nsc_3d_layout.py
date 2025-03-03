"""Nonsequential 3D Layout viewer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from zospy.analyses.decorators import analysis_settings
from zospy.analyses.systemviewers.base import ImageSize, SystemViewerWrapper

if TYPE_CHECKING:
    from zospy.api import _ZOSAPI

__all__ = ("NSC3DLayout", "NSC3DLayoutSettings")


@analysis_settings
class NSC3DLayoutSettings:
    """Settings for the nonsequential 3D Layout viewer.

    Notes
    -----
    Not all settings available in OpticStudio are supported yet.
    """

    image_size: ImageSize = Field(default=(800, 600), description="Image size")


class NSC3DLayout(SystemViewerWrapper[NSC3DLayoutSettings], analysis_type="NSC3DLayout", mode="Nonsequential"):
    """3D Layout viewer for Non-Sequential systems."""

    def __init__(self, *, image_size: tuple[int, int] = (800, 600)):
        """Create a new nonsequential 3D Layout viewer.

        See Also
        --------
        NSC3DLayoutSettings : Settings for the NSC 3D Layout viewer
        """
        super().__init__(settings_kws=locals())

    def configure_layout_tool(
        self,
    ) -> _ZOSAPI.Tools.Layouts.INSC3DLayoutExport:
        """Configure the nonsequential 3D Layout viewer."""
        layout_tool = self.oss.Tools.Layouts.OpenNSC3DLayoutExport()

        layout_tool.OutputPixelWidth, layout_tool.OutputPixelHeight = self.settings.image_size

        return layout_tool
