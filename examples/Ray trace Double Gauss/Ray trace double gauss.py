"""
In standalone runs and plots single ray traces
and ray fan analysis in Double Gauss lens.
"""

import matplotlib.pyplot as plt
import numpy as np

import zospy as zp

##########################
## Input

# Number of rays per field
Nr = 3

# Field coordinates
fields = [0, 10 / 14, 1]

# Plot colors for fields and wavelengths
cols = ["b", "g", "r"]

##########################
## Connect to OpticStudio
print("Connecting to Zemax API ...")
zos = zp.ZOS()
zos.wakeup()
zos.create_new_application()
oss = zos.get_primary_system()

# Load example file
file = "Double Gauss 28 degree field.zmx"
testFile = zos.Application.SamplesDir + "\\Sequential\\Objectives\\" + file
print('Loading file "%s" ...' % file)
oss.load(testFile)

## Run ray trace analysis
print("Running single ray traces ...")
for ii, hy in enumerate(fields):
    # Loop through pupil coordinates
    for py in np.linspace(-1, 1, Nr):
        # Run single ray trace
        raydata = zp.analyses.raysandspots.single_ray_trace(oss, hy=hy, py=py, wavelength=2, global_coordinates=True)

        # Extract real ray data
        raydf = raydata["Data"]["RealRayTraceData"]

        # Plot rays
        plt.plot(raydf.loc[1:]["Z-coordinate"], raydf.loc[1:]["Y-coordinate"], color=cols[ii])
plt.xlabel("Z-coordinate (mm)")
plt.ylabel("Y-coordinate (mm)")
plt.title(file)

## Run ray fan analysis
print("Running ray fan analysis ...")
rayfandata = zp.analyses.raysandspots.ray_fan(oss, number_of_rays=20, wavelength="All", field="All")

fig, ax = plt.subplots(2, 3, sharex=True, sharey=True)
ii = 0
for key, value in rayfandata["Data"].items():
    if key == "Header":
        continue

    for jj in range(value.shape[1] - 1):
        x = value["Pupil"]
        y = value.iloc[:, [jj + 1]]
        ax[ii % 2, int(ii / 2)].plot(x, y, c=cols[jj])
        ax[ii % 2, int(ii / 2)].set_title(key)
    ii += 1
ax[1, 1].set_xlabel("Pupil coordinate")
ax[0, 0].set_ylabel("ey (µm)")
ax[1, 0].set_ylabel("ex (µm)")

print("Done.")
plt.show()
