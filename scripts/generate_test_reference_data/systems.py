from __future__ import annotations

import zospy as zp


def _initialize_system(
    oss: zp.zpcore.OpticStudioSystem,
    aperture_type: zp.constants.SystemData.ZemaxApertureType | str = "FloatByStopSize",
    wavelength: float = 543,
):
    oss.new()

    oss.SystemData.Aperture.ApertureType = zp.constants.process_constant(
        zp.constants.SystemData.ZemaxApertureType, aperture_type
    )
    oss.SystemData.Wavelengths.GetWavelength(1).Wavelength = wavelength / 1000


def empty_system(oss: zp.zpcore.OpticStudioSystem) -> zp.zpcore.OpticStudioSystem:
    _initialize_system(oss)

    return oss


def simple_system(oss: zp.zpcore.OpticStudioSystem) -> zp.zpcore.OpticStudioSystem:
    _initialize_system(oss)

    surface_object = oss.LDE.GetSurfaceAt(0)
    surface_object.Thickness = float("inf")

    surface_stop = oss.LDE.GetSurfaceAt(1)
    surface_stop.SemiDiameter = 1

    lens_front = oss.LDE.InsertNewSurfaceAt(2)
    lens_front.Comment = "lens front"
    lens_front.Radius = 20
    lens_front.Thickness = 1
    zp.solvers.material_model(lens_front.MaterialCell, refractive_index=1.5)

    lens_back = oss.LDE.InsertNewSurfaceAt(3)
    lens_back.Comment = "lens back"
    lens_back.Radius = -20
    lens_back.Thickness = 19.792

    return oss
