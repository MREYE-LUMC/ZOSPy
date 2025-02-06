"""Utility functions for the Lens Data Editor (LDE) in OpticStudio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from warnings import warn

from zospy.api import _ZOSAPI, constants

if TYPE_CHECKING:
    from zospy.zpcore import OpticStudioSystem

__all__ = ("get_pupil", "surface_change_type", "find_surface_by_comment", "surface_change_aperturetype")


@dataclass(frozen=True)
class PupilData:
    """OpticStudio pupil data.

    Attributes
    ----------
    ApertureType : int
        The aperture type.
    ApertureValue : float
        The aperture value.
    EntrancePupilDiameter : float
        The entrance pupil diameter.
    EntrancePupilPosition : float
        The entrance pupil position.
    ExitPupilDiameter : float
        The exit pupil diameter.
    ExitPupilPosition : float
        The exit pupil position.
    ApodizationType : int
        The apodization type.
    ApodizationFactor : float
        The apodization factor.
    """

    ApertureType: int
    ApertureValue: float
    EntrancePupilDiameter: float
    EntrancePupilPosition: float
    ExitPupilDiameter: float
    ExitPupilPosition: float
    ApodizationType: int
    ApodizationFactor: float


def get_pupil(oss: OpticStudioSystem):
    """Obtain the pupil data from the optical system.

    Parameters
    ----------
    oss : zospy.zpcore.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance.

    Returns
    -------
    PupilData
        The pupildata.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.connect()
    >>> zp.functions.lde.get_pupil(oss)
    """
    return PupilData(*oss.LDE.GetPupil())


def surface_change_type(
    surface: _ZOSAPI.Editors.LDE.ILDERow, new_type: constants.Editors.LDE.SurfaceType | str, filename=None
):
    """Change the type of a surface in the Lens Data Editor.

    Parameters
    ----------
    surface : ZOSAPI.Editors.LDE.ILDERow
        The Row/Surface for which the change is to be made.
    new_type : zospy.constants.Editors.LDE.SurfaceType | str
        The new surface type, either string (e.g. 'Standard') or int. The integer will be treated as if obtained from
        zp.constants.Editors.LDE.SurfaceType.

    Returns
    -------
    None

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.connect()
    >>> new_surface = oss.LDE.InsertNewSurfaceAt(0)
    >>> zp.functions.lde.surface_change_type(
    ...     new_surface, zp.constants.Editors.LDE.SurfaceType.Standard
    ... )
    """
    new_type = constants.process_constant(constants.Editors.LDE.SurfaceType, new_type)

    # Apply
    new_surface_type_settings = surface.GetSurfaceTypeSettings(new_type)

    if new_surface_type_settings.RequiresFile:
        if filename is None:
            raise ValueError(f"Surface type {new_type!s} requires the specification of a filename.")
        if filename not in list(new_surface_type_settings.GetFileNames()):
            raise ValueError(
                f"Filename '{filename}' is not listed as valid filename for this surface type. The "
                f"accepted names for this surface type are: "
                f"{', '.join(list(new_surface_type_settings.GetFileNames()))}"
            )
        new_surface_type_settings.Filename = filename

    surface.ChangeType(new_surface_type_settings)


def find_surface_by_comment(
    lde: _ZOSAPI.Editors.LDE, comment: str, *, case_sensitive: bool = True
) -> list[_ZOSAPI.Editors.LDE.ILDERow]:
    """Retrieve surfaces from the Lens Data Editor that have the supplied string as Comment.

    In case of multiple matches, the surfaces are returned in ascending order.

    Parameters
    ----------
    lde : ZOSAPI.Editors.LDE
        The Lens Data Editor (LDE)
    comment : str
        String that is searched for in the Comment column of the LDE.
    case_sensitive : bool
        Flag that specifies whether the search is case-sensitive or not. Defaults to True.

    Returns
    -------
    list[ZOSAPI.Editors.LDE.ILDERow]
        A list of surfaces in the LDE that have a Comment column value which matches the supplied comment argument.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.connect()
    >>> lde_object_1 = oss.LDE.GetSurfaceAt(0)
    >>> lde_object_1.Comment = "aa"
    >>> lde_object_2 = oss.LDE.GetSurfaceAt(1)
    >>> lde_object_2.Comment = "bb"
    >>> lde_object_3 = oss.LDE.GetSurfaceAt(2)
    >>> lde_object_3.Comment = "aA"
    >>> zp.functions.lde.find_surface_by_comment(oss.LDE, "aa")
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


# Define constants for the aperture settings
_APERTURE_FILE = "ApertureFile"
_APERTURE_X_DECENTER = "ApertureXDecenter"
_APERTURE_Y_DECENTER = "ApertureYDecenter"
_MAXIMUM_RADIUS = "MaximumRadius"
_MINIMUM_RADIUS = "MinimumRadius"
_NUMBER_OF_ARMS = "NumberOfArms"
_WIDTH_OF_ARMS = "WidthOfArms"
_X_HALF_WIDTH = "XHalfWidth"
_Y_HALF_WIDTH = "YHalfWidth"
_UDA_SCALE = "UDAScale"

# Define a dictionary with accepted constants
_APERTURETYPE_USED_SETTINGS = {
    "None": (),
    "CircularAperture": (_APERTURE_X_DECENTER, _APERTURE_Y_DECENTER, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "CircularObscuration": (_APERTURE_X_DECENTER, _APERTURE_Y_DECENTER, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "Spider": (_NUMBER_OF_ARMS, _WIDTH_OF_ARMS, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "RectangularAperture": (_X_HALF_WIDTH, _Y_HALF_WIDTH, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "RectangularObscuration": (_X_HALF_WIDTH, _Y_HALF_WIDTH, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "EllipticalAperture": (_X_HALF_WIDTH, _Y_HALF_WIDTH, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "EllipticalObscuration": (_X_HALF_WIDTH, _Y_HALF_WIDTH, _MAXIMUM_RADIUS, _MINIMUM_RADIUS),
    "UserAperture": (_APERTURE_FILE, _APERTURE_X_DECENTER, _APERTURE_Y_DECENTER, _UDA_SCALE),
    "UserObscuration": (_APERTURE_FILE, _APERTURE_X_DECENTER, _APERTURE_Y_DECENTER, _UDA_SCALE),
    "FloatingAperture": (),
}


def surface_change_aperturetype(
    surface: _ZOSAPI.Editors.LDE.ILDERow,
    new_type: constants.Editors.LDE.SurfaceApertureTypes | str,
    aperture_file: str | None = None,
    aperture_x_decenter: float | None = None,
    aperture_y_decenter: float | None = None,
    maximum_radius: float | None = None,
    minimum_radius: float | None = None,
    number_of_arms: int | None = None,
    uda_scale: float | None = None,
    width_of_arms: float | None = None,
    x_half_width: float | None = None,
    y_half_width: float | None = None,
) -> None:
    """Change the aperturetype of a surface in the Lens Data Editor.

    Be aware that while all aperture parameters can be specified, only the ones accepted by the new_type should be
    given, any parameter that is not None but not accepted by the new type will result in a UserWarning and will not be
    used. Keeping a parameter on None will result in the default values used by the local OpticStudio instance.

    Parameters
    ----------
    surface : ZOSAPI.Editors.LDE.ILDERow
        The Row/Surface for which the change is to be made.
    new_type : zospy.constants.Editors.LDE.SurfaceApertureTypes | str
        The new surface aperture type.
    aperture_file : str | None
        The aperture file. Defaults to None.
    aperture_x_decenter : int | None
        The x decenter of the aperture. Defaults to None.
    aperture_y_decenter : int | None
        The y decenter of the aperture. Defaults to None.
    maximum_radius : float | None
        The maximum radius. Defaults to None.
    minimum_radius : float | None
        The minimum radius. Defaults to None.
    number_of_arms : int | None
        The number of arms. Defaults to None.
    uda_scale : float | None
        The UDA scale. Defaults to None.
    width_of_arms : float | None
        The width of arms. Defaults to None.
    x_half_width : float | None
        The x half width. Defaults to None
    y_half_width : float | None
        The y half width. Defaults to None

    Returns
    -------
    None
    """
    new_type = constants.process_constant(constants.Editors.LDE.SurfaceApertureTypes, new_type)

    new_aperturetype_settings = surface.ApertureData.CreateApertureTypeSettings(new_type)

    for param, attr_name in [
        (aperture_file, _APERTURE_FILE),
        (aperture_x_decenter, _APERTURE_X_DECENTER),
        (aperture_y_decenter, _APERTURE_Y_DECENTER),
        (maximum_radius, _MAXIMUM_RADIUS),
        (minimum_radius, _MINIMUM_RADIUS),
        (number_of_arms, _NUMBER_OF_ARMS),
        (uda_scale, _UDA_SCALE),
        (width_of_arms, _WIDTH_OF_ARMS),
        (x_half_width, _X_HALF_WIDTH),
        (y_half_width, _Y_HALF_WIDTH),
    ]:
        if param is not None:
            if attr_name not in _APERTURETYPE_USED_SETTINGS[str(new_type)]:
                warn(
                    f"Aperture type {new_type!s} does not support the specification of {attr_name}. See the "
                    f"OpticStudio documentation for more information.",
                    UserWarning,
                )
            else:
                setattr(new_aperturetype_settings, attr_name, param)

    surface.ApertureData.ChangeApertureTypeSettings(new_aperturetype_settings)
