from __future__ import annotations

import logging
import warnings
import weakref

from zospy.api import _ZOSAPI, constants
from zospy.api.apisupport import load_zosapi, load_zosapi_nethelper

logger = logging.getLogger(__name__)


class OpticStudioSystem:
    """Wrapper for OpticStudio System instances."""

    def __init__(self, zos_instance, system_instance):
        """Initiates the OpticStudioSystem.

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
        return self._System.SystemName

    @SystemName.setter
    def SystemName(self, value: str):
        self._System.SystemName = value

    @property
    def SystemID(self) -> int:
        return self._System.SystemID

    @property
    def Mode(self) -> str:
        return str(self._System.Mode)

    @property
    def SystemFile(self) -> str:
        return self._System.SystemFile

    @property
    def IsNonAxial(self) -> bool:
        return self._System.IsNonAxial

    @property
    def NeedsSave(self) -> bool:
        return self._System.NeedsSave

    @property
    def SystemData(self) -> _ZOSAPI.SystemData.ISystemData:
        return self._System.SystemData

    @property
    def LDE(self) -> _ZOSAPI.Editors.LDE.ILensDataEditor:
        return self._System.LDE

    @property
    def NCE(self) -> _ZOSAPI.Editors.NCE.INonSeqEditor:
        return self._System.NCE

    @property
    def MFE(self) -> _ZOSAPI.Editors.MFE.IMeritFunctionEditor:
        return self._System.MFE

    @property
    def TDE(self) -> _ZOSAPI.Editors.TDE.IToleranceDataEditor:
        return self._System.TDE

    @property
    def MCE(self) -> _ZOSAPI.Editors.MCE.IMultiConfigEditor:
        return self._System.MCE

    @property
    def Analyses(self) -> _ZOSAPI.Analysis.I_Analyses:
        return self._System.Analyses

    @property
    def Tools(self) -> _ZOSAPI.Tools.IOpticalSystemTools:
        return self._System.Tools

    @property
    def TheApplication(self) -> _ZOSAPI.IZOSAPI_Application:
        return self._System.TheApplication

    @property
    def LensUpdateMode(self) -> str:
        return str(self._System.UpdateMode)

    @LensUpdateMode.setter
    def LensUpdateMode(self, value: _ZOSAPI.LensUpdateMode):
        """Sets the LensUpdateMode.

        Parameters
        ----------
        value: str or int
            The new mode. Should be one of ['None', 'EditorsOnly', 'AllWindows'] or int. The integer is interpreted as
            one of the zospy.constants.LensUpdateMode constants.
        """
        self._System.LensUpdateMode = value

    @property
    def SessionModes(self) -> str:
        return str(self._System.SessionMode)

    @SessionModes.setter
    def SessionModes(self, value: constants.SessionModes | str):
        """Sets the SessionMode.

        Parameters
        ----------
        value: str or int
            The new mode. Should be one of ['FromPreferences', 'SessionOn', 'SessionOff'].
        """
        self._System.SessionMode = constants.process_constant(constants.SessionModes, value)

    def get_current_status(self) -> str:
        return self._System.GetCurrentStatus()

    def update_status(self) -> str:
        return self._System.UpdateStatus()

    def make_sequential(self) -> bool:
        return self._System.MakeSequential()

    def make_nonsequential(self) -> bool:
        return self._System.MakeNonSequential()

    def load(self, filepath: str, saveifneeded: bool = False):
        """Loads an earlier defined zemax file.

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
        """Creates a new session file.

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
        """Saves the current session under a specified name.

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
        """Saves the current optic studio session.

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
        """Closes the optical system. Only works on secondary systems (See OpticStudio documentation).

        Parameters
        ----------
        saveifneeded: bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        return self._System.Close(saveifneeded)

    def copy_system(self) -> OpticStudioSystem:
        """Copies the current OpticStudioSystem instance.

        Returns
        -------
        zospy.core.OpticStudioSystem
            A ZOSPy OpticStudioSystem instance. Should be sequential.
        """
        return OpticStudioSystem(self._ZOS, self._System.CopySystem())

    def _ensure_correct_mode(self, required: str):
        """Ensures that the system is in the required type.

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
    and control OpticStudio. The connection is established as following:

    Simple:
    1. self.wakeup().
    2. self.create_new_session() or self.connect_as_extension().
    3. self.get_primary_system()

    Advanced:
    1. self._load_zos_dlls()
    2. self._update_constants()
    3. self.create_new_session() or self.connect_as_extension().
    4. self.get_primary_system()

    After connection, many OpticStudio functionalities are controllable through ZOS.ZOSAPI()

    Attributes
    ----------
        ZOSAPI (None | netModuleObject): The ZOSAPI interface or if loaded.
        ZOSAPI_NetHelper (None | netModuleObject): The ZOSAPI_NetHelper interface if loaded.
    """

    _OpticStudioSystem = OpticStudioSystem

    _instances = set()

    def __new__(cls, *args, **kwargs):
        if len(cls._instances) >= 1:
            # As the number of applications within runtime is limited to 1 by Zemax, it is logical to also limit the
            # number of ZOS instances
            raise ValueError("Cannot have more than one active ZOS instance")

        instance = super(ZOS, cls).__new__(cls, *args, **kwargs)

        return instance

    def __init__(self):
        """Initiation of the ZOS Instance."""
        logger.debug("Initializing ZOS instance")

        self.ZOSAPI: _ZOSAPI = None
        self.ZOSAPI_NetHelper = None
        self.Connection: _ZOSAPI.IZOSAPI_Connection = None
        self.Application: _ZOSAPI.IZOSAPI_Application = None

        # Register the instance and create a finalize code to remove it from ZOS._instances when deleted
        ZOS._instances.add(id(self))
        weakref.finalize(self, ZOS._instances.discard, id(self))

        logger.info("ZOS instance initialized")

    def wakeup(self, preload: bool = False, zosapi_nethelper: str = None):
        """Wakes the zosapi instance.

        The parameters are passed to self._load_zos_dlls()

        Parameters
        ----------
        preload: bool
            A boolean indicating if nested namespaces should be preloaded.
        zosapi_nethelper: str, optional
            Optional filepath to the ZOSAPI_NetHelper dll, if None, the windows registry will be used to find
            ZOSAPI_NetHelper dll. Defaults to None.

        Returns
        -------
        None
        """
        self._load_zos_dlls(preload=preload, zosapi_nethelper=zosapi_nethelper)
        self._assign_connection()

    def _load_zos_dlls(self, preload: bool = False, zosapi_nethelper: str = None):
        """Loads the ZOS-API DLLs and makes them available for usage through ZOS.ZOSAPI and ZOS.ZOSAPI_NetHelper.

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
        """Assigns the ZOSAPI Connection to self.Connection."""
        if not self.Connection:
            logger.debug("Assigning ZOSAPI_Connection() to self.Connection")
            self.Connection = self.ZOSAPI.ZOSAPI_Connection()
        else:
            logger.debug("ZOSAPI_Connection() already assigned self.Connection")

    def connect_as_extension(self, instancenumber: int = 0) -> bool:
        """Creates a standalone Zemax Opticstudio instance.

        The application will be assigned to self.Application.

        Returns
        -------
        bool
            True if a valid connection is made, else False
        """
        self._assign_connection()

        if self.Connection.IsAlive:  # ToDo ensure no memory leak
            raise RuntimeError("Only one Zemax application can exist within runtime")

        self.Application = self.Connection.ConnectAsExtension(instancenumber)

        if self.Application.IsValidLicenseForAPI:
            return True
        else:
            logger.critical("OpticStudio Licence is not valid for API, connection not established")
            return False

    def create_new_application(self) -> bool:
        """Creates a standalone Zemax Opticstudio instance.

        The application will be assigned to self.Application.

        Returns
        -------
        bool
            True if a valid connection is made, else False
        """
        self._assign_connection()

        if self.Connection.IsAlive:  # ToDo ensure no memory leak
            raise RuntimeError("Only one Zemax application can exist within runtime")

        self.Application = self.Connection.CreateNewApplication()

        if self.Application.IsValidLicenseForAPI:
            return True
        else:
            logger.critical("OpticStudio Licence is not valid for API, connection not established")
            return False

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
        opticstudiosystem = self.Application.PrimarySystem
        return self._OpticStudioSystem(zos_instance=self, system_instance=opticstudiosystem)

    def get_system(self, pos: int = 0) -> OpticStudioSystem:
        warnings.warn("ZOS.get_system() has not been tested yet")
        # ToDo test
        opticstudiosystem = self.Application.PrimarySystem.GetSystemAt(pos)
        return self._OpticStudioSystem(zos_instance=self, system_instance=opticstudiosystem)

    def licence_check(self):
        pass
