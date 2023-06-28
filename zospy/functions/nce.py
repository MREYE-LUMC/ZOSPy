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
    >>> newobj = oss.NCE.InsertNewObjectAt(0)
    >>> object_change_type(newobj, zp.constants.Editors.NCE.ObjectType.StandardLens)
    """
    new_type = constants.process_constant(constants.Editors.NCE.ObjectType, new_type)

    # Apply
    new_surface_type_settings = obj.GetObjectTypeSettings(new_type)
    obj.ChangeType(new_surface_type_settings)

def find_object_comment(nce: _ZOSAPI.Editors.NCE, comment: str, case_sensitive: bool=False) -> list[int] | int:
    """Function equivalent to ZPL numeric function OBJC($A).

    Parameters
    ----------
    nce: ZOSAPI.Editors.NCE
        The Non-sequential Component Editor (NCE).
    comment: str
        String that is searched for in the Comment column of the NCE.
    case_sensitive: bool=False
        Flag that specifies whether the search is case-sensitive or not.


    Returns
    ----------
    A list of integer indices corresponding to the rows of the NCE
    that had a matching comment, or -1 if no correspondance was
    found.

    Examples
    ----------
    >>> To be added
    """
    
    # Number of objects in the NCE
    number_of_objects = nce.NumberOfObjects

    # Is the search case-sensitive?
    if not case_sensitive:
        # If the search is NOT case-sensitive put 
        # comment argument in all small letters
        comment = comment.lower()

    # Initialize list of return indexes corresponding
    # to NCE rows with matched Comment column
    return_indices = []

    # Loop over the objects and check the comments
    for object_index in range(1, number_of_objects+1):
        # Retrieve current object comment
        object_comment = nce.GetObjectAt(object_index).Comment

        # Is the search case-sensitive?
        if not case_sensitive:
            # If the search is NOT case-sensitive put 
            # current object comment in all small letters
            object_comment = object_comment.lower()           

        # If the comment matches, store the corresponding object index
        if comment == object_comment:
            return_indices.append(object_index)

    # If no match are found set the return list to -1
    if not return_indices:
        return_indices = -1

    # Return list of matched inices
    return return_indices
