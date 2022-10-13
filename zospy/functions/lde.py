import pandas as pd

from zospy.api import constants
from zospy.utils.clrutils import DUMMY_DOUBLE, DUMMY_ENUM
from zospy.utils.zputils import proc_constant


def get_pupil(oss):
    """Obtains the pupil data.

    Parameters
    ----------
    oss: zospy.core.OpticStudioSystem
        A ZOSPy OpticStudioSystem instance.

    Returns
    -------
    pd.Series
        The pupildata.

    Examples
    --------
    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()
    >>> zp.functions.lde.get_pupil(oss)
    """
    pupdat = oss.LDE.GetPupil(int(), *[float()]*5, int(), float())

    ret = pd.Series(
        index=['ApertureType', 'ApertureValue', 'EntrancePupilDiameter', 'EntrancePupilPosition', 'ExitPupilDiameter',
               'ExitPupilPosition', 'ApodizationType', 'ApodizationFactor'],
        data=pupdat[1:]
        )

    return ret


def surface_change_type(surf, newtype):
    """Simple function to change the type of a surface in the LDE.

    Parameters
    ----------
    surf: ILDERow
        The Row/Surface for which the change is to be made.
    newtype: str or int
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
    >>> surface_change_type(newsurf, 'Standard')
    """
    # Obtain the integer representing the new type if needed
    newtype = proc_constant(constants.Editors.LDE.SurfaceType, newtype)

    # Apply
    newsurftypesettings = surf.GetSurfaceTypeSettings(newtype)
    surf.ChangeType(newsurftypesettings)

