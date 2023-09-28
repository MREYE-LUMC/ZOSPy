from __future__ import annotations

import locale
import logging
import warnings
import weakref

from semver.version import Version

from zospy.api import _ZOSAPI, constants
from zospy.api.apisupport import load_zosapi, load_zosapi_nethelper

logger = logging.getLogger(__name__)


class OpticStudioSystem:
    """Wrapper for OpticStudio System instances."""

    def __init__(self, zos_instance, system_instance):
        """Initiate the OpticStudioSystem.

        Parameters
        ----------
        zos_instance: ZOS
            A ZOS instance
        system_instance: ZOS.Application.PrimarySystem
            A PrimarySystem instance obtained from the zos_instance.
        """
        self._ZOS: ZOS = zos_instance

        self._System: _ZOSAPI.IOpticalSystem = system_instance
        self._OpenFile = None

    @property
    def SystemName(self) -> str:
        """Name of the current optical system."""
        return self._System.SystemName

    @SystemName.setter
    def SystemName(self, value: str):
        self._System.SystemName = value

    @property
    def SystemID(self) -> int:
        """Unique identifier for the optical system.

        This identifier can be used to differentiate between multiple `OpticStudioSystem` instances.

        Examples
        --------
        Create two different optical systems in a single instance of OpticStudio:

        >>> import zospy as zp
        >>> zos = zp.ZOS()
        >>> oss1 = zos.connect_as_standalone(return_primary_system=True)
        >>> oss2 = zos.create_new_system()
        >>> oss1.SystemID != oss2.SystemID
        True
        """
        return self._System.SystemID

    @property
    def Mode(self) -> str:
        """Mode of the optical system. Either "Sequential" or "NonSequential"."""
        return str(self._System.Mode)

    @property
    def SystemFile(self) -> str:
        """File path to the current optical system."""
        return self._System.SystemFile

    @property
    def IsNonAxial(self) -> bool:
        """Indicates whether the optical system is axial and sequential.

        `True` if the system is non-axial, `False` otherwise.
        """
        return self._System.IsNonAxial

    @property
    def NeedsSave(self) -> bool:
        """Indicates if the optical system contains unsaved changes."""
        return self._System.NeedsSave

    @property
    def SystemData(self) -> _ZOSAPI.SystemData.ISystemData:
        """Data for configuring everything in the system explorer.

        Examples
        --------
        Change the aperture type to "FloatByStopSize":

        >>> oss.SystemData.Aperture.ApertureType = zp.constants.SystemData.ZemaxApertureType.FloatByStopSize

        Add a wavelength of 543 nm with weight 1:

        >>> oss.SystemData.Wavelengths.AddWavelength(0.543, 1)
        """
        return self._System.SystemData

    @property
    def LDE(self) -> _ZOSAPI.Editors.LDE.ILensDataEditor:
        """Lens Data Editor."""
        return self._System.LDE

    @property
    def NCE(self) -> _ZOSAPI.Editors.NCE.INonSeqEditor:
        """Non-Sequential Component Editor."""
        return self._System.NCE

    @property
    def MFE(self) -> _ZOSAPI.Editors.MFE.IMeritFunctionEditor:
        """Merit Function Editor."""
        return self._System.MFE

    @property
    def TDE(self) -> _ZOSAPI.Editors.TDE.IToleranceDataEditor:
        """Tolerance Data Editor."""
        return self._System.TDE

    @property
    def MCE(self) -> _ZOSAPI.Editors.MCE.IMultiConfigEditor:
        """Multi-Configuration Editor."""
        return self._System.MCE

    @property
    def Analyses(self) -> _ZOSAPI.Analysis.I_Analyses:
        """Analyses for the current system."""
        return self._System.Analyses

    @property
    def Tools(self) -> _ZOSAPI.Tools.IOpticalSystemTools:
        """Interface to run various tools on the optical system."""
        return self._System.Tools

    @property
    def TheApplication(self) -> _ZOSAPI.IZOSAPI_Application:
        """Application in which the optical system is opened."""
        return self._System.TheApplication

    @property
    def LensUpdateMode(self) -> str:
        """Lens update mode of the optical system.

        Possible values are ['None', 'EditorsOnly', 'AllWindows'] or `zospy.constants.LensUpdateMode`.
        """
        return str(self._System.UpdateMode)

    @LensUpdateMode.setter
    def LensUpdateMode(self, value: constants.LensUpdateMode | str):
        self._System.UpdateMode = value

    @property
    def SessionModes(self) -> str:
        """Session mode of the optical system.

        Possible values are ['FromPreferences', 'SessionOn', 'SessionOff'], or `zospy.constants.SessionModes`.
        """
        return str(self._System.SessionMode)

    @SessionModes.setter
    def SessionModes(self, value: constants.SessionModes | str):
        self._System.SessionMode = constants.process_constant(constants.SessionModes, value)

    def get_current_status(self) -> str:
        """Get the last status of the optical system. If null or the length is 0, then the system has no errors.

        Returns
        -------
        str
            Current status of the optical system.
        """
        return self._System.GetCurrentStatus()

    def update_status(self) -> str:
        """Force an update of the system, and returns the current status.

        Returns
        -------
        str
            Current status of the optical system.
        """
        return self._System.UpdateStatus()

    def make_sequential(self) -> bool:
        """Set the optical system to sequential mode if it is not already."""
        return self._System.MakeSequential()

    def make_nonsequential(self) -> bool:
        """Set the optical system to non-sequential mode if it is not already."""
        return self._System.MakeNonSequential()

    def load(self, filepath: str, saveifneeded: bool = False):
        """Load an earlier defined Zemax file.

        Parameters
        ----------
        filepath: str
            The filepath that should be loaded
        saveifneeded: bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        logger.debug("Opening {} with SaveIfNeeded set to {}".format(filepath, saveifneeded))

        self._System.LoadFile(filepath, saveifneeded)
        self._OpenFile = filepath

        logger.info("Opened {}".format(filepath))

    def new(self, saveifneeded: bool = False):
        """Create a new session file.

        Parameters
        ----------
        saveifneeded: bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        logger.debug("Creating new file")

        self._System.New(saveifneeded)
        self._OpenFile = None

        logger.info("Opened new file")

    def save_as(self, filepath: str):
        """Save the current session under a specified name.

        Parameters
        ----------
        filepath: str
            The filepath where the system should be saved. Note that a partial path or relative path does not work.
        """
        logger.debug("Saving open session as {}".format(filepath))

        self._System.SaveAs(filepath)
        self._OpenFile = filepath

        logger.info("File saved as {}".format(filepath))

    def save(self) -> bool:
        """Save the current OpticStudio session.

        If the file name for the current session is not known (e.g. when a new file was created), a warning is raised
        and the file is not saved. On these occurences, save_as() should be used once.

        Returns (bool): A boolean indicating if the saving was successful.

        """
        logger.debug("Saving file")

        if self._OpenFile is None:
            warnings.warn(
                "No file name has been defined for the current system, the current session has not been "
                "saved. Please use the save_as() function before using save."
            )
            logger.critical("Could not save file")

            return False
        else:
            self._System.Save()
            logger.info("File saved")
            return True

    def close(self, saveifneeded: bool = False) -> bool:
        """Close the optical system. Only works on secondary systems (See OpticStudio documentation).

        Parameters
        ----------
        saveifneeded : bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        return self._System.Close(saveifneeded)

    def copy_system(self) -> OpticStudioSystem:
        """Copy the current OpticStudioSystem instance.

        Returns
        -------
        zospy.core.OpticStudioSystem
            A ZOSPy OpticStudioSystem instance. Should be sequential.
        """
        return OpticStudioSystem(self._ZOS, self._System.CopySystem())

    def _ensure_correct_mode(self, required: str):
        """Ensure that the system is in the required type.

        Parameters
        ----------
        required: str
            The required system type. Either 'Sequential' or 'NonSequential'.

        Returns
        -------
        None

        Raises
        ------
        ValueError:
            When the system is in the incorrect type
        """
        logger.debug("Ensuring correct mode")
        if self.Mode != required:
            err = "Incorrect system type. System is in {} mode but {} mode is required".format(self.Mode, required)
            logger.critical(err)
            raise TypeError(err)
        else:
            logger.debug("System is in correct mode")
        # ToDo: Eveluate what happens in 'mixed mode'

    def __del__(self):
        logger.debug("Closing connections with Zemax OpticStudio")
        # ToDo Add cleanup


class ZOS:
    """A Communication instance for Zemax OpticStudio.

    This class can be used to establish a link between Python and Zemax OpticStudio through .NET,
    and subsequently control OpticStudio. Only one instance of `ZOS` can exist at any time.

    The connection is established in two ways, the preferred method as wel as a legacy method for backwards
    compatability. See examples.

    Parameters
    ----------
    preload : bool
        A boolean indicating if nested namespaces should be preloaded upon initiating ZOS. Defaults to False.
    zosapi_nethelper : str | None
        Optional filepath to the ZOSAPI_NetHelper dll that is required to connect to OpticStudio. If None, the
        Windows registry will be used to find the ZOSAPI_NetHelper dll. Defaults to None.

    Attributes
    ----------
    ZOSAPI : None | netModuleObject
        The ZOSAPI interface once loaded, else None.
    ZOSAPI_NetHelper : None | netModuleObject
        The ZOSAPI_NetHelper interface once loaded, else None.

    Raises
    ------
    ValueError
        When it is attempted to initiate a second instance of  `ZOS`. Only one instance can exist at any time.

    Examples
    --------
    Preferred methods:

    1. Connecting as extension:

    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.connect_as_extension(return_primary_system=True)

    2. Launching OpticStudio in standalone mode:

    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> oss = zos.create_new_application(return_primary_system=True)

    Legacy methods:

    1. Connecting as extension:

    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.wakeup()
    >>> zos.connect_as_extension()
    >>> oss = zos.get_primary_system()

    2. Launching OpticStudio in standalone mode:

    >>> import zospy as zp
    >>> zos = zp.ZOS()
    >>> zos.wakeup()
    >>> zos.create_new_application()
    >>> oss = zos.get_primary_system()
    """

    _OpticStudioSystem = OpticStudioSystem

    _instances = set()

    def __new__(cls, *args, **kwargs):
        if len(cls._instances) >= 1:
            # As the number of applications within runtime is limited to 1 by Zemax, it is logical to also limit the
            # number of ZOS instances
            raise ValueError(
                "Cannot have more than one active ZOS instance.\n\n"
                "Since OpticStudio limits the number of connections to the ZOS-API to 1, only a single ZOS instance "
                "is allowed. Re-use the existing instance, or delete the existing instance prior to initializing a "
                "new one. See https://zospy.rtfd.io/faq#single-zos-instance for more information."
            )

        instance = super(ZOS, cls).__new__(cls)

        return instance

    def __init__(self, preload: bool = False, zosapi_nethelper: str = None):
        """Initiation of the ZOS instance.

        The ZOS instance can subsequently be used to connect to OpticStudio. See the examples in the class docstring for
        more information.

        Parameters
        ----------
        preload : bool
            A boolean indicating if nested namespaces should be preloaded upon initiating ZOS. Defaults to False.
        zosapi_nethelper : str | None
            Optional filepath to the ZOSAPI_NetHelper dll that is required to connect to OpticStudio. If None, the
            Windows registry will be used to find the ZOSAPI_NetHelper dll. Defaults to None.
        """
        logger.debug("Initializing ZOS instance")

        self.ZOSAPI: _ZOSAPI = None
        self.ZOSAPI_NetHelper = None
        self.Connection: _ZOSAPI.IZOSAPI_Connection = None
        self.Application: _ZOSAPI.IZOSAPI_Application = None

        # Register the instance and create a finalize code to remove it from ZOS._instances when deleted
        ZOS._instances.add(id(self))
        weakref.finalize(self, ZOS._instances.discard, id(self))

        logger.info("ZOS instance initialized")

        self.wakeup(preload=preload, zosapi_nethelper=zosapi_nethelper)

    def wakeup(self, preload: bool = False, zosapi_nethelper: str = None):
        """Wake the zosapi instance.

        .. deprecated:: 1.1.0
                `wakeup` will be removed in ZOSPy 2.0.0, as it is automatically called by `__init__`.

        The parameters are passed to self._load_zos_dlls().

        Parameters
        ----------
        preload : bool
            A boolean indicating if nested namespaces should be preloaded.
        zosapi_nethelper : str, optional
            File path to the ZOSAPI_NetHelper dll, if None, the Windows registry will be used to find
            ZOSAPI_NetHelper dll. Defaults to None.

        Returns
        -------
        None
        """
        if self.Connection is None:
            self._load_zos_dlls(preload=preload, zosapi_nethelper=zosapi_nethelper)
            self._assign_connection()

    def _load_zos_dlls(self, preload: bool = False, zosapi_nethelper: str = None):
        """Load the ZOS-API DLLs and makes them available for usage through ZOS.ZOSAPI and ZOS.ZOSAPI_NetHelper.

        As there are many nested namespaces in the ZOSAPI DLLs that are always available after import but not
        preloaded, it can be chosen to do so. This should only be done for developmental reasons, as it likely slows
        down the code.

        Parameters
        ----------
        preload: bool
            A boolean indicating if nested namespaces should be preloaded.
        zosapi_nethelper: str, optional
            Optional filepath to the ZOSAPI_NetHelper dll, if None, the windows registry will be used to find
            ZOSAPI_NetHelper dll. Defaults to None.

        Raises
        ------
        FileNotFoundError:
            An error occurred in locating one of the DLLs.
        ModuleNotFoundError:
            One of the nested namespaces cannot be found. This error can only occur with preload set to True.
        """
        logger.debug("Loading ZOS DLLs with preload set to {}".format(preload))
        self.ZOSAPI_NetHelper = load_zosapi_nethelper(filepath=zosapi_nethelper, preload=preload)
        self.ZOSAPI = load_zosapi(self.ZOSAPI_NetHelper, preload=preload)

    def _assign_connection(self):
        """Assign the ZOSAPI Connection to self.Connection."""
        if not self.Connection:
            logger.debug("Assigning ZOSAPI_Connection() to self.Connection")
            self.Connection = self.ZOSAPI.ZOSAPI_Connection()
        else:
            logger.debug("ZOSAPI_Connection() already assigned self.Connection")

    def connect_as_extension(
        self, instancenumber: int = 0, return_primary_system: bool = False
    ) -> bool | OpticStudioSystem:
        """Connect to Zemax OpticStudio as extension.

        The application will be assigned to ZOS.Application.

        Parameters
        ----------
        instancenumber : int, optional
            An integer to specify the number of the instance used.
        return_primary_system: bool, optional
            A boolean indicating if the primary OpticStudioSystem should be returned. Defaults to `False`.

        Returns
        -------
        bool | OpticStudioSystem
            `True` if a valid connection is made, else `False`. If `return_primary_system` is `True`, the function
            returns the primary `OpticStudioSystem`.
        """
        self._assign_connection()

        if self.Connection.IsAlive:  # ToDo ensure no memory leak
            raise RuntimeError("Only one Zemax application can exist within runtime")

        self.Application = self.Connection.ConnectAsExtension(instancenumber)

        if not self.Application.IsValidLicenseForAPI:
            logger.critical("OpticStudio Licence is not valid for API, connection not established")

            if return_primary_system:
                raise ConnectionRefusedError("OpticStudio Licence is not valid for API, connection not established")

            return False

        if return_primary_system:
            return self.get_primary_system()

        return True

    def create_new_application(self, return_primary_system: bool = False) -> bool | OpticStudioSystem:
        """Create a standalone Zemax OpticStudio instance.

        The application will be assigned to ZOS.Application.

        Parameters
        ----------
        return_primary_system : bool, optional
            A boolean indicating if the primary OpticStudioSystem should be returned. Defaults to `False`.

        Returns
        -------
        bool | OpticStudioSystem
            `True` if a valid connection is made, else `False`. If `return_primary_system` is `True`, the function
            returns the primary `OpticStudioSystem`.
        """
        self._assign_connection()

        if self.Connection.IsAlive:  # ToDo ensure no memory leak
            raise RuntimeError("Only one Zemax application can exist within runtime")

        self.Application = self.Connection.CreateNewApplication()

        if not self.Application.IsValidLicenseForAPI:
            logger.critical("OpticStudio Licence is not valid for API, connection not established")

            if return_primary_system:
                raise ConnectionRefusedError("OpticStudio Licence is not valid for API, connection not established")

            return False

        if return_primary_system:
            return self.get_primary_system()

        return True

    def connect_as_standalone(self, return_primary_system: bool = False) -> bool | OpticStudioSystem:
        """Creates a standalone Zemax OpticStudio instance.

        Equal to `ZOS.create_new_application`.

        Parameters
        ----------
        return_primary_system : bool, optional
            A boolean indicating if the primary OpticStudioSystem should be returned. Defaults to `False`.

        Returns
        -------
        bool | OpticStudioSystem
            `True` if a valid connection is made, else `False`. If `return_primary_system` is `True`, the function
            returns the primary `OpticStudioSystem`.
            runs ZOS.get_primary_system() and directly returns OpticStudioSystem.
        """
        return self.create_new_application(return_primary_system=return_primary_system)

    def create_new_system(self, system_mode: constants.SystemType | str = "Sequential") -> OpticStudioSystem:
        """Creates a new OpticStudioSystem. This works only if ZOSPy is connected to a standalone application.

        Parameters
        ----------
        system_mode : constants.SystemType | str
            The mode of the new system, must be one of "Sequential", "NonSequential". Defaults to "Sequential".

        Returns
        -------
        OpticStudioSystem
            The new OpticStudioSystem.
        """
        if self.Application.Mode == constants.ZOSAPI_Mode.Server:
            new_system = self.Application.CreateNewSystem(constants.process_constant(constants.SystemType, system_mode))
            return self._OpticStudioSystem(zos_instance=self, system_instance=new_system)

        raise ValueError("Can only create a new system when using a standalone connection.")

    def get_primary_system(self) -> OpticStudioSystem:
        """
        Get the primary optical system.

        Returns
        -------
        OpticStudioSystem
            Primary optical system.
        """
        opticstudiosystem = self.Application.PrimarySystem
        return self._OpticStudioSystem(zos_instance=self, system_instance=opticstudiosystem)

    def get_system(self, pos: int = 0) -> OpticStudioSystem:
        """
        Get the optical system at the specified position.

        Parameters
        ----------
        pos : int
            Index of the optical system. If `0`, the primary system is returned.

        Returns
        -------
        OpticStudioSystem
            Optical system at position `pos`.
        """
        opticstudiosystem = self.Application.GetSystemAt(pos)
        return self._OpticStudioSystem(zos_instance=self, system_instance=opticstudiosystem)

    def get_txtfile_encoding(self) -> str:
        """Determines the encoding used to write textfiles in OpticStudio.

        Returns
        -------
        str
            The encoding used for textfiles by OpticStudio

        Raises
        ------
        RuntimeError
            When ZOS does not have a connection to the OpticStudio application
        NotImplementedError
            When the ZOS.Application.Preferences.General.TXTFileEncoding is not one of ["Unicode", "ANSI"]
        """
        if self.Application is None:
            raise RuntimeError("ZOS.get_txtfile_encoding requires a live connection to the OpticStudio application.")

        if str(self.Application.Preferences.General.TXTFileEncoding) == "Unicode":
            return "UTF-16-le"
        elif str(self.Application.Preferences.General.TXTFileEncoding) == "ANSI":
            return locale.getpreferredencoding(do_setlocale=False)
        else:
            raise NotImplementedError(
                f"ZOSPy cannot handle encoding {str(self.Application.Preferences.General.TXTFileEncoding)}"
            )

    @property
    def version(self) -> Version:
        """Returns the OpticStudio version as Version object."""
        return Version(
            major=self.Application.ZOSMajorVersion,
            minor=self.Application.ZOSMinorVersion,
            patch=self.Application.ZOSSPVersion,
        )
