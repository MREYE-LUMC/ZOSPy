from __future__ import annotations

from dataclasses import dataclass

from zospy.api import _ZOSAPI, constants
from zospy.zpcore import OpticStudioSystem


@dataclass(frozen=True)
class PupilData:
    ApertureType: int
    ApertureValue: float
    EntrancePupilDiameter: float
    EntrancePupilPosition: float
    ExitPupilDiameter: float
    ExitPupilPosition: float
    ApodizationType: int
    ApodizationFactor: float


def get_pupil(oss: OpticStudioSystem):
    """Obtains the pupil data.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance.

    Returns
    -------
    PupilData
        The pupildata.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> zp.functions.lde.get_pupil(oss)
    """
    return PupilData(*oss.LDE.GetPupil())


def surface_change_type(surface: _ZOSAPI.Editors.LDE.ILDERow, new_type: constants.Editors.LDE.SurfaceType | str):
    """Simple function to change the type of a surface in the LDE.

    Parameters
    ----------
    surface: ZOSAPI.Editors.LDE.ILDERow
        The Row/Surface for which the change is to be made.
    new_type: zospy.constants.Editors.LDE.SurfaceType | str
        The new surface type, either string (e.g. 'Standard') or int. The integer will be treated as if obtained from
        zp.constants.Editors.LDE.SurfaceType.

    Returns
    -------
    None

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> newsurf = oss.LDE.InsertNewSurfaceAt(0)
    >>> surface_change_type(newsurf, zp.constants.Editors.LDE.SurfaceType.Standard)
    """
    new_type = constants.process_constant(constants.Editors.LDE.SurfaceType, new_type)

    # Apply
    new_surface_type_settings = surface.GetSurfaceTypeSettings(new_type)
    surface.ChangeType(new_surface_type_settings)
