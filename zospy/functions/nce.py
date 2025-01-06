"""Utility functions for the Non-Sequential Component Editor (NCE) in OpticStudio."""

from __future__ import annotations

from zospy.api import _ZOSAPI, constants

__all__ = (
    "find_object_by_comment",
    "object_change_type",
)


def object_change_type(obj: _ZOSAPI.Editors.NCE.INCERow, new_type: constants.Editors.NCE.ObjectType | str):
    """Change the object type in the Non-Sequential Component Editor.

    Parameters
    ----------
    obj : ZOSAPI.Editors.NCE.INCERow
        The Row/Object for which the change is to be made.
    new_type : zospy.constants.Editors.NCE.ObjectType | str
        The new object type, either string (e.g. 'StandardLens') or int. The integer will be treated as if obtained from
        zp.constants.Editors.NCE.ObjectType.

    Returns
    -------
    None

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.connect()
    >>> oss.make_nonsequential()
    >>> new_object = oss.NCE.InsertNewObjectAt(1)
    >>> zp.functions.nce.object_change_type(
    ...     new_object, zp.constants.Editors.NCE.ObjectType.StandardLens
    ... )
    """
    new_type = constants.process_constant(constants.Editors.NCE.ObjectType, new_type)

    # Apply
    new_surface_type_settings = obj.GetObjectTypeSettings(new_type)
    obj.ChangeType(new_surface_type_settings)


def find_object_by_comment(
    nce: _ZOSAPI.Editors.NCE, comment: str, *, case_sensitive: bool = True
) -> list[_ZOSAPI.Editors.NCE.INCERow]:
    """Retrieve objects from the Non-Sequential Component Editor that have the supplied string as Comment.

    In case of multiple matches, the objects are returned in ascending order.

    Parameters
    ----------
    nce : ZOSAPI.Editors.NCE
        The Non-sequential Component Editor (NCE).
    comment : str
        String that is searched for in the Comment column of the NCE.
    case_sensitive : bool=False
        Flag that specifies whether the search is case-sensitive (default value) or not.

    Returns
    -------
    list[ZOSAPI.Editors.NCE.INCERow]
        A list of object in the NCE that have a Comment column value which matches the comment argument.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.connect()
    >>> oss.make_nonsequential()
    >>> nce_object_1 = oss.NCE.InsertNewObjectAt(1)
    >>> nce_object_1.Comment = "aa"
    >>> nce_object_2 = oss.NCE.InsertNewObjectAt(1)
    >>> nce_object_2.Comment = "bb"
    >>> nce_object_3 = oss.NCE.InsertNewObjectAt(1)
    >>> nce_object_3.Comment = "aA"
    >>> find_object_by_comment(oss.NCE, "aa")
    """
    # Number of objects in the NCE
    number_of_objects = nce.NumberOfObjects

    # Is the search case-sensitive?
    if not case_sensitive:
        # If the search is NOT case-sensitive put comment argument in all small letters
        comment = comment.lower()

    # Initialize list of objects with matching comment
    matching_objects = []

    # Loop over the objects in the NCE and check if their comment matches
    for object_index in range(1, number_of_objects + 1):
        # Retrieve current object
        current_object = nce.GetObjectAt(object_index)

        # Retrieve current object comment
        object_comment = current_object.Comment

        # Is the search case-sensitive?
        if not case_sensitive:
            # If the search is NOT case-sensitive put current object comment in all small letters
            object_comment = object_comment.lower()

        # If the comment matches, append the corresponding object to the return list
        if comment == object_comment:
            matching_objects.append(current_object)

    # Return list of objects with matching comment
    return matching_objects
