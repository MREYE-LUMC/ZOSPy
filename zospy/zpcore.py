"""Manage the connection with OpticStudio and interact with the optical system.

This module provides two classes:

- `ZOS` is used to connect to OpticStudio and manage the connection.
- `OpticStudioSystem` is used to interact with the optical system.

Examples
--------
Connect to OpticStudio and create a new optical system:

>>> import zospy as zp
>>> zos = zp.ZOS()
>>> oss = zos.connect()
>>> oss.make_sequential()
>>> oss.SystemName = "New System"
>>> oss.LDE.InsertNewSurfaceAt(1)
"""

from __future__ import annotations

import locale
import logging
import warnings
import weakref
from sys import version_info
from typing import TYPE_CHECKING, Literal
from weakref import WeakValueDictionary

from semver.version import Version

from zospy.api import _ZOSAPI, constants
from zospy.api.apisupport import load_zosapi, load_zosapi_nethelper
from zospy.utils.pyutils import abspath

if TYPE_CHECKING:
    from os import PathLike

__all__ = ("OpticStudioSystem", "ZOS")

logger = logging.getLogger(__name__)


class OpticStudioSystem:
    """Wrapper for OpticStudio System instances."""

    def __init__(self, zos_instance: ZOS, system_instance: _ZOSAPI.IOpticalSystem):
        """Initiate the OpticStudioSystem.

        Parameters
        ----------
        zos_instance : ZOS
            A ZOS instance
        system_instance : ZOSAPI.IOpticalSystem
            An optical system obtained from the ZOS instance.

        Raises
        ------
        TypeError
            If a weak reference to the ZOS instance is passed instead of the instance itself.
        """
        if isinstance(zos_instance, weakref.ProxyType):
            raise TypeError(
                "zos_instance must be a ZOS instance, but a weak reference is passed. Use "
                "ZOS.get_instance() to get the current ZOS instance."
            )

        # Use weak reference to make sure that the ZOS instance is not kept alive by the OpticStudioSystem instance
        self.ZOS: ZOS = weakref.proxy(zos_instance)

        self._System: _ZOSAPI.IOpticalSystem = system_instance
        self._OpenFile = None

    @property
    def SystemName(self) -> str:  # noqa: N802
        """Name of the current optical system."""
        return self._System.SystemName

    @SystemName.setter
    def SystemName(self, value: str):  # noqa: N802
        self._System.SystemName = value

    @property
    def SystemID(self) -> int:  # noqa: N802
        """Unique identifier for the optical system.

        This identifier can be used to differentiate between multiple `OpticStudioSystem` instances.

        Examples
        --------
        Create two different optical systems in a single instance of OpticStudio:

        >>> import zospy as zp
        >>> zos = zp.ZOS()
        >>> oss1 = zos.connect()
        >>> oss2 = zos.create_new_system()
        >>> oss1.SystemID != oss2.SystemID
        True
        """
        return self._System.SystemID

    @property
    def Mode(self) -> str:  # noqa: N802
        """Mode of the optical system. Either "Sequential" or "NonSequential"."""
        return str(self._System.Mode)

    @property
    def SystemFile(self) -> str:  # noqa: N802
        """File path to the current optical system."""
        return self._System.SystemFile

    @property
    def IsNonAxial(self) -> bool:  # noqa: N802
        """Indicates whether the optical system is axial and sequential.

        `True` if the system is non-axial, `False` otherwise.
        """
        return self._System.IsNonAxial

    @property
    def NeedsSave(self) -> bool:  # noqa: N802
        """Indicates if the optical system contains unsaved changes."""
        return self._System.NeedsSave

    @property
    def SystemData(self) -> _ZOSAPI.SystemData.ISystemData:  # noqa: N802
        """Data for configuring everything in the system explorer.

        Examples
        --------
        Change the aperture type to "FloatByStopSize":

        >>> oss.SystemData.Aperture.ApertureType = (
        ...     zp.constants.SystemData.ZemaxApertureType.FloatByStopSize
        ... )

        Add a wavelength of 543 nm with weight 1:

        >>> oss.SystemData.Wavelengths.AddWavelength(0.543, 1)
        """
        return self._System.SystemData

    @property
    def LDE(self) -> _ZOSAPI.Editors.LDE.ILensDataEditor:  # noqa: N802
        """Lens Data Editor."""
        return self._System.LDE

    @property
    def NCE(self) -> _ZOSAPI.Editors.NCE.INonSeqEditor:  # noqa: N802
        """Non-Sequential Component Editor."""
        return self._System.NCE

    @property
    def MFE(self) -> _ZOSAPI.Editors.MFE.IMeritFunctionEditor:  # noqa: N802
        """Merit Function Editor."""
        return self._System.MFE

    @property
    def TDE(self) -> _ZOSAPI.Editors.TDE.IToleranceDataEditor:  # noqa: N802
        """Tolerance Data Editor."""
        return self._System.TDE

    @property
    def MCE(self) -> _ZOSAPI.Editors.MCE.IMultiConfigEditor:  # noqa: N802
        """Multi-Configuration Editor."""
        return self._System.MCE

    @property
    def Analyses(self) -> _ZOSAPI.Analysis.I_Analyses:  # noqa: N802
        """Analyses for the current system."""
        return self._System.Analyses

    @property
    def Tools(self) -> _ZOSAPI.Tools.IOpticalSystemTools:  # noqa: N802
        """Interface to run various tools on the optical system."""
        return self._System.Tools

    @property
    def TheApplication(self) -> _ZOSAPI.IZOSAPI_Application:  # noqa: N802
        """Application in which the optical system is opened."""
        return self._System.TheApplication

    @property
    def LensUpdateMode(self) -> str:  # noqa: N802
        """Lens update mode of the optical system.

        Possible values are ['None', 'EditorsOnly', 'AllWindows'] or `zospy.constants.LensUpdateMode`.
        """
        return str(self._System.UpdateMode)

    @LensUpdateMode.setter
    def LensUpdateMode(self, value: constants.LensUpdateMode | str):  # noqa: N802
        self._System.UpdateMode = value

    @property
    def SessionModes(self) -> str:  # noqa: N802
        """Session mode of the optical system.

        Possible values are ['FromPreferences', 'SessionOn', 'SessionOff'], or `zospy.constants.SessionModes`.
        """
        return str(self._System.SessionMode)

    @SessionModes.setter
    def SessionModes(self, value: constants.SessionModes | str):  # noqa: N802
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

    def load(self, filepath: str | PathLike, *, saveifneeded: bool = False):
        """Load an earlier defined Zemax file.

        Parameters
        ----------
        filepath : str | PathLike
            Path to the file that should be loaded
        saveifneeded : bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        filepath = abspath(filepath)

        logger.debug(f"Opening {filepath} with SaveIfNeeded set to {saveifneeded}")

        self._System.LoadFile(filepath, saveifneeded)
        self._OpenFile = filepath

        logger.info(f"Opened {filepath}")

    def new(self, *, saveifneeded: bool = False):
        """Create a new session file.

        Parameters
        ----------
        saveifneeded : bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        logger.debug("Creating new file")

        self._System.New(saveifneeded)
        self._OpenFile = None

        logger.info("Opened new file")

    def save_as(self, filepath: str | PathLike):
        """Save the current session under a specified name.

        Parameters
        ----------
        filepath : str | PathLike
            The filepath where the system should be saved. Note that a partial path or relative path does not work.
        """
        filepath = abspath(filepath, check_directory_only=True)

        logger.debug(f"Saving open session as {filepath}")

        self._System.SaveAs(filepath)
        self._OpenFile = filepath

        logger.info(f"File saved as {filepath}")

    def save(self) -> bool:
        """Save the current OpticStudio session.

        If the file name for the current session is not known (e.g. when a new file was created), a warning is raised.
        On these occurences, save_as() should be used once.

        Returns (bool): A boolean indicating if the saving was successful.
        """
        logger.debug("Saving file")

        if self._OpenFile is None:
            warnings.warn(
                "The optical system has not been saved because no file name has been defined for the current system."
                "Please use the 'save_as' function before using 'save'."
            )
            logger.critical("Could not save file because the path has not been set using save_as")

        self._System.Save()
        logger.info("File saved")
        return True

    def close(self, *, saveifneeded: bool = False) -> bool:
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
        zospy.zpcore.OpticStudioSystem
            A ZOSPy OpticStudioSystem instance. Should be sequential.
        """
        return OpticStudioSystem(ZOS.get_instance(), self._System.CopySystem())

    def _ensure_correct_mode(self, required: str):
        """Ensure that the system is in the required type.

        Parameters
        ----------
        required : str
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
            err = f"Incorrect system type. System is in {self.Mode} mode but {required} mode is required"
            logger.critical(err)
            raise TypeError(err)
        logger.debug("System is in correct mode")
        # TODO: Eveluate what happens in 'mixed mode'

    def __del__(self):
        """Close the optical system when the instance is deleted."""
        logger.debug("Closing connections with Zemax OpticStudio")


class ZOS:
    """A Communication instance for Zemax OpticStudio.

    This class manages the connection between Python and Zemax OpticStudio through .NET, and controls OpticStudio
    instances. Only one instance of `ZOS` can exist at any time. If a second instance is attempted to be created, the
    existing instance is returned.

    Parameters
    ----------
    preload : bool
        A boolean indicating if nested namespaces should be preloaded upon initiating ZOS. Defaults to False.
    zosapi_nethelper : str | None
        Optional filepath to the ZOSAPI_NetHelper dll that is required to connect to OpticStudio. If None, the
        Windows registry will be used to find the ZOSAPI_NetHelper dll. Defaults to `None`.
    opticstudio_directory : str, optional
        Path to the directory containing the OpticStudio DLLs. If `None`, the directory will be acquired through the
        zosapi_nethelper. Note that either the zosapi_nethelper or the opticstudio_directory has to be specified,
        not both.

    Attributes
    ----------
    ZOSAPI : None | netModuleObject
        The ZOSAPI interface once loaded, else `None`.
    ZOSAPI_NetHelper : None | netModuleObject
        The ZOSAPI_NetHelper interface once loaded, else `None`.

    Examples
    --------
    Preferred methods:

    1. Connecting as extension:

        Make sure OpticStudio is running and the "Interactive Extension" mode in the programming tab is active.

        >>> import zospy as zp
        >>> zos = zp.ZOS()
        >>> oss = zos.connect(mode="extension")

    2. Launching OpticStudio in standalone mode:

        >>> import zospy as zp
        >>> zos = zp.ZOS()
        >>> oss = zos.connect(mode="standalone")
    """

    _instances: WeakValueDictionary = WeakValueDictionary()

    def __new__(cls, *args, **kwargs):  # noqa: ARG003
        """Ensure that only one instance of ZOS exists at any time.

        If a ZOS instance already exists, the existing instance is returned. If not, a new instance is created.
        """
        if cls not in cls._instances:
            instance = super().__new__(cls)
            instance.__initialized = False  # noqa: SLF001
            cls._instances[cls] = instance
        else:
            warnings.warn("Only a single instance of ZOS can exist at any time. Returning existing instance.")

        return cls._instances[cls]

    def __init__(
        self, *, preload: bool = False, zosapi_nethelper: str | None = None, opticstudio_directory: str | None = None
    ):
        """Initiate the OpticStudio API.

        The ZOS instance can subsequently be used to connect to OpticStudio. See the examples in the class docstring for
        more information.

        Parameters
        ----------
        preload : bool
            A boolean indicating if nested namespaces should be preloaded upon initiating ZOS. Defaults to False.
        zosapi_nethelper : str, optional
            Path to the ZOSAPI_NetHelper dll that is required to connect to OpticStudio. If `None`, the
            Windows registry will be used to find the ZOSAPI_NetHelper dll. Defaults to `None`.
        opticstudio_directory : str, optional
            Path to the directory containing the OpticStudio DLLs. If `None`, the directory will be acquired through the
            zosapi_nethelper. Note that either the zosapi_nethelper or the opticstudio_directory has to be specified,
            not both.
        """
        if self.__initialized:
            logger.debug("ZOS instance already initialized")
            return

        logger.debug("Initializing ZOS instance")

        self.ZOSAPI: _ZOSAPI = None
        self.ZOSAPI_NetHelper = None
        self.Connection: _ZOSAPI.IZOSAPI_Connection | None = None
        self.Application: _ZOSAPI.IZOSAPI_Application | None = None

        # Register the instance and create finalizers to tear down the ZOS instance when deleted
        weakref.finalize(self, self.disconnect)

        logger.info("ZOS instance initialized")

        self._wakeup(preload=preload, zosapi_nethelper=zosapi_nethelper, opticstudio_directory=opticstudio_directory)

        self.__initialized = True

    def _wakeup(
        self, *, preload: bool = False, zosapi_nethelper: str | None = None, opticstudio_directory: str | None = None
    ):
        """Wake the ZOSAPI instance.

        The parameters are passed to `ZOS._load_zos_dlls`.

        Parameters
        ----------
        preload : bool
            A boolean indicating if nested namespaces should be preloaded.
        zosapi_nethelper : str, optional
            File path to the ZOSAPI_NetHelper dll, if `None`, the Windows registry will be used to find
            ZOSAPI_NetHelper dll. Defaults to `None`.
        opticstudio_directory : str, optional
            Path to the directory containing the OpticStudio DLLs. If `None`, the directory will be acquired through the
            zosapi_nethelper. Note that either the zosapi_nethelper or the opticstudio_directory has to be specified,
            not both.
        """
        if self.Connection is None:
            self._load_zos_dlls(
                preload=preload, zosapi_nethelper=zosapi_nethelper, opticstudio_directory=opticstudio_directory
            )
            self._assign_connection()

    def _load_zos_dlls(
        self, *, preload: bool = False, zosapi_nethelper: str | None = None, opticstudio_directory: str | None = None
    ):
        """Load the ZOS-API DLLs and makes them available for usage through ZOS.ZOSAPI and ZOS.ZOSAPI_NetHelper.

        As there are many nested namespaces in the ZOSAPI DLLs that are always available after import but not
        preloaded, it can be chosen to do so. This should only be done for development reasons, as it likely slows
        down the code.

        If multiple versions of OpticStudio are installed on the same system, a specific version can be used by
        manually specifying the path to the OpticStudio installation directory with `opticstudio_directory`.

        Parameters
        ----------
        preload : bool
            A boolean indicating if nested namespaces should be preloaded.
        zosapi_nethelper : str, optional
            Path to the ZOSAPI_NetHelper dll, if `None`, the Windows registry will be used to find
            ZOSAPI_NetHelper dll. Defaults to `None`.
        opticstudio_directory : str, optional
            Path to the directory containing the OpticStudio DLLs. If `None`, the directory will be acquired through the
            zosapi_nethelper. Note that either the zosapi_nethelper or the opticstudio_directory has to be specified,
            not both.

        Raises
        ------
        FileNotFoundError
            An error occurred in locating one of the DLLs.
        ModuleNotFoundError
            One of the nested namespaces cannot be found. This error can only occur with preload set to True.
        ValueError
            Both `zosapi_nethelper` and `opticstudio_directory` are specified.
        """
        if zosapi_nethelper is not None and opticstudio_directory is not None:
            raise ValueError("Only one of `zosapi_nethelper` and `opticstudio_directory` may be specified.")

        logger.debug(f"Loading ZOS DLLs with preload set to {preload}")

        if opticstudio_directory is not None:
            self.ZOSAPI = load_zosapi(zemaxdirectory=opticstudio_directory, preload=preload)
        else:
            self.ZOSAPI_NetHelper = load_zosapi_nethelper(filepath=zosapi_nethelper, preload=preload)
            self.ZOSAPI = load_zosapi(zosapi_nethelper=self.ZOSAPI_NetHelper, preload=preload)

    def _assign_connection(self):
        """Assign the ZOSAPI Connection to self.Connection."""
        if not self.Connection:
            logger.debug("Assigning ZOSAPI_Connection() to self.Connection")
            self.Connection = self.ZOSAPI.ZOSAPI_Connection()
        else:
            logger.debug("ZOSAPI_Connection() already assigned self.Connection")

    def connect(
        self,
        mode: Literal["standalone", "extension"] = "standalone",
        instance_number: int | None = None,
        *,
        message_logging: bool = True,
    ) -> OpticStudioSystem:
        """Connect to Zemax OpticStudio.

        The application will be assigned to ZOS.Application.

        Parameters
        ----------
        mode : str
            Connection mode, either "standalone" or "extension". Default is "standalone".
            In standalone mode, ZOSPy initializes a new, invisible OpticStudio instance and connects to this instance.
            In extension mode, ZOSPy connects to an already open instance of OpticStudio in "Interactive Extension"
            mode.
        instance_number : int, optional
            An integer to specify the number of the instance used. Only applicable in extension mode.
        message_logging : bool, optional
            If `True`, OpticStudio's message logging will be enabled after establishing a connection.

        Returns
        -------
        OpticStudioSystem
            The primary optical system of the connected OpticStudio instance.
        """
        if mode != "extension" and instance_number is not None:
            warnings.warn("Instance number is only used in extension mode.")

        self._assign_connection()

        if self.Connection.IsAlive:  # TODO ensure no memory leak
            raise RuntimeError("Only one Zemax application can exist within runtime")

        if mode == "standalone":
            self.Application = self.Connection.CreateNewApplication()
        elif mode == "extension":
            self.Application = self.Connection.ConnectAsExtension(instance_number or 0)
        else:
            raise ValueError(f"Invalid connection mode {mode}")

        if not self.Application.IsValidLicenseForAPI:
            logger.critical("OpticStudio Licence is not valid for API, connection not established")
            raise ConnectionRefusedError("OpticStudio Licence is not valid for API, connection not established")

        if message_logging:
            self.Application.BeginMessageLogging()

        return self.get_primary_system()

    def disconnect(self):
        """Disconnect from the connected OpticStudio instance.

        When connected in standalone mode, this closes the standalone OpticStudio instance. When connected in extension
        mode, this closes the connection but keeps the OpticStudio instance open.
        """
        logger.debug("Disconnecting from OpticStudio")

        if self.Application is not None:
            self.Application.CloseApplication()
            self.Application = None

        logger.info("Disconnected from OpticStudio")

    def create_new_system(self, system_mode: constants.SystemType | str = "Sequential") -> OpticStudioSystem:
        """Create a new OpticStudioSystem.

        This works only if ZOSPy is connected to a standalone application.

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
            return OpticStudioSystem(zos_instance=self, system_instance=new_system)

        # TODO: Check if this is really true
        raise ValueError("Can only create a new system when using a standalone connection.")

    def get_primary_system(self) -> OpticStudioSystem:
        """Get the primary optical system.

        Returns
        -------
        OpticStudioSystem
            Primary optical system.
        """
        optic_studio_system = OpticStudioSystem(zos_instance=self, system_instance=self.Application.PrimarySystem)

        # Automatically populate _OpenFile when connecting in extension mode, to prevent unnecessary errors when
        # calling save
        if self.Application.Mode == constants.ZOSAPI_Mode.Plugin:
            optic_studio_system._OpenFile = optic_studio_system.SystemFile  # noqa: SLF001

        return optic_studio_system

    def get_system(self, pos: int = 0) -> OpticStudioSystem:
        """Get the optical system at the specified position.

        Parameters
        ----------
        pos : int
            Index of the optical system. If `0`, the primary system is returned.

        Returns
        -------
        OpticStudioSystem
            Optical system at position `pos`.
        """
        optic_studio_system = self.Application.GetSystemAt(pos)
        return OpticStudioSystem(zos_instance=self, system_instance=optic_studio_system)

    def get_txtfile_encoding(self) -> str:
        """Determine the encoding used to write text files in OpticStudio.

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
        if str(self.Application.Preferences.General.TXTFileEncoding) == "ANSI":
            if version_info < (3, 11):
                return locale.getpreferredencoding(False)

            # Python 3.11 introduced locale.getencoding, which returns the system preferred encoding also if Python's
            # UTF-8 mode is enabled
            return locale.getencoding()
        raise NotImplementedError(
            f"ZOSPy cannot handle encoding {self.Application.Preferences.General.TXTFileEncoding!s}"
        )

    def retrieve_logs(self) -> str:
        """Retrieve messages logged by OpticStudio.

        Returns
        -------
        str
            Messages logged by OpticStudio.
        """
        return self.Application.RetrieveLogMessages()

    @property
    def version(self) -> Version:
        """Returns the OpticStudio version as Version object."""
        return Version(
            major=self.Application.ZOSMajorVersion,
            minor=self.Application.ZOSMinorVersion,
            patch=self.Application.ZOSSPVersion,
        )

    @classmethod
    def get_instance(cls) -> ZOS | None:
        """Get the current instance of ZOS.

        Unlike `__new__`, this method does not create a new instance if none exists.

        Returns
        -------
        ZOS | None
            The current instance of ZOS, or `None` if no instance exists.
        """
        return cls._instances.get(cls)
