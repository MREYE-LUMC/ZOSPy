# Example: Escudero-Sanz eye model

This example shows how to create and analyze a wide-angle eye model described in the paper _[Off-axis aberrations of a wide-angle schematic eye model](https://doi.org/10.1364/JOSAA.16.001881)_  by I. Escudero-Sanz and R. navarro.

## Included functionalities

* _Sequential mode_:
  - Usage of `zospy.solvers.material_model()` to model the refractive index of the elements of the eye.
  - Usage of `zospy.analyses.viewers.viewer_3d` and `zospy.analyses.viewers.shaded_model()` to open viewers.
  - Usage of `zospy.analyses.psf.huygens_psf()` to perform a Huygens PSF analysis.

## Citation

Next to [citing ZOSPy](../../README.md#referencing), please also cite the following paper when using the data provided in this example:

> Escudero-Sanz, I. & Navarro, R. (1999).
> Off-axis aberrations of a wide-angle schematic eye model.
> Journal of the Optical Society of America A, 16(8), 1881-1891. 
> https://doi.org/10.1364/JOSAA.16.001881

## Warranty and liability

The examples are provided 'as is'. There is no warranty and rights cannot be derived from them, as is also stated in the general license of this repository.