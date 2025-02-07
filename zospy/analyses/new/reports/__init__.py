"""OpticStudio analyses from the Reports category."""

from zospy.analyses.new.reports.cardinal_points import CardinalPoints, CardinalPointsSettings
from zospy.analyses.new.reports.surface_data import SurfaceData, SurfaceDataSettings
from zospy.analyses.new.reports.system_data import SystemData

__all__ = ("SurfaceData", "SurfaceDataSettings", "SystemData", "CardinalPoints", "CardinalPointsSettings")
