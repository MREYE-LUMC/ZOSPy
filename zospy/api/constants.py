"""
Submodule used for package wide access to all ZOS api constants. Note that the constant-naming within this module breaks
pep, but is kept as such to be in-sync with the api documentation. Constants should in general be accessed through
'zospy.constants' (or 'zp.constants'). All constants are obtained dynamically from the api. Therefore, they are only
available after running the code stated under examples.

Prior to starting the interaction with the zosapi, any attempt to obtain a constant from this module will throw an
AttributeError

Examples
--------
import zospy as zp
zos = zp.ZOS()
zos.wakeup()
zp.constants
"""

import logging
import warnings
from types import SimpleNamespace

from pandas import Index

from zospy import utils

logger = logging.getLogger(__name__)

_notloadederrormsg = """
ZOSAPI constant is not yet loaded. Please run the following code to load all constants:

    import zospy as zp
    zos = zp.ZOS()
    zos.wakeup()
"""


class _UnloadedZOSConstant(SimpleNamespace):
    def __getattr__(self, attr):
        raise AttributeError(_notloadederrormsg)


# Non-nested namespaces
LensUpdateMode = _UnloadedZOSConstant()
LicenseStatusType = _UnloadedZOSConstant()
UpdateStatus = _UnloadedZOSConstant()
SystemType = _UnloadedZOSConstant()
ZOSAPI_Mode = _UnloadedZOSConstant()

# Nested namespaces
Analysis = SimpleNamespace()
Common = SimpleNamespace()
Editors = SimpleNamespace()
Preferences = SimpleNamespace()
SystemData = SimpleNamespace()
Tools = SimpleNamespace()
Wizards = SimpleNamespace()

Analysis.AnalysisIDM = _UnloadedZOSConstant()
Analysis.DetectorViewerShowDataTypes = _UnloadedZOSConstant()
Analysis.ErrorType = _UnloadedZOSConstant()
Analysis.GridPlotType = _UnloadedZOSConstant()
Analysis.HuygensShowAsTypes = _UnloadedZOSConstant()
Analysis.HuygensSurfaceMftShowAsTypes = _UnloadedZOSConstant()
Analysis.POPSampling = _UnloadedZOSConstant()
Analysis.SampleSizes = _UnloadedZOSConstant()
Analysis.SampleSizes_ContrastLoss = _UnloadedZOSConstant()
Analysis.SampleSizes_Pow2Plus1 = _UnloadedZOSConstant()
Analysis.SampleSizes_Pow2Plus1_X = _UnloadedZOSConstant()
Analysis.ShowAs = _UnloadedZOSConstant()
Analysis.SurfaceCurvatureCrossData = _UnloadedZOSConstant()
Analysis.SurfaceCurvatureData = _UnloadedZOSConstant()
Analysis.SurfacePhaseData = _UnloadedZOSConstant()
Analysis.SurfaceSagData = _UnloadedZOSConstant()
Analysis.UserAnalysisDataType = _UnloadedZOSConstant()
Analysis.RayTracing = SimpleNamespace()
Analysis.RayTracing.PathAnalysisSortType = _UnloadedZOSConstant()
Analysis.Settings = SimpleNamespace()
Analysis.Settings.AxisType = _UnloadedZOSConstant()
Analysis.Settings.DetectorViewerScaleTypes = _UnloadedZOSConstant()
Analysis.Settings.DisplayOption = _UnloadedZOSConstant()
Analysis.Settings.HuygensPsfTypes = _UnloadedZOSConstant()
Analysis.Settings.Polarizations = _UnloadedZOSConstant()
Analysis.Settings.PsfSpread = _UnloadedZOSConstant()
Analysis.Settings.PsfTypes = _UnloadedZOSConstant()
Analysis.Settings.Rotations = _UnloadedZOSConstant()
Analysis.Settings.ScanTypes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations = SimpleNamespace()
Analysis.Settings.Aberrations.DisplayAsTypes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.Distortions = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.FFA_AberrationTypes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.FFA_DecompositionTypes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.FFA_DisplayTypes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.FFA_FieldShapes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.FFA_ShowAsTypes = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.FieldScanDirections = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.RayTraceType = _UnloadedZOSConstant()
Analysis.Settings.Aberrations.ZernikeCoefficientTypes = _UnloadedZOSConstant()
Analysis.Settings.EncircledEnergy = SimpleNamespace()
Analysis.Settings.EncircledEnergy.EncircledEnergyTypes = _UnloadedZOSConstant()
Analysis.Settings.EncircledEnergy.ExtendedSourceTypes = _UnloadedZOSConstant()
Analysis.Settings.EncircledEnergy.GeometricLineEdgeSpreadTypes = _UnloadedZOSConstant()
Analysis.Settings.EncircledEnergy.ReferToTypes = _UnloadedZOSConstant()
Analysis.Settings.Fans = SimpleNamespace()
Analysis.Settings.Fans.SagittalAberrationComponent = _UnloadedZOSConstant()
Analysis.Settings.Fans.TangentialAberrationComponent = _UnloadedZOSConstant()
Analysis.Settings.Mtf = SimpleNamespace()
Analysis.Settings.Mtf.HuygensMtfTypes = _UnloadedZOSConstant()
Analysis.Settings.Mtf.MtfDataTypes = _UnloadedZOSConstant()
Analysis.Settings.Mtf.MtfTypes = _UnloadedZOSConstant()
Analysis.Settings.Mtf.ShowAsTypes = _UnloadedZOSConstant()
Analysis.Settings.Mtf.SurfaceMtfTypes = _UnloadedZOSConstant()
Analysis.Settings.Psf = SimpleNamespace()
Analysis.Settings.Psf.FftPsfType = _UnloadedZOSConstant()
Analysis.Settings.Psf.PsfRotation = _UnloadedZOSConstant()
Analysis.Settings.Psf.PsfSampling = _UnloadedZOSConstant()
Analysis.Settings.RMS = SimpleNamespace()
Analysis.Settings.RMS.FieldDensities = _UnloadedZOSConstant()
Analysis.Settings.RMS.FocusDensities = _UnloadedZOSConstant()
Analysis.Settings.RMS.Method = _UnloadedZOSConstant()
Analysis.Settings.RMS.Orientations = _UnloadedZOSConstant()
Analysis.Settings.RMS.RayDensities = _UnloadedZOSConstant()
Analysis.Settings.RMS.ReferTo = _UnloadedZOSConstant()
Analysis.Settings.RMS.WaveDensities = _UnloadedZOSConstant()
Analysis.Settings.RMS.RMSField = SimpleNamespace()
Analysis.Settings.RMS.RMSField.DataType = _UnloadedZOSConstant()
Analysis.Settings.RMS.RMSFieldMap = SimpleNamespace()
Analysis.Settings.RMS.RMSFieldMap.DataType = _UnloadedZOSConstant()
Analysis.Settings.Spot = SimpleNamespace()
Analysis.Settings.Spot.ColorRaysBy = _UnloadedZOSConstant()
Analysis.Settings.Spot.Patterns = _UnloadedZOSConstant()
Analysis.Settings.Spot.Reference = _UnloadedZOSConstant()
Analysis.Settings.Spot.ShowScales = _UnloadedZOSConstant()
Analysis.Settings.Wavefront = SimpleNamespace()
Analysis.Settings.Wavefront.DataType = _UnloadedZOSConstant()
Analysis.Settings.Wavefront.FoucaultShowAs = _UnloadedZOSConstant()
Analysis.Settings.Wavefront.KnifeType = _UnloadedZOSConstant()
Analysis.Settings.Wavefront.Types = _UnloadedZOSConstant()

Common.SettingsDataType = _UnloadedZOSConstant()
Common.ZemaxColor = _UnloadedZOSConstant()
Common.ZemaxOpacity = _UnloadedZOSConstant()

Editors.CellDataType = _UnloadedZOSConstant()
Editors.EditorType = _UnloadedZOSConstant()
Editors.ReflectTransmitCode = _UnloadedZOSConstant()
Editors.SampleSides = _UnloadedZOSConstant()
Editors.Samplings = _UnloadedZOSConstant()
Editors.SolveStatus = _UnloadedZOSConstant()
Editors.SolveType = _UnloadedZOSConstant()
Editors.LDE = SimpleNamespace()
Editors.LDE.CoatingStatusType = _UnloadedZOSConstant()
Editors.LDE.ConversionOrder = _UnloadedZOSConstant()
Editors.LDE.CoordinateConversionResult = _UnloadedZOSConstant()
Editors.LDE.CoordinateReturnType = _UnloadedZOSConstant()
Editors.LDE.InterpolationMethod = _UnloadedZOSConstant()
Editors.LDE.PilotRadiusMode = _UnloadedZOSConstant()
Editors.LDE.PupilApodizationType = _UnloadedZOSConstant()
Editors.LDE.QTypes = _UnloadedZOSConstant()
Editors.LDE.SubstrateType = _UnloadedZOSConstant()
Editors.LDE.SurfaceApertureTypes = _UnloadedZOSConstant()
Editors.LDE.SurfaceColumn = _UnloadedZOSConstant()
Editors.LDE.SurfaceEdgeDraw = _UnloadedZOSConstant()
Editors.LDE.SurfaceScatteringTypes = _UnloadedZOSConstant()
Editors.LDE.SurfaceType = _UnloadedZOSConstant()
Editors.LDE.TiltDecenterOrderType = _UnloadedZOSConstant()
Editors.LDE.TiltDecenterPickupType = _UnloadedZOSConstant()
Editors.LDE.TiltType = _UnloadedZOSConstant()
Editors.LDE.XYSampling = _UnloadedZOSConstant()
Editors.MCE = SimpleNamespace()
Editors.MCE.MultiConfigOperandType = _UnloadedZOSConstant()
Editors.MFE = SimpleNamespace()
Editors.MFE.MeritColumn = _UnloadedZOSConstant()
Editors.MFE.MeritOperandType = _UnloadedZOSConstant()
Editors.NCE = SimpleNamespace()
Editors.NCE.ApertureShapes = _UnloadedZOSConstant()
Editors.NCE.ArrayMode = _UnloadedZOSConstant()
Editors.NCE.BirefringentMode = _UnloadedZOSConstant()
Editors.NCE.BirefringentReflections = _UnloadedZOSConstant()
Editors.NCE.DetectorDataType = _UnloadedZOSConstant()
Editors.NCE.DetectorShowAsType = _UnloadedZOSConstant()
Editors.NCE.DiffractionSplitType = _UnloadedZOSConstant()
Editors.NCE.DiffractiveFaceChoices = _UnloadedZOSConstant()
Editors.NCE.DrawingResolutionType = _UnloadedZOSConstant()
Editors.NCE.EfficiencySpectrumType = _UnloadedZOSConstant()
Editors.NCE.EndCapOptions = _UnloadedZOSConstant()
Editors.NCE.FaceIsType = _UnloadedZOSConstant()
Editors.NCE.HologramTypes = _UnloadedZOSConstant()
Editors.NCE.InterpolateChoices = _UnloadedZOSConstant()
Editors.NCE.NCEIndexType = _UnloadedZOSConstant()
Editors.NCE.ObjectColumn = _UnloadedZOSConstant()
Editors.NCE.ObjectScatteringTypes = _UnloadedZOSConstant()
Editors.NCE.ObjectType = _UnloadedZOSConstant()
Editors.NCE.OrderChoices = _UnloadedZOSConstant()
Editors.NCE.PixelAddressing = _UnloadedZOSConstant()
Editors.NCE.PolarDetectorDataType = _UnloadedZOSConstant()
Editors.NCE.RaysIgnoreObjectType = _UnloadedZOSConstant()
Editors.NCE.ScatterToType = _UnloadedZOSConstant()
Editors.NCE.ShapeChoices = _UnloadedZOSConstant()
Editors.NCE.SourceBulkScatterMode = _UnloadedZOSConstant()
Editors.NCE.SourceColorMode = _UnloadedZOSConstant()
Editors.NCE.SourceSamplingMethod = _UnloadedZOSConstant()
Editors.NCE.UniformAngleChoices = _UnloadedZOSConstant()
Editors.NCE.VolumePhysicsModelType = _UnloadedZOSConstant()
Editors.TDE = SimpleNamespace()
Editors.TDE.ToleranceColumn = _UnloadedZOSConstant()
Editors.TDE.ToleranceOperandType = _UnloadedZOSConstant()

Preferences.DateTimeType = _UnloadedZOSConstant()
Preferences.EncodingType = _UnloadedZOSConstant()
Preferences.LanguageType = _UnloadedZOSConstant()
Preferences.ShowLineAsType = _UnloadedZOSConstant()

SystemData.FNumberComputationType = _UnloadedZOSConstant()
SystemData.FieldColumn = _UnloadedZOSConstant()
SystemData.FieldNormalizationType = _UnloadedZOSConstant()
SystemData.FieldPattern = _UnloadedZOSConstant()
SystemData.FieldType = _UnloadedZOSConstant()
SystemData.HuygensIntegralSettings = _UnloadedZOSConstant()
SystemData.ParaxialRaysSetting = _UnloadedZOSConstant()
SystemData.PolarizationMethod = _UnloadedZOSConstant()
SystemData.QuadratureSteps = _UnloadedZOSConstant()
SystemData.RayAimingMethod = _UnloadedZOSConstant()
SystemData.ReferenceOPDSetting = _UnloadedZOSConstant()
SystemData.WavelengthPreset = _UnloadedZOSConstant()
SystemData.ZemaxAfocalModeUnits = _UnloadedZOSConstant()
SystemData.ZemaxAnalysisUnits = _UnloadedZOSConstant()
SystemData.ZemaxApertureType = _UnloadedZOSConstant()
SystemData.ZemaxApodizationType = _UnloadedZOSConstant()
SystemData.ZemaxMTFUnits = _UnloadedZOSConstant()
SystemData.ZemaxSourceUnits = _UnloadedZOSConstant()
SystemData.ZemaxSystemUnits = _UnloadedZOSConstant()
SystemData.ZemaxUnitPrefix = _UnloadedZOSConstant()

Tools.CriticalRayType = _UnloadedZOSConstant()
Tools.RayPatternOption = _UnloadedZOSConstant()
Tools.RunStatus = _UnloadedZOSConstant()
Tools.General = SimpleNamespace()
Tools.General.ArchiveFileStatus = _UnloadedZOSConstant()
Tools.General.CADAngularToleranceType = _UnloadedZOSConstant()
Tools.General.CADFileType = _UnloadedZOSConstant()
Tools.General.CADToleranceType = _UnloadedZOSConstant()
Tools.General.LensShape = _UnloadedZOSConstant()
Tools.General.LensType = _UnloadedZOSConstant()
Tools.General.QuickAdjustCriterion = _UnloadedZOSConstant()
Tools.General.QuickAdjustType = _UnloadedZOSConstant()
Tools.General.QuickFocusCriterion = _UnloadedZOSConstant()
Tools.General.RayPatternType = _UnloadedZOSConstant()
Tools.General.ScaleToUnits = _UnloadedZOSConstant()
Tools.General.SplineSegmentsType = _UnloadedZOSConstant()
Tools.Optimization = SimpleNamespace()
Tools.Optimization.OptimizationAlgorithm = _UnloadedZOSConstant()
Tools.Optimization.OptimizationCycles = _UnloadedZOSConstant()
Tools.Optimization.OptimizationSaveCount = _UnloadedZOSConstant()
Tools.RayTrace = SimpleNamespace()
Tools.RayTrace.LTEdgeSasmpling = _UnloadedZOSConstant()
Tools.RayTrace.LTRaySampling = _UnloadedZOSConstant()
Tools.RayTrace.NSCTraceOptions = _UnloadedZOSConstant()
Tools.RayTrace.OPDMode = _UnloadedZOSConstant()
Tools.RayTrace.RayStatus = _UnloadedZOSConstant()
Tools.RayTrace.RaysType = _UnloadedZOSConstant()
Tools.RayTrace.ZRDFormatType = _UnloadedZOSConstant()
Tools.Tolerancing = SimpleNamespace()
Tools.Tolerancing.CriterionComps = _UnloadedZOSConstant()
Tools.Tolerancing.CriterionFields = _UnloadedZOSConstant()
Tools.Tolerancing.Criterions = _UnloadedZOSConstant()
Tools.Tolerancing.MonteCarloStatistics = _UnloadedZOSConstant()
Tools.Tolerancing.SetupCaches = _UnloadedZOSConstant()
Tools.Tolerancing.SetupChanges = _UnloadedZOSConstant()
Tools.Tolerancing.SetupModes = _UnloadedZOSConstant()
Tools.Tolerancing.SetupPolynomials = _UnloadedZOSConstant()

Wizards.CriterionTypes = _UnloadedZOSConstant()
Wizards.DefaultAndDegrees = _UnloadedZOSConstant()
Wizards.DefaultAndFringes = _UnloadedZOSConstant()
Wizards.OptimizationTypes = _UnloadedZOSConstant()
Wizards.PupilArmsCount = _UnloadedZOSConstant()
Wizards.ReferenceTypes = _UnloadedZOSConstant()
Wizards.WizardType = _UnloadedZOSConstant()


def _getkeys(obj, stack, ep_only):
    """Constructs a list of all nested keys. Specifically designed for _list_nested_attributes().

    Parameters
    ----------
    obj: SimpleNamespace
        The namespace for which nested keys are to be listed
    stack: list[str]
        The current stack
    ep_only: bool
        Whether only endpoints are listed (recognized as UnloadedZOSConstant) or also all values inbetween

    Returns
    -------
    list[str]
        The nested keys
    """
    for k, v in obj.__dict__.items():
        k2 = stack + ([k] if k else [])  # don't return empty keys
        if ep_only and not isinstance(v, _UnloadedZOSConstant) and isinstance(v, SimpleNamespace):
            for c in _getkeys(v, k2, ep_only):
                yield c
        elif not ep_only and not isinstance(v, _UnloadedZOSConstant) and isinstance(v, SimpleNamespace) and \
                len(v.__dict__) > 0:
            for c in _getkeys(v, k2, ep_only):
                yield c
        else:  # leaf
            yield k2


def _list_nested_attributes(param, endpoints_only=False):
    """Lists all nested attributes.

    Parameters
    ----------
    param: SimpleNamespace
        One of the above defined constants for which the nested attributes are to be listed.
    endpoints_only: bool
        Defines if only endpoints of endpoints and all steps in between are returned

    Returns
    -------
    List
        A list of all nested attributes

    """
    logger.debug('Listing nesting (endpoints_only={})'.format(endpoints_only))

    keys = list(_getkeys(param, [], endpoints_only))

    if endpoints_only:
        ret = ['.'.join(item) for item in keys]
    else:
        ret = []
        for item in keys:
            for ii in range(1, len(item) + 1):
                dep = '.'.join(item[:ii])
                if dep not in ret:
                    ret.append(dep)

    return ret


def update_from_zosapi(zosapi):
    """Updates the constants from a ZOSAPI instance.

    Parameters
    ----------
    zosapi
        A ZOSAPI instance (e.g. zospy.zpcore.ZOS().ZOSAPI

    Returns
    -------
    None

    Warns
    -----
    ImportWarning
        If one of the sets of constants cannot be found
    """
    logging.info('Updating ZOSAPI Constants from ZOSAPI')

    without_nesting = ['LensUpdateMode', 'LicenseStatusType', 'UpdateStatus', 'SystemType', 'ZOSAPI_Mode']
    with_nesting = ['Analysis', 'Common', 'Editors', 'Preferences', 'SystemData', 'Tools', 'Wizards']

    for constant in without_nesting:
        logger.debug(f'Updating constant "{constant}"')
        clrattr = utils.pyutils.rgetattr(zosapi, constant, None)
        if clrattr is not None:
            globals()[constant] = utils.clrutils.series_from_system_enum(clrattr)
            logger.debug(f'Constant "{constant}" updated')
        else:
            warnings.warn(f'Could not obtain constant "{constant}" from ZOSAPI', ImportWarning)
            logger.warning(f'Could not obtain constant "{constant}" from ZOSAPI')

    for constant in with_nesting:
        logger.debug(f'Updating constant "{constant}"')
        for subitem in _list_nested_attributes(globals()[constant], endpoints_only=True):
            clrattr = utils.pyutils.rgetattr(zosapi, f'{constant}.{subitem}', None)
            if clrattr is not None:
                utils.pyutils.rsetattr(globals()[constant], subitem, utils.clrutils.series_from_system_enum(clrattr))
                logger.debug(f'Constant "{constant}" updated')
            else:
                warnings.warn(f'Could not obtain constant "{constant}" from ZOSAPI', ImportWarning)
                logger.warning(f'Could not obtain constant "{constant}" from ZOSAPI')

    logging.info('Finished updating constants')


def get_constantname_by_value(constant_series, value):
    """Obtain a constant name from a value

    Parameters
    ----------
    constant_series: pd.Series
        The set of constants used to look up the value
    value: int
        The value for which the constant name is to be found

    Returns
    -------
    str
        The constant name
    """
    try:
        return constant_series.index[Index(constant_series).get_loc(value)]
    except KeyError:
        raise ValueError('None of the constants has value {} assigned'.format(value))
