---
title: 'ZOSPy: optical ray tracing in Python through OpticStudio'
tags:
  - Python
  - Ray tracing
  - OpticStudio
  - Zemax
authors:
  - name: Luc van Vught
    affiliation: "1, 2"
    corresponding: true
    equal-contrib: true
    orcid: 0000-0001-8290-9071
  - name: Corné Haasjes
    affiliation: "1, 2, 3"
    equal-contrib: true
    orcid: 0000-0003-0187-4116
  - name: Jan-Willem M. Beenakker
    affiliation: "1, 2, 3"
    orcid: 0000-0003-0479-5587
affiliations:
  - name: Department of Ophthalmology, Leiden University Medical Center, Leiden, the Netherlands
    index: 1
  - name: Department of Radiology, C.J. Gorter MRI Center, Leiden University Medical Center, Leiden, the Netherlands
    index: 2
  - name: Department of Radiation Oncology, Leiden University Medical Center, Leiden, the Netherlands
    index: 3
date: 07 June 2023
bibliography: paper.bib
---

# Summary
Zemax OpticStudio (Ansys, Inc) is a commonly used software package for designing optical setups and performing ray tracing simulations. It offers an Application Programming Interface (API) but interacting with this API is complex. Consequently, current ray tracing simulations generally require substantial manual user interaction, which in turn hampers the sharing of methods between scientists. We have therefore developed `ZOSPy`, a Python package that provides an accessible interface as well as unit tests. As a result, `ZOSPy` enables scientists to focus more on optical modelling instead of coding and contributes to open science as optical setups and analyses can easily be shared amongst users. 

# Statement of need
Ray tracing simulations are widely used to design, optimize and analyze optical systems. Its applications are diverse, ranging from designing spectrometers [@Naeem2022] or telescopes [@Zhang2023], to understanding the optics of the human eye [@Simpson2020; @vanVught2022]. Moreover, in ophthalmology, ray tracing is used to optimize the outcomes of cataract surgery [@Canovas2011; @Artal2023] and evaluate the accuracy of ocular radiotherapy [@Jaarsma2023]. These optical simulations are often performed in OpticStudio, which offers a powerful set of tools to design, optimize and evaluate optical systems.

Although OpticStudio offers an API, the `ZOS-API`, using this API in Python is complex and time-consuming. It involves, for example, establishing a connection with the API through the .NET framework, casting between .NET and Python datatypes, identifying which constants need to be set in specific cases, and working around  non-uniform methods of parsing the output [@GettingStartedWithZOSAPI]. This leads to studies which, in practice, largely rely on user interaction and therefore mostly assess a small number of optical systems. Although this is generally sufficient for the design of an optical system, other applications would benefit from the evaluation a large set of systems. In vision science, for example, clinical studies typically analyze vision-related complaints in cohorts of hundreds of eyes [@Ellis2001; @Osher2008], but the ray-tracing studies aiming to link these complaints to the subject’s ocular optics are limited to a small number of eyes [@Holladay1999; @Simpson2020]. Furthermore, the sharing of methodology is often limited to screenshots [@Hong2011], simple tables [@Naeem2022] or optical systems saved in the proprietary file format of OpticStudio [@Polans2018], which hinders open science initiatives. 

With `ZOSPy`, we aim to provide an accessible interface to the OpticStudio API, enabling the user to focus on optical modelling instead of complex coding. Furthermore, as users can directly share their optical system via Python scripts or Jupyter Notebooks rather than screenshots or optical systems saved in proprietary file formats, we strive to facilitate open science. 

# Functionality
`ZOSPy` is, in its most basic form, a Python wrapper around the OpticStudio API. It facilitates the .NET connection required to connect to OpticStudio through its API, as well as all subsequent casting of variables between .NET and Python. Additionally, it provides object-oriented methods to define surfaces and their optical properties. Furthermore, it offers single-line, easy to understand, methods to perform analyses that return the analysis results in a uniform way. As a result, `ZOSPy` enables a straight-forward interaction with OpticStudio and improves code readability, which facilitates method sharing between scientists.

`ZOSPy` also offers autocompletion. Interacting with OpticStudio through its API requires the use of many constants, for example to define the shape of an optical surface or initiate an analysis. These constants do not autocomplete in IDEs such as PyCharm or VS Code as the API is built on the .NET framework. As a result, the user has to know the exact name of each constant, for example `ZOSAPI.Analysis.Settings.Mtf.MtfTypes.Modulation`. `ZOSPy`, however, includes stubs for all constants and functions, enabling full autocompletion. 

Finally, `ZOSPy` offers a set of unit tests to assure that the software provides correct results. These tests provide means to compare results across `ZOSPy` and Python versions, as well as across versions of OpticStudio. The current version of `ZOSPy` provides basic tests for the most common optical surfaces and analyses.


# Use cases
Multiple examples, from modelling the effect of a coated prism on the polarization of light to assessing the optical characteristics of the human eye have been contributed to `ZOSPy`. These examples provide new users with an easy start with `ZOSPy`. A minimal example of using `ZOSPy` to create and evaluate a thick lens is shown below, and the corresponding results are shown in \autoref{fig:1}. 

```python
import zospy as zp

# Initiate the connection to OpticStudio
zos = zp.ZOS()
zos.wakeup()
zos.connect_as_extension()
oss = zos.get_primary_system()
oss.new()

# Set up the optical system
oss.SystemData.Aperture.ApertureValue = 10

input_beam = oss.LDE.InsertNewSurfaceAt(1)
input_beam.Thickness = 10

# Make a 10 mm thick lens with a radius of curvature of 30mm 
# and material type BK10 
front_surface = oss.LDE.GetSurfaceAt(2)
front_surface.Radius = 30
front_surface.Thickness = 10
front_surface.SemiDiameter = 15
front_surface.Material = "BK10"

back_surface = oss.LDE.InsertNewSurfaceAt(3)
back_surface.Radius = -30
back_surface.Thickness = 29
back_surface.SemiDiameter = 15

# Make a detector surface
image_surface = oss.LDE.GetSurfaceAt(4)
image_surface.SemiDiameter = 5

# Render the model
draw3d = zp.analyses.systemviewers.viewer_3d(oss)

# Analyze the system by calculating the Modulation Transfer Function (MTF) 
# and the Point Spread Function (PSF)
mtf = zp.analyses.mtf.fft_through_focus_mtf(
    oss, sampling="512x512", deltafocus=2.5, numberofsteps=51)

huygens_psf = zp.analyses.psf.huygens_psf(
    oss, pupil_sampling="512x512", image_sampling="512x512", normalize=True)
```

![**Results of the example code**. **A)** The created optical system results in a slightly out of focus image. **B)** The calculated Modulation Transfer Function (MTF) shows that the image plane needs a 1.9 mm shift towards the lens to be in focus. **C)** The Huygens Point Spread Function (PSF) shows the aberrations of the system.\label{fig:1}](Figure%201.png)

Furthermore, `ZOSPy` has been used in different ophthalmic studies. In one of these studies, `ZOSPy` was used to evaluate the relation of ocular anatomy to peripheral visual complaints [@vanVught2022]. In another study, `ZOSPy` showed that the extent of an intra-ocular tumor can be overestimated during surgery due to its shadow (\autoref{fig:2}) [@Jaarsma2023].

![**Simulation mimicking the clip surgery for radiotherapy of an intraocular tumor [@Jaarsma2023]**. The ocular geometry including the dimension of the tumor were loaded into OpticStudio using `ZOSPy` and the *CAD Part: STL* object type, after which the retinal illumination was simulated. The results were rendered using the non-sequential Shaded Model analysis (`zospy.analyses.systemviewers.nsc_shaded_model`).\label{fig:2}](Figure%202.png)

# Acknowledgements
We would like to thank all users that have reported bugs or implemented new functionality. 

# References

