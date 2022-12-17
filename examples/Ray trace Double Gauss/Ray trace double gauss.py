"""
In standalone runs single ray traces in Double Gauss lens
and plots them like the layout viewer.
"""

import zospy as zp
import matplotlib.pyplot as plt
import numpy as np

##########################
## Input

# Number of rays per field
Nr = 3

# Field coordinates
fields = [0,0.5,1]

# Plot colors for fields
fieldcols = ['b','g','r']

##########################
## Connect to OpticStudio
zos = zp.ZOS()
zos.wakeup()
zos.create_new_application()
oss = zos.get_primary_system()

# Load example file
file = "Double Gauss 28 degree field.zos"
testFile = zos.Application.SamplesDir + "\\Sequential\\Objectives\\" + file
oss.load(testFile)

# Loop through fields
for ii, hy in enumerate(fields):
    # Loop through pupil coordinates
    for py in np.linspace(-1,1,Nr):
        # Run single ray trace
        raydata = zp.analyses.raytrace.single_ray_trace(oss,
                                                        Hy=hy,Py=py,
                                                        wavelength=2,
                                                        global_coordinates=True)

        # Extract real ray data
        raydf = raydata['Data']['RealRayTraceData']

        # Plot rays
        plt.plot(raydf.loc[1:]['Z-coordinate'],
                 raydf.loc[1:]['Y-coordinate'],
                 color=fieldcols[ii])
plt.xlabel('Z-coordinate (mm)')
plt.ylabel('Y-coordinate (mm)')
plt.title(file)
plt.show()
