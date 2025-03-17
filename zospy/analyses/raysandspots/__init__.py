"""OpticStudio analyses from the Rays and spots category."""

from zospy.analyses.raysandspots.ray_fan import RayFan, RayFanSettings
from zospy.analyses.raysandspots.single_ray_trace import (
    SingleRayTrace,
    SingleRayTraceSettings,
)

__all__ = ("SingleRayTrace", "SingleRayTraceSettings", "RayFan", "RayFanSettings")
