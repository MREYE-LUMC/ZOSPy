"""OpticStudio analyses from the Reports category."""

from zospy.analyses.reports.cardinal_points import CardinalPoints, CardinalPointsSettings
from zospy.analyses.reports.surface_data import SurfaceData, SurfaceDataSettings
from zospy.analyses.reports.system_data import SystemData

__all__ = ("SurfaceData", "SurfaceDataSettings", "SystemData", "CardinalPoints", "CardinalPointsSettings")
