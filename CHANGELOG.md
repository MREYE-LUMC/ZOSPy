# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html),
with one exception: small features that only simplify access to certain parts of the
ZOS-API can also be added in patch releases.

## [Unreleased]

### Added

### Fixed

### Changed

- Changed license to MIT (#57, #58) - 2023-12-22

### Deprecated

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
