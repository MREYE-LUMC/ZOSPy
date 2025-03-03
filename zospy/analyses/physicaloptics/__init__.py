"""OpticStudio analyses from the Physical Optics category."""

from zospy.analyses.physicaloptics.physical_optics_propagation import (
    PhysicalOpticsPropagation,
    PhysicalOpticsPropagationSettings,
    create_beam_parameter_dict,
    create_fiber_parameter_dict,
)

__all__ = (
    "PhysicalOpticsPropagation",
    "PhysicalOpticsPropagationSettings",
    "create_beam_parameter_dict",
    "create_fiber_parameter_dict",
)
