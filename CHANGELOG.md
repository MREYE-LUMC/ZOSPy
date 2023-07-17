# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Fixed

### Changed

- Update the error message in `zospy.ZOS` to explain why only a single instance of `ZOS` is allowed (#24)

### Deprecated

### Removed

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