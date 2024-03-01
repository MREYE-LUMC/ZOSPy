# Proposed new FFT MTF analyses

This example shows and hopefully explains the design idea and functionality of the new FFT MTF Analyses

## Concept

The idea is that there is ZOSPy class representing the analysis window in Optic Studio.
An instance of the class can be freshly created or can be associated with the already opened analysis-windows.
To actually run the analysis the .Apply() or .ApplyAndWaitForCompletion() method needs to be called.

## new functions methods in existing files

class OpticStudioSystem has new property opened_analyses() and method get_analyses_of_type().

## new difinitions

There is a mtfclasses module with Fft_Mtf and Fft_Mtf_Map classes (so far)
For convenience (and to maintain sanity of a designer switching between OS directlt an ZOSPy)
FFT_MTF provides .os_colors for use in matplotlibs prop_cycler to mimic the OS color cycle
FFT_MTF_MAP provides .os_color_map and cmap_norm to make matplotlib.pyplot.pcolormesh or matplotlib.pyplot.confourf 
look similar to OS's color-plots
