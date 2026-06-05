from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from zospy.tools import QuickFocus

if TYPE_CHECKING:
    from zospy.zpcore import OpticStudioSystem


def test_quick_focus(simple_system: OpticStudioSystem):
    """Test the Quick Focus tool."""
    simple_system.LDE.GetSurfaceAt(3).Thickness = 30

    QuickFocus().run(simple_system)

    assert simple_system.LDE.GetSurfaceAt(3).Thickness == pytest.approx(19.777975)
