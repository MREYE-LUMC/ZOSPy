"""OpticStudio analyses from the Reports category."""

from __future__ import annotations

from zospy.analyses.reports.cardinal_points import CardinalPoints, CardinalPointsSettings
from zospy.analyses.reports.surface_data import SurfaceData, SurfaceDataSettings
from zospy.analyses.reports.system_data import SystemData

__all__ = ("CardinalPoints", "CardinalPointsSettings", "SurfaceData", "SurfaceDataSettings", "SystemData")
