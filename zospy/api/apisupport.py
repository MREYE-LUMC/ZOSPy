import logging
import os
import sys
import winreg

import clr  # noqa

import zospy.api.constants
from zospy.utils import clrutils

logger = logging.getLogger(__name__)


def get_zos_root():
    """Obtains the Zemax OpticStudio folder from the windows registry.

    Returns
    -------
    filepath: str
        The root folder of the installed Zemax Version

    Raises
    ------
    FileNotFoundError
        If either Zemax OpticStudio cannot be found in the Windows Registry or the Zemax OpticStudio root folder could
        not be obtained from the registry.
    """
    logger.info("Obtaining Zemax Location from Windows Registry")

    # Search for Zemax OpticStudio in the Windows Registry
    try:
        regkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Zemax")
    except FileNotFoundError as e:
        logger.exception("Zemax cannot be found in the registry, " "the following error is raised:\n{}".format(e))
        raise e

    # Obtain the Zemax OpticStudio root path from the registry
    try:
        zemaxfolder, _ = winreg.QueryValueEx(regkey, "ZemaxRoot")
        logger.info("Found ZemaxFolder at {}".format(zemaxfolder))
    except FileNotFoundError as e:
        logger.exception(
            "The Zemax Root folder cannot be found in the registry key, " "the following error is raised:\n{}".format(e)
        )
        raise e
    finally:  # Clean up
        logger.debug("Closing registry key")
        winreg.CloseKey(regkey)
        logger.debug("Registry key closed")

    return zemaxfolder


def load_zosapi_nethelper(filepath=None, preload=False):
    """Loads the ZOSAPI_NetHelper.

    Parameters
    ----------
    filepath: str, optional
        The location of the ZOSAPI_NetHelper. If not supplied, the location will be deducted from the windows registry.
    preload: bool
        Specifies if CLR should import with preload on (True) or off (False). Defaults to False).

    Returns
    -------
    ZOSAPI_NetHelper: netModuleObject
        The ZOSAPI_NetHelper as module object
    """
    if not filepath:  # get the path through the windows registry
        zos_root = get_zos_root()
        znh_filepath = os.path.join(zos_root, r"ZOS-API\Libraries\ZOSAPI_NetHelper.dll")
    else:
        znh_filepath = filepath

    logger.debug("Adding reference {} to clr".format(znh_filepath))
    sys.path.append(os.path.basename(znh_filepath))
    clr.AddReference(znh_filepath)

    logger.debug("Importing ZOSAPI_NetHelper")
    znh = __import__("ZOSAPI_NetHelper", globals(), locals(), [], 0)
    logger.info("ZOSAPI_NetHelper imported successfully")

    return znh


def load_zosapi(zosapi_nethelper=None, zemaxdirectory=None, preload=False):
    """Load the ZOS-API using the ZOSAPI NetHelper DLL.

    Parameters
    ----------
    zosapi_nethelper: netModuleObject, optional
        The loaded ZOSAPI_NetHelper DLL. If None, the zemaxdirectory parameter will be used. Note that either the
        zosapi_nethelper or the zemaxdirectory has to be specified, not both.
    zemaxdirectory: str, optional
        The directory containing the Zemax DLLs. If None, the directory will be acquired through the zosapi_nethelper.
        Note that either the zosapi_nethelper or the zemaxdirectory has to be specified, not both.
    preload: bool
        Specifies if CLR should import with preload on (True) or off (False). Defaults to False).

    Returns
    -------
    zosapi: netModuleObject
        The ZOSAPI module.

    Raises
    ------
    ValueError:
        If either both or None of zosapi_nethelper and zemaxdirectory are specified.
    FileNotFoundError:
        If one of ZOSAPI_Interfaces.dll or ZOSAPI.dll cannot be found.
    """
    if not any((zosapi_nethelper, zemaxdirectory)):
        raise ValueError("Either the zosapi_nethelper or the zemaxdirectory should be specified.")
    elif all((zosapi_nethelper, zemaxdirectory)):
        raise ValueError("Only one of zosapi_nethelper and zemaxdirectory should be specified.")
    else:
        pass

    # Get the Zemax OpticStudio directory and add it to the path
    if zosapi_nethelper:
        logger.info("Obtaining Zemax Directory from ZOSAPI_NetHelper")
        zosapi_nethelper.ZOSAPI_Initializer.Initialize()
        zos_dir = zosapi_nethelper.ZOSAPI_Initializer.GetZemaxDirectory()
        logger.info("Zemax OpticStudio found at {}".format(zos_dir))
    else:
        logger.info("Zemax Directory specified by user ({})".format(zemaxdirectory))
        zos_dir = zemaxdirectory
    sys.path.append(zos_dir)

    logger.info("Searching and registering ZOSAPI DLLs")
    for dll in ["ZOSAPI_Interfaces", "ZOSAPI"]:
        if clr.FindAssembly(dll):
            logger.debug("{}.dll found".format(dll))
            clr.AddReference(dll)
            logger.info("{} imported to clr".format(dll))
        else:
            logger.critical("Cannot locate {}.dll".format(dll))
            raise FileNotFoundError("Cannot locate {}.dll in {}".format(dll, zos_dir))

    logger.debug("Checking content of ZOSAPI_Interfaces.dll")
    content = clrutils.reflect_dll_content(os.path.join(zos_dir, "ZOSAPI_Interfaces.dll"))

    logger.debug("Loading ZOSAPI")
    zosapi = __import__("ZOSAPI", globals(), locals(), [], 0)
    logger.debug("ZOSAPI loaded")

    logger.debug("Loading nested namespaces")
    for nsp in content["namespaces"]:
        if nsp == "ZOSAPI":
            continue
        __import__(nsp, globals(), locals(), [], 0)
        logger.debug("Nested namespace {} preloaded".format(nsp))

    zospy.api.constants._construct_from_zosapi_and_enumkeys(zosapi, content["enums"])  # noqa

    return zosapi
