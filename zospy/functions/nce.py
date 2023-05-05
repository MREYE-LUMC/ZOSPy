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
