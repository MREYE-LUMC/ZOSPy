from __future__ import annotations

from zospy.api import _ZOSAPI, constants


def object_change_type(obj: _ZOSAPI.Editors.NCE.INCERow, new_type: constants.Editors.NCE.ObjectType | str):
    """Simple function to change the object type in the NCE.

    Parameters
    ----------
    obj: ZOSAPI.Editors.NCE.INCERow
        The Row/Object for which the change is to be made.
    new_type: zospy.constants.Editors.NCE.ObjectType | str
        The new object type, either string (e.g. 'StandardLens') or int. The integer will be treated as if obtained from
        zp.constants.Editors.NCE.ObjectType.

    Returns
    -------
    None

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> oss.make_nonsequential()
    >>> newobj = oss.NCE.InsertNewObjectAt(1)
    >>> zp.functions.nce.object_change_type(newobj, zp.constants.Editors.NCE.ObjectType.StandardLens)
    """
    new_type = constants.process_constant(constants.Editors.NCE.ObjectType, new_type)

    # Apply
    new_surface_type_settings = obj.GetObjectTypeSettings(new_type)
    obj.ChangeType(new_surface_type_settings)


def find_object_by_comment(
    nce: _ZOSAPI.Editors.NCE, comment: str, case_sensitive: bool = True
) -> list[_ZOSAPI.Editors.NCE.INCERow]:
    """Returns a list of objects from the NCE that have the supplied string as Comment.

    In case of multiple matches, the objects are returned in ascending order.

    Parameters
    ----------
    nce: ZOSAPI.Editors.NCE
        The Non-sequential Component Editor (NCE).
    comment: str
        String that is searched for in the Comment column of the NCE.
    case_sensitive: bool=False
        Flag that specifies whether the search is case-sensitive (default value) or not.

    Returns
    -------
    list[ZOSAPI.Editors.NCE.INCERow]
        A list of object in the NCE that have a Comment column value which matches the comment argument.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> oss.make_nonsequential()
    >>> newobj1 = oss.NCE.InsertNewObjectAt(1)
    >>> newobj1.Comment = 'aa'
    >>> newobj2 = oss.NCE.InsertNewObjectAt(1)
    >>> newobj2.Comment = 'bb'
    >>> newobj3 = oss.NCE.InsertNewObjectAt(1)
    >>> newobj3.Comment = 'aA'
    >>> find_object_by_comment(oss.NCE, 'aa')
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


def get_object_data(obj: _ZOSAPI.Editors.NCE.INCERow) -> _ZOSAPI.Editors.NCE.IObject:
    """Returns the object-specific data.

    Parameters
    ----------
    obj: ZOSAPI.Editors.NCE.INCERow
        The Row/Object for which the data is requested.

    Returns
    -------
    ZOSAPI.Editors.NCE.IObject
        The object-specific data with the inherited implementation.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> oss.make_nonsequential()
    >>> detector_object = oss.NCE.GetObjectAt(1)
    >>> detector_type = detector_object.GetObjectTypeSettings(zp.constants.Editors.NCE.ObjectType.DetectorRectangle)
    >>> detector_object.ChangeType(detector_type)
    >>> detector_data = zp.functions.nce.get_object_data(detector_object)
    >>> number_of_x_pixels = detector_data.NumberXPixels
    """
    return obj.ObjectData.__implementation__
