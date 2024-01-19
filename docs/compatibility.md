# Compatibility

```{include} compatibility_table.md
```

(compatibility/24-1-0)=
## OpticStudio 24.1.0

No known problems.

(compatibility/23-2-1)=
## OpticStudio 23.2.1

No known problems.

(compatibility/23-1-0)=
## OpticStudio 23.1.0

No known problems.

(compatibility/20-3-2)=
## OpticStudio 20.3.2

:::{list-table}
* - Type
  - Python
  - Description
* - ℹ
  - All
  - The output of `zospy.analyses.polarization.TestPolarizationPupilMap` differs from the reference OpticStudio version in the returned Orientation. 
    This is a difference between the two OpticStudio versions, not an issue with ZOSPy. 
    As a result, the following unit tests fail:
     - `test_polarization_pupil_map_matches_reference_data[1-0-0-0-Image-11x11]`
     - `test_polarization_pupil_map_matches_reference_data[1-1-45-90-Image-17x17]`
:::