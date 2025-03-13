# Compatibility

The unit tests automatically check compatibility with different versions of OpticStudio against a reference version.
The current reference version is OpticStudio 25 R1.01.

```{include} compatibility_table.md
```

(compatibility/25-1-1)=
## OpticStudio 25.1.1

No known problems.

(compatibility/24-2-2)=
## OpticStudio 24.2.2

No known problems.

(compatibility/24-1-3)=
## OpticStudio 24.1.3

:::{list-table}
* - Type
  - Description
* - ℹ
  - The output of `zospy.analyses.polarization.TestPolarizationPupilMap` differs from the reference OpticStudio version in the returned Orientation. 
    This is a difference between the two OpticStudio versions, not an issue with ZOSPy. 
    As a result, the following unit tests fail:
     - `test_polarization_pupil_map_matches_reference_data[1-1-45-90-Image-17x17]`
:::

(compatibility/24-1-0)=
## OpticStudio 24.1.0

No known problems.
