"""Nonsequential 3D Layout viewer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from zospy.analyses.new.decorators import analysis_settings
from zospy.analyses.new.systemviewers.base import ImageSize, SystemViewerWrapper

if TYPE_CHECKING:
    from zospy.api import _ZOSAPI


@analysis_settings
class NSC3DLayoutSettings:
    """Settings for the nonsequential 3D Layout viewer.

    Notes
    -----
    Not all settings available in OpticStudio are supported yet.
    """

    image_size: ImageSize = Field(default=(800, 600), description="Image size")


class NSC3DLayout(SystemViewerWrapper[NSC3DLayoutSettings]):
    """3D Layout viewer for Non-Sequential systems."""

    TYPE = "NSC3DLayout"
    MODE = "Nonsequential"

    def __init__(self, *, image_size: tuple[int, int] = (800, 600), settings: NSC3DLayoutSettings | None = None):
        """Create a new nonsequential 3D Layout viewer.

        See Also
        --------
        NSC3DLayoutSettings : Settings for the NSC 3D Layout viewer
        """
        super().__init__(settings or NSC3DLayoutSettings(), locals())

    def configure_layout_tool(
        self,
    ) -> _ZOSAPI.Tools.Layouts.INSC3DLayoutExport:
        """Configure the nonsequential 3D Layout viewer."""
        layout_tool = self.oss.Tools.Layouts.OpenNSC3DLayoutExport()

        layout_tool.OutputPixelWidth, layout_tool.OutputPixelHeight = self.settings.image_size

        return layout_tool