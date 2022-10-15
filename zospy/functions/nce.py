from zospy.api import constants
from zospy.utils.zputils import proc_constant


def object_change_type(obj, newtype):
    """Simple function to change the type of an object in the NCE

    Parameters
    ----------
    obj: INCERow
        The Row/Object for which the change is to be made.
    newtype: str or int
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
    >>> object_change_type(newobj, 'StandardLens')
    """
    # Obtain the integer representing the new type if needed
    newtype = proc_constant(constants.Editors.NCE.ObjectType, newtype)

    # Apply
    newsurftypesettings = obj.GetObjectTypeSettings(newtype)
    obj.ChangeType(newsurftypesettings)

