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
    >>> zp.functions.lde.surface_change_type(newsurf, zp.constants.Editors.LDE.SurfaceType.Standard)
    """
    new_type = constants.process_constant(constants.Editors.LDE.SurfaceType, new_type)

    # Apply
    new_surface_type_settings = surface.GetSurfaceTypeSettings(new_type)
    surface.ChangeType(new_surface_type_settings)


def find_surface_by_comment(
    lde: _ZOSAPI.Editors.LDE, comment: str, case_sensitive: bool = True
) -> list[_ZOSAPI.Editors.LDE.ILDERow]:
    """Returns a list of surfaces from the LDE that have the supplied string as Comment.

    In case of multiple matches, the surfaces are returned in ascending order.

    Parameters
    ----------
    lde: ZOSAPI.Editors.LDE
        The Lens Data Editor (LDE)
    comment: str
        String that is searched for in the Comment column of the LDE.
    case_sensitive: bool
        Flag that specifies whether the search is case-sensitive or not. Defaults to True.

    Returns
    -------
    list[ZOSAPI.Editors.LDE.ILDERow]
        A list of surfaces in the LDE that have a Comment column value which matches the supplied comment argument.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.wakeup()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> newobj1 = oss.LDE.GetSurfaceAt(0)
    >>> newobj1.Comment = 'aa'
    >>> newobj2 = oss.LDE.GetSurfaceAt(1)
    >>> newobj2.Comment = 'bb'
    >>> newobj3 = oss.LDE.GetSurfaceAt(2)
    >>> newobj3.Comment = 'aA'
    >>> zp.functions.lde.find_surface_by_comment(oss.LDE, 'aa')
    """
    # Is the search case-sensitive?
    if not case_sensitive:
        # If the search is NOT case-sensitive put comment argument in all small letters
        comment = comment.lower()

    # Initialize list of return indexes corresponding to LDE rows with matched Comment column

    return_indices = []
    # Loop over the objects and check the comments

    for surface_index in range(lde.NumberOfSurfaces):
        # Retrieve current object comment
        surface = lde.GetSurfaceAt(surface_index)
        surface_comment = surface.Comment

        # Is the search case-sensitive?
        if not case_sensitive:
            # If the search is NOT case-sensitive put current object comment in all small letters
            surface_comment = surface_comment.lower()

        # If the comment matches, store the corresponding object index
        if comment == surface_comment:
            return_indices.append(surface)

    # Return list of matched inices
    return return_indices
