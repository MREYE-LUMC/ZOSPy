# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html),
with one exception: small features that only simplify access to certain parts of the
ZOS-API can also be added in patch releases.

## [Unreleased]

### Added

- FFT PSF analysis: `zospy.analysis.psf.FFTPSF` (#146)
- FFT MTF analysis: `zospy.analysis.mtf.FFTMTF` (#150)

### Fixed

- `OpticStudioSystem.copy_system` now uses `ZOS.get_instance` instead of an internal weak reference (#149)

### Deprecated

### Removed

## [[2.0.2]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v2.0.2) - 2025-04-23

### Fixed

- `zospy.analyses.wavefront.ZernikeStandardCoefficients` now supports fields of type object height (#144)

## [[2.0.1]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v2.0.1) - 2025-04-22

### Fixed

- `zospy.analyses.wavefront.ZernikeStandardCoefficients` now supports non-zero fields in the X-direction (#139)

## [[2.0.0]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v2.0.0) - 2025-03-17

### Added

- `zospy.zpcore.ZOS.get_instance` to get the existing `ZOS` instance, if present (#107).
- Test reference data for OpticStudio 2025 R1. This is now the reference version for the tests (#127).

### Fixed

- `zospy.analyses.base.Analysis` now raises an `AttributeError` when trying to set an attribute that is not present in the OpticStudio analysis object (#106).
- Obtain correct minimum x and y values in data grids for `zospy.analyses.extendedscene.geometric_image_analysis` (#103).
- Setting beam and fiber type with external files in `zospy.analyses.physicaloptics.physical_optics_propagation` (#114)

### Changed

- `zospy.zpcore.ZOS` now uses a singleton pattern to ensure only one instance of `ZOS` is created. If a second instance is created, the existing instance is returned instead and a warning is raised (#107)
- `zospy.zpcore.OpticStudioSystem._ZOS` was renamed to `ZOS`, making it a public attribute (#107)
- `zospy.analyses.new_analysis`: `settings_first` is now a keyword-only argument.
- `zospy.api.apisupport.load_zosapi_nethelper`: `preload` is now a keyword-only argument.
- `zospy.api.apisupport.load_zosapi`: `preload` is now a keyword-only argument.
- `zospy.functions.lde.find_surface_by_comment`: `case_sensitive` is now a keyword-only argument.
- `zospy.functions.nce.find_object_by_comment`: `case_sensitive` is now a keyword-only argument.
- `zospy.utils.flatten_dict`: `keep_unflattened` is now a keyword-only argument.
- `zospy.zpcore.OpticStudioSystem.load`: `saveifneeded` is now a keyword-only argument.
- `zospy.zpcore.OpticStudioSystem.new`: `saveifneeded` is now a keyword-only argument.
- `zospy.zpcore.OpticStudioSystem.close`: `saveifneeded` is now a keyword-only argument.
- `zospy.zpcore.ZOS.__init__`: all parameters are now keyword-only arguments.
- Replaced `zospy.utils.zputils.rsetattr` with `zospy.utils.zputils.attrsetter`, based on `operator.attrgetter`.
- `zospy.analyses` now uses a new, object-oriented interface for OpticStudio analyses (#118). The old interface is now deprecated, but still available in `zospy.analyses.old`.
  See discussion [#87](https://github.com/MREYE-LUMC/ZOSPy/discussions/87) and the release notes for more information.
- `zospy.utils.zputils.unpack_datagrid` now returns a DataGrid with column and row labels indicating the centers of the cells, instead
  of the bottom-left corners of the cells (#128).

### Deprecated

- `zospy.analyses.old` is deprecated in favor of the new object-oriented interface in `zospy.analyses` (#118).

### Removed

- `zospy.zpcore.ZOS.wakeup` is no longer needed, as the ZOS-API is now loaded in `zospy.zpcore.ZOS.__init__` (#107)
- `zospy.zpcore.ZOS.connect_as_extension`, `zospy.zpcore.ZOS.create_new_application` and `zospy.zpcore.ZOS.connect_as_standalone` have been removed in favor of `zospy.zpcore.ZOS.connect` (#107)
- `zospy.functions.nce.get_object_data` has been removed because it implements a conversion that is now done automatically by `zospy.api.codecs.OpticStudioInterfaceEncoder` (#107)
- Removed `zospy.utils.zputils.rgetattr` because `operator.attrgetter` does the same thing.

## [[1.3.1]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.3.1) - 2025-01-16

### Fixed

- Physical optics analysis start surface was hardcoded to 1 (#111, #112)

## [[1.3.0]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.3.0) - 2024-10-30

### Added

- Wavefront analysis: `zospy.analyses.wavefront.wavefront_map` (!61)
- Extended scene analysis: `zospy.analyses.extendedscene.geometric_image_analysis` (!61)
- Physical optics analysis: `zospy.analyses.physicaloptics.physical_optics_propagation` (!61)
  - Helper functions to generate specific parameter dictionaries for these analyses: `zospy.analyses.physicaloptics.pop_create_beam_parameter_dict`, `zospy.analyses.physicaloptics.pop_create_fiber_parameter_dict`
- Convenience function to change the aperture type of a surface in sequential mode: `zospy.functions.lde.surface_change_aperturetype`
- Experimental new interface for analyses in `zospy.analyses.new` (#78, #15)
- Add support for system viewer exports in `zospy.analyses.systemviewers.viewer_3d` and
  `zospy.analyses.systemviewers.cross_section` (#80).

### Changed

- Updated `zospy.functions.lde.surface_change_type` to also support surfaces that require the specification of a file to load. (!61)
- Added support for dictionary parameters in both `zospy.tests` and `zospy.scripts.generate_test_reference_data`. (!61)

## [[1.2.1]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.2.1) - 2024-03-11

### Fixed

- Unsupported locale setting on import (#66, #69)
- Zernike Standard Coefficients analysis parses dates as floats under German locale (#70)

### Changed

- Custom `__dir__` method for `zospy.analyses.base.Analysis`. 
  `dir` now shows both the wrapper members and the OpticStudio analysis members (!56)

## [[1.2.0]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.2.0) - 2024-01-19

### Added

- New, unified, connection method `ZOS.connect`. This method replaces the existing connection methods
  `ZOS.connect_as_extension`, `ZOS.create_new_application` and `ZOS.connect_as_standalone`.
  The connection mode is passed as an argument and the primary system is always returned (!47) 
- The OpticStudio installation directory can be manually specified using the `opticstudio_directory` 
  parameter of the `ZOS` class. This is particularly useful if multiple OpticStudio versions are installed
  on the same system and you want to use a specific version (!47)
  - **Note:** when this parameter is used, the `ZOSAPI_NetHelper` is not loaded and `ZOS.ZOSAPI_NetHelper` 
    remains unset.
- `zospy.api.codecs` for customized conversions between ZOS-API types and Python types (!48)
- `zospy.api.codecs.OpticStudioInterfaceEncoder` for automatic downcasting of certain common generic interfaces
    to their implementation (e.g. the use of `__implementation__` is no longer needed) (!48)
- MTF analysis: `huygens_mtf` (#55)
- `pickup_chief_ray` solver (!38)
- `ZOS.disconnect` to disconnect from OpticStudio (!47)
- Support for OpticStudio 2024 R1 (!51)
- Support for Python 3.12 (!54)

### Fixed

- `OpticStudioSystem.load` fails silently when path is incorrect or relative (#34)
- Saving after connecting in extension mode fails because `OpticStudioSystem._OpenFile` is not set.
  When connecting in extension mode, `_OpenFile` is now set with the path to the opened system to prevent this (#41)

### Changed

- Changed license to MIT (#57, #58) - 2023-12-22
- Deleting a `zospy.zpcore.ZOS` object now automatically calls `ZOS.disconnect` (!47)
- When connecting in extension mode, it is not necessary anymore to save the primary system with 
  `OpticStudioSystem.save_as` before it can be saved with `OpticStudioSystem.save` (!47, #41)
- `zospy.analyses.base.Analysis` now uses `zospy.api.codecs.OpticStudioInterfaceEncoder` to downcast
    analysis interfaces to their implementation (!48)
- Accept relative paths and check if the path exists in `OpticStudioSystem.load` and `OpticStudioSystem.save_as` (!50)
- Use `zospy.constants.process_constant` for parsing the `from_column` argument of `zospy.solvers.surface_pickup`.
  This column can now be specified as either a value from `zospy.constants` or a string (!53)

### Deprecated

- `ZOS.connect_as_extension`, `ZOS.create_new_application` and `ZOS.connect_as_standalone`.
  They have been replaced with `ZOS.connect` (!47)
- `zospy.functions.nce.get_object_data` is deprecated because its task is now performed by
    `zospy.api.codecs.OpticStudioInterfaceEncoder` (!48)

### Removed

## [[1.1.2]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.1.2) - 2023-12-13

### Fixed

- Reversed row index of datagrids in `zospy.utils.zputils.unpack_datagrid` (!42)

## [[1.1.1]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.1.1) - 2023-09-25

### Added

- `ZOS.connect_as_standalone` as alias for `ZOS.create_new_application` (#26)
- New parameter `return_primary_system` for `ZOS.connect_as_extension` and `ZOS.create_new_application`. These methods return the primary optical system if this parameter is `True`. If the license is not valid for the ZOS-API, a `ConnectionRefusedError` is raised (#26)
- `zospy.functions.nce.get_object_data` to get the data of an NCE object (#30)

### Fixed

- Erroneous parsing of analyses results when textfile encoding was not set to `Unicode` by implementing `zospy.zpcore.ZOS.get_txt_file_encoding` (!36)
- Bug that did not allow users to change the LensUpdateMode directly through `OpticStudioSystem.LensUpdateMode` (#40)

### Changed

- Updated how and when constants in `zospy.api.config` are determined for more clarity (!39)
- Update the error message in `zospy.ZOS` to explain why only a single instance of `ZOS` is allowed (#24)
- Load ZOS-API DLLs in `ZOS.__init__` (#26)

### Deprecated

- Separate calls to `ZOS.wakeup` are now redundant. This method will be removed in a later release (#26)

## [[1.1.0]](https://github.com/MREYE-LUMC/ZOSPy/releases/tag/v1.1.0) - 2023-07-03

### Added

- Polarization analyses: `polarization_pupil_map`, `transmission` (#14)
- System viewer analyses: `cross_section`, `viewer_3d`, `shaded_model`, `nsc_3d_layout`, `nsc_shaded_model` (!20)
- Documentation for all examples (!25)
- `version` property for the `ZOS` class (!21)
- `zospy.utils.pyutils.atox`, `zospy.utils.pyutils.xtoa` and `_config.THOUSANDS_SEPARATOR` for locale-aware conversion between strings and numbers (!26)
- [.zenodo.json](.zenodo.json) to have more control over Zenodo (!32)
- `zospy.functions.lde.find_surface_by_comment` and `zospy.functions.nce.find_object_by_comment` to find LDE surfaces / NCE objects based on their comments (#18)

### Fixed

- Bug when setting the MTF type though the ZOS-API for OpticStudio < 21.2; added `zospy.analyses.mtf._correct_fft_through_focus_mtftype_api_bug` (!21)
- Incorrect implementation of `zospy.zpcore.ZOS.get_system` (!30)
- Incorrect examples in the docstrings of `zospy.functions.lde.surface_change_type` and `zospy.functions.nce.object_change_type` (!31)

### Changed

- Converted some examples into Jupyter notebooks
- Renamed `_config.DECIMAL` to `_config.DECIMAL_POINT` (!26)
- Use `.zmx` files instead of `.zos` files for unit test reference system files (!23)
- Updated compatibility information in README.md (!29)

### Removed

- Empty method `zospy.zpcore.ZOS.licence_check` (!30)
