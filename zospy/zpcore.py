import logging
import warnings
import weakref

from zospy.analyses import mtf, reports, wavefront, psf
from zospy.api import constants
from zospy.api.apisupport import load_zosapi_nethelper, load_zosapi
from zospy.functions.lde import get_pupil
from zospy.utils.zputils import proc_constant

logger = logging.getLogger(__name__)


class OpticStudioSystem:
    """Wrapper for OpticStudio System instances"""
    def __init__(self, zos_instance, system_instance):
        """Initiates the OpticStudioSystem.

        Parameters
        ----------
        zos_instance: ZOS
            A ZOS instance
        system_instance: ZOS.Application.PrimarySystem
            A PrimarySystem instance obtained from the zos_instance.
        """
        self._ZOS = zos_instance

        self._System = system_instance
        self._OpenFile = None

    @property
    def SystemName(self): # noqa
        return self._System.SystemName

    @SystemName.setter
    def SystemName(self, value): # noqa
        self._System.SystemName = value

    @property
    def SystemID(self): # noqa
        return self._System.SystemID

    @property
    def Mode(self): # noqa
        return constants.get_constantname_by_value(constants.SystemType, self._System.Mode)

    @property
    def SystemFile(self): # noqa
        return self._System.SystemFile

    @property
    def IsNonAxial(self): # noqa
        return self._System.IsNonAxial

    @property
    def NeedsSave(self): # noqa
        return self._System.NeedsSave

    @property
    def SystemData(self): # noqa
        return self._System.SystemData

    @property
    def LDE(self):  # noqa
        return self._System.LDE

    @property
    def NCE(self):  # noqa
        return self._System.NCE

    @property
    def MFE(self):  # noqa
        return self._System.MFE

    @property
    def TDE(self):  # noqa
        return self._System.TDE

    @property
    def MCE(self):  # noqa
        return self._System.MCE

    @property
    def Analyses(self): # noqa
        return self._System.Analyses

    @property
    def Tools(self): # noqa
        return self._System.Tools

    @property
    def TheApplication(self): # noqa
        return self._System.TheApplication

    @property
    def LensUpdateMode(self): # noqa
        return constants.get_constantname_by_value(constants.LensUpdateMode, self._System.LensUpdateMode)

    @LensUpdateMode.setter
    def LensUpdateMode(self, value): # noqa
        """Sets the LensUpdateMode.

        Parameters
        ----------
        value: str or int
            The new mode. Should be one of ['None', 'EditorsOnly', 'AllWindows'] or int. The integer is interpreted as
            one of the zospy.constants.LensUpdateMode constants.
        """
        self._System.LensUpdateMode = proc_constant(constants.LensUpdateMode, value)

    @property
    def SessionModes(self): # noqa

        return constants.get_constantname_by_value(constants.SessionModes, self._System.SessionModes)

    @SessionModes.setter
    def SessionModes(self, value): # noqa
        """Sets the SessionMode.

        Parameters
        ----------
        value: str or int
            The new mode. Should be one of ['FromPreferences', 'SessionOn', 'SessionOff'] or int. The integer is
            interpreted as one of the zospy.constants.LensUpdateMode constants.
        """
        self._System.SessionModes = proc_constant(constants.SessionModes, value)

    def get_current_status(self):
        return self._System.GetCurrentStatus()

    def update_status(self):
        return self._System.UpdateStatus()

    def make_sequential(self):
        return self._System.MakeSequential()

    def make_nonsequential(self):
        return self._System.MakeNonSequential()

    def load(self, filepath, saveifneeded=False):
        """Loads an earlier defined zemax file


        Parameters
        ----------
        filepath: str
            The filepath that should be loaded
        saveifneeded: bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        logger.debug('Opening {} with SaveIfNeeded set to {}'.format(filepath, saveifneeded))

        self._System.LoadFile(filepath, saveifneeded)
        self._OpenFile = filepath

        logger.info('Opened {}'.format(filepath))

    def new(self, saveifneeded=False):
        """Creates a new session file.

        Parameters
        ----------
        saveifneeded: bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """

        logger.debug('Creating new file')

        self._System.New(saveifneeded)
        self._OpenFile = None

        logger.info('Opened new file')

    def save_as(self, filepath):
        """Saves the current session under a specified name.

        Parameters
        ----------
        filepath: str
            The filepath where the system should be saved. Note that a partial path or relative path does not work.
        """

        logger.debug('Saving open session as {}'.format(filepath))

        self._System.SaveAs(filepath)
        self._OpenFile = filepath

        logger.info('File saved as {}'.format(filepath))

    def save(self):
        """Saves the current optic studio session.

        If the file name for the current session is not known (e.g. when a new file was created), a warning is raised
        and the file is not saved. On these occurences, save_as() should be used once.

        Returns (bool): A boolean indicating if the saving was successful.

        """
        logger.debug('Saving file')

        if self._OpenFile is None:
            warnings.warn('No file name has been defined for the current system, the current session has not been '
                          'saved. Please use the save_as() function before using save.')
            logger.critical('Could not save file')

            return False
        else:
            self._System.Save()
            logger.info('File saved')
            return True

    def close(self, saveifneeded=False):
        """Closes the optical system. Only works on secondary systems (See OpticStudio documentation)

        Parameters
        ----------
        saveifneeded: bool
            Defines if the current file is saved before opening the new file. Defaults to False.
        """
        return self._System.Close(saveifneeded)

    def copy_system(self):
        """Copies the current OpticStudioSystem instance.

        Returns
        -------
        zospy.core.OpticStudioSystem
            A ZOSPy OpticStudioSystem instance. Should be sequential.
        """
        return OpticStudioSystem(self._ZOS, self._System.CopySystem())

    def _ensure_correct_mode(self, required):
        """Ensures that the system is in the required type

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
        logger.debug('Ensuring correct mode')
        if self.Mode != required:
            err = 'Incorrect system type. System is in {} mode but {} mode is required'.format(self.Mode, required)
            logger.critical(err)
            raise TypeError(err)
        else:
            logger.debug('System is in correct mode')
        # ToDo: Eveluate what happens in 'mixed mode'

    def __del__(self):
        logger.debug('Closing connections with Zemax OpticStudio')
        # ToDo Add cleanup

    def get_pupil(self):
        """Obtains the pupil data.

        Returns
        -------
        pd.Series
            The pupildata.
        """
        return get_pupil(self.LDE)

    def cardinal_points(self, surf1, surf2, oncomplete='Close', cfgoutfile=None, txtoutfile=None):
        """Wrapper around the OpticStudio Cardinal Point Analysis.

        Parameters
        ----------
        surf1: int
            The surface number corresponding to the first surface of the analyzed system
        surf2: int
            The surface number corresponding to the last surface of the analyzed system
        oncomplete: str

            Defines behaviour upon completion of the analysis. Should be one of ['close', 'release', 'sustain']. If
            'close', the analysis will be closed after completion. If 'release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interation when oncomplete ==
            'sustain', the OpticStudio Analysis instance will be availabe in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'close'.
        cfgoutfile: str or None
            The configuration file to which the current configuration is saved. If None, a temporary file will be
            created and deleted. If string, it should be a full system path with '.CFG' as extension, after which the
            file will be saved in that location. (Allowing usage of this configuration file using
            surface_data_fromcfg()). Defaults to None.
        txtoutfile: str or None
            The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and
            deleted. If string, it should be a full system path with '.txt' as extension, after which the file will
            be saved in that location. Defaults to None.

        Returns
        -------
        AnalysisResult
            A SurfaceDataSettings analysis result. Next to the standard data, the raw text return obtained from the
            analysis will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under
            'TxtOutFile'.
        """

        return reports.cardinal_points(self, surf1=surf1, surf2=surf2, oncomplete=oncomplete, cfgoutfile=cfgoutfile,
                                       txtoutfile=txtoutfile)

    def cardinal_points_fromcfg(self, cfgfile, oncomplete='Close', txtoutfile=None):
        """Wrapper around the OpticStudio Cardinal Point Analysis that uses a predefined configuration file.

        Parameters
        ----------
        cfgfile: str
            The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.
        txtoutfile: str or None
            The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and
            deleted. If string, it should be a full system path with '.txt' as extension, after which the file will
            be saved in that location. Defaults to None.

        Returns
        -------
        AnalysisResult
            A SurfaceDataSettings analysis result. Next to the standard data, the used cfgfile will be present under
            'UsedCfgFile', raw text return under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
        """

        return reports.cardinal_points_fromcfg(self, cfgfile=cfgfile, oncomplete=oncomplete, txtoutfile=txtoutfile)

    def surface_data(self, surf, oncomplete='Close', cfgoutfile=None, txtoutfile=None):
        """Wrapper around the OpticStudio Surface Data Analysis.

        Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
        subsequently reading in this file

        Parameters
        ----------
        surf: int
        The surface number that is to be analyzed
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.
        cfgoutfile: str or None
            The configuration file to which the current configuration is saved. If None, a temporary file will be
            created and deleted. If string, it should be a full system path with '.CFG' as extension, after which the
            file will be saved in that location. (Allowing usage of this configuration file using
            surface_data_fromcfg()). Defaults to None.
        txtoutfile: str or None
            The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and
            deleted. If string, it should be a full system path with '.txt' as extension, after which the file will be
            saved in that location. Defaults to None.

        Returns
        -------
        AnalysisResult
            A SurfaceDataSettings analysis result. Next to the standard data, the raw text return obtained from the
            analysis  will be present under 'RawTextData', the cfgoutfile under 'CfgOutFile', and the txtoutfile under
            'TxtOutFile'.
        """
        return reports.surface_data(self, surf=surf, oncomplete=oncomplete, cfgoutfile=cfgoutfile,
                                    txtoutfile=txtoutfile)

    def surface_data_fromcfg(self, cfgfile, oncomplete='Close', txtoutfile=None):
        """Wrapper around the OpticStudio Surface Data Analysis that uses a predefined configuration file.

        Due to limitations in the ZOS-API, the output is obtained by writing the OpticStudio results to a file and
        subsequently reading in this file

        Parameters
        ----------
        cfgfile: str
        The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.
        txtoutfile: str or None
            The textfile to which the Zemax output is saved. If None, a temporary file will be created and deleted. If
            string, it should be a full system path with '.txt' as extension, after which the file will be saved in that
            location. Defaults to None.

        Returns
        -------
        AnalysisResult
            A SurfaceDataSettings analysis result. Next to the standard data, the used cfgfile will be present under
            'UsedCfgFile', raw text return under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
        """
        return reports.surface_data_fromcfg(self, cfgfile=cfgfile, oncomplete=oncomplete, txtoutfile=txtoutfile)

    def zernike_standard_coefficients(self, sampling='64x64', maximum_term=37, wavelength=1, field=1,
                                      reference_opd_to_vertex=False, surface='Image', sx=0.0, sy=0.0, sr=0.0,
                                      oncomplete='Close', txtoutfile=None):
        """Wrapper around the OpticStudio Zernike Standard Coefficient Analysis.

        Parameters
        ----------
        sampling: str or int
        The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants integer.
        maximum_term: int
            The maximum Zernike term, defaults to 37.
        wavelength: int
            The wavelength number that is to be used. Defaults to 1 (the first wavelength).
        field:
            The field that is to be analyzed. Defaults to 1.
        reference_opd_to_vertex: bool
            If the OPD should be referenced to vertex. Defaults to False.
        surface: str or int
            The surface that is to be analyzed. Either 'Image', 'Object' or an integer. Defaults to 'Image'.
        sx: float
            The sx.
        sy: float
            The sy.
        sr: float
            The sr.
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.
        txtoutfile: str or None
            The textfile to which the OpticStudio output is saved. If None, a temporary file will be created and
            deleted. If string, it should be a full system path with '.txt' as extension, after which the file will be
            saved in that location. Defaults to None.

        Returns
        -------
        AnalysisResult
            A ZernikeStandardCoefficients analysis result. Next to the standard data, the raw text return obtained from
            the analysis will be present under 'RawTextData' and the txtoutfile under 'TxtOutFile'.
        """
        return wavefront.zernike_standard_coefficients(self, sampling=sampling, maximum_term=maximum_term,
                                                       wavelength=wavelength, field=field,
                                                       reference_opd_to_vertex=reference_opd_to_vertex, surface=surface,
                                                       sx=sx, sy=sy, sr=sr, oncomplete=oncomplete,
                                                       txtoutfile=txtoutfile)

    def fft_through_focus_mtf(self, sampling='64x64', deltafocus=0.1, frequency=0, numberofsteps=5, wavelength='All',
                              field='All', mtftype='Modulation', use_polarization=False, use_dashes=False,
                              oncomplete='Close'):
        """Wrapper around the OpticStudio FFT Through Focus MTF.

        For an in depth explanation of the parameters, see the Zemax OpticStudio user manual

        Parameters
        ----------
        sampling: str or int
            The sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
            integer.
        deltafocus: float
            The delta focus, defaults to 0.1
        frequency: float
            The frequency. Defaults to 0.
        numberofsteps: int
            The number of steps. Defaults to 5.
        wavelength: str or int
            The wavelength to use in the MTF. Either 'All' or an integer specifying the wavelength number.
        field: str or int
            The field to use in the MTF. Either 'All' or an integer specifying the field number.
        mtftype: str or int
            The MTF type (e.g. 'Modulation') that is calculated.
        use_polarization: bool
            Use polarization. Defaults to False.
        use_dashes: bool
            Use dashes. Defaults to False.
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.

        Returns
        -------
        AnalysisResult
            An FftThroughFocusMtf analysis result
        """
        return mtf.fft_through_focus_mtf(self, sampling=sampling, deltafocus=deltafocus, frequency=frequency,
                                         numberofsteps=numberofsteps, wavelength=wavelength, field=field,
                                         mtftype=mtftype, use_polarization=use_polarization, use_dashes=use_dashes,
                                         oncomplete=oncomplete)

    def fft_through_focus_mtf_fromcfg(self, cfgfile, oncomplete='Close'):
        """Wrapper around the OpticStudio FFT Through Focus MTF.

        For an in depth explanation of the parameters, see the Zemax OpticStudio user manual

        Parameters
        ----------
        cfgfile: str
            The configuration file that is to be used. Should be a full system path with '.CFG' as extension.
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.

        Returns
        -------
        AnalysisResult
            An FftThroughFocusMtf analysis result
        """
        return mtf.fft_through_focus_mtf_fromcfg(oss=self, cfgfile=cfgfile, oncomplete=oncomplete)

    def huygens_psf(self, pupil_sampling='32x32', image_sampling='32x32', image_delta=0, rotation=0, wavelength='All',
                    field=1, psftype='Linear', show_as='Surface', use_polarization=False, use_centroid=False,
                    normalize=False, oncomplete='Close'):
        """Wrapper around the OpticStudio Huygens PSF

        Parameters
        ----------
        pupil_sampling: str or int
            The pupil sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
            integer.
        image_sampling: str or int
            The image sampling, either string (e.g. '64x64') or int. The integer will be treated as a ZOSAPI Constants
            integer.
        image_delta: float or int
            The image delta
        rotation: int
            The rotation, should be one off [0, 90, 180, 270].
        wavelength: str or int
            The wavelength number that is to be used. Either 'All' or an integer specifying the wavelength number.
            Defaults to 'All'.
        field: str or int
            The field number that is to be used. Either 'All' or an integer specifying the field number. Defaults to 1.
        psftype: str or int
            The PSF type (e.g. 'Linear') that is calculated. Defaults to 'Linear'.
        show_as: str or int
            Defines how the data is showed within OpticStudio. Defaults to 'Surface'
        use_polarization: bool
            Defines if polarization is used. Defaults to False.
        use_centroid: bool
            Defines if centroid is used. Defaults to False.
        normalize: bool
            Defines if normalization is used. Defaults to False.
        oncomplete: str
            Defines behaviour upon completion of the analysis. Should be one of ['Close', 'Release', 'Sustain']. If
            'Close', the analysis will be closed after completion. If 'Release', the analysis will remain open in
            OpticStudio, but the link with python will be destroyed. If 'Sustain' the analysis will be kept open in
            OpticStudio and the link with python will be sustained. To enable interaction when oncomplete ==
            'Sustain', the OpticStudio Analysis instance will be available in the returned AnalysisResult through
            AnalysisResult.Analysis. Defaults to 'Close'.

        Returns
        -------
        AnalysisResult
            A HuygensPsf analysis result
        """
        return psf.huygens_psf(self, pupil_sampling=pupil_sampling, image_sampling=image_sampling,
                               image_delta=image_delta, rotation=rotation, wavelength=wavelength, field=field,
                               psftype=psftype, show_as=show_as, use_polarization=use_polarization,
                               use_centroid=use_centroid, normalize=normalize, oncomplete=oncomplete)


class ZOS:
    """An Communication instance for Zemax OpticStudio.

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

    Attributes:
        ZOSAPI (None | netModuleObject): The ZOSAPI interface or if loaded.
        ZOSAPI_NetHelper (None | netModuleObject): The ZOSAPI_NetHelper interface if loaded.
    """

    _OpticStudioSystem = OpticStudioSystem

    _instances = set()

    def __new__(cls, *args, **kwargs):

        if len(cls._instances) >= 1:
            # As the number of applications within runtime is limited to 1 by Zemax, it is logical to also limit the
            # number of ZOS instances
            raise ValueError('Cannot have more than one active ZOS instance')

        instance = super(ZOS, cls).__new__(cls, *args, **kwargs)

        return instance

    def __init__(self):
        """Initiation of the ZOS Instance."""
        logger.debug('Initializing ZOS instance')

        self.ZOSAPI = None
        self.ZOSAPI_NetHelper = None
        self.Connection = None
        self.Application = None

        # Register the instance and create a finalize code to remove it from ZOS._instances when deleted
        ZOS._instances.add(id(self))
        weakref.finalize(self, ZOS._instances.discard, id(self))

        logger.info('ZOS instance initialized')

    @property
    def Constants(self):  # noqa
        """Class level access to constants to maintain compatibility with older code."""
        return constants

    def wakeup(self, preload=False, zosapi_nethelper=None):
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

    def _load_zos_dlls(self, preload=False, zosapi_nethelper=None):
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
        logger.debug('Loading ZOS DLLs with preload set to {}'.format(preload))
        self.ZOSAPI_NetHelper = load_zosapi_nethelper(filepath=zosapi_nethelper, preload=preload)
        self.ZOSAPI = load_zosapi(self.ZOSAPI_NetHelper, preload=preload)

    def _assign_connection(self):
        """Assigns the ZOSAPI Connection to self.Connection"""
        if not self.Connection:
            logger.debug('Assigning ZOSAPI_Connection() to self.Connection')
            self.Connection = self.ZOSAPI.ZOSAPI_Connection()
        else:
            logger.debug('ZOSAPI_Connection() already assigned self.Connection')

    def connect_as_extension(self, instancenumber=0):
        """Creates a standalone Zemax Opticstudio instance.

        The application will be assigned to self.Application.

        Returns
        -------
        bool
            True if a valid connection is made, else False
        """

        self._assign_connection()

        if self.Connection.IsAlive:  # ToDo ensure no memory leak
            raise RuntimeError('Only one Zemax application can exist within runtime')

        self.Application = self.Connection.ConnectAsExtension(instancenumber)

        if self.Application.IsValidLicenseForAPI:
            return True
        else:
            logger.critical('OpticStudio Licence is not valid for API, connection not established')
            return False

    def create_new_application(self):
        """Creates a standalone Zemax Opticstudio instance.

        The application will be assigned to self.Application.

        Returns
        -------
        bool
            True if a valid connection is made, else False
        """
        self._assign_connection()

        if self.Connection.IsAlive:  # ToDo ensure no memory leak
            raise RuntimeError('Only one Zemax application can exist within runtime')

        self.Application = self.Connection.CreateNewApplication()

        if self.Application.IsValidLicenseForAPI:
            return True
        else:
            logger.critical('OpticStudio Licence is not valid for API, connection not established')
            return False

    def get_primary_system(self):
        opticstudiosystem = self.Application.PrimarySystem
        return self._OpticStudioSystem(zos_instance=self, system_instance=opticstudiosystem)

    def get_system(self, pos=0):
        warnings.warn('ZOS.get_system() has not been tested yet')
        # ToDo test
        opticstudiosystem = self.Application.PrimarySystem.GetSystemAt(pos)
        return self._OpticStudioSystem(zos_instance=self, system_instance=opticstudiosystem)

    def licence_check(self):
        pass
