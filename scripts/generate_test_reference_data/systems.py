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


BK7_WAVELENGTH = 0.546706
BK7_REFRACTIVE_INDEX = 1.51872


def fabry_perot_system(oss: zp.zpcore.OpticStudioSystem) -> zp.zpcore.OpticStudioSystem:
    """Test system for polarization analyses.

    This system is based on the Fabry-Perot example from Zemax OpticStudio.
    Surface 1 and 2 use hardcoded refractive indices instead of BK7 glass in order
    to ensure consistency between different OpticStudio versions.
    """

    _initialize_system(oss)

    oss.SystemData.Aperture.ApertureType = zp.constants.SystemData.ZemaxApertureType.EntrancePupilDiameter
    oss.SystemData.Aperture.ApertureValue = 5.0
    oss.SystemData.Aperture.FastSemiDiameters = True

    # Set wavelength to 546.706 nm
    oss.SystemData.Wavelengths.GetWavelength(1).Wavelength = BK7_WAVELENGTH

    surface_object = oss.LDE.GetSurfaceAt(0)
    surface_object.SemiDiameter = float("inf")

    surface_stop = oss.LDE.GetSurfaceAt(1)
    surface_stop.Thickness = 2.0
    zp.solvers.material_model(surface_stop.MaterialCell, refractive_index=BK7_REFRACTIVE_INDEX)
    surface_stop.SemiDiameter = 3.0

    surface_coating = oss.LDE.InsertNewSurfaceAt(2)
    surface_coating.Thickness = 2.0
    zp.solvers.material_model(surface_coating.MaterialCell, refractive_index=BK7_REFRACTIVE_INDEX)
    surface_coating.Coating = "FP"
    surface_coating.SemiDiameter = 3.0

    surface_aperture = oss.LDE.InsertNewSurfaceAt(3)
    surface_aperture.Thickness = 5.0
    surface_aperture.SemiDiameter = 3.0

    surface_paraxial = oss.LDE.InsertNewSurfaceAt(4)
    zp.functions.lde.surface_change_type(surface_paraxial, zp.constants.Editors.LDE.SurfaceType.Paraxial)
    surface_paraxial.Thickness = 19.0

    # Focal length
    surface_paraxial.GetCellAt(12).DoubleValue = 20.0

    # OPD Mode
    surface_paraxial.GetCellAt(13).IntegerValue = 1

    return oss
