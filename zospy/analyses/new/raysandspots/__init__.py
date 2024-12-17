"""OpticStudio analyses from the Rays and spots category."""

from zospy.analyses.new.raysandspots.ray_fan import RayFan, RayFanSettings
from zospy.analyses.new.raysandspots.single_ray_trace import (
    SingleRayTrace,
    SingleRayTraceSettings,
)

__all__ = ("SingleRayTrace", "SingleRayTraceSettings", "RayFan", "RayFanSettings")
