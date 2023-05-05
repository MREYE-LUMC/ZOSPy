"""
Supplementary materials to the scientific publication:

van Vught L, Que I, Luyten GPM, Beenakker JWM. Effect of anatomical differences and intraocular lens design on Negative
Dysphotopsia. Journal of Cataract & Refractive Surgery: September 06, 2022. doi: 10.1097/j.jcrs.0000000000001054

These supplementary materials consist of:

-	Eye models with specific anatomical characteristics for patients with Negative Dysphotopsia and for pseudophakic
controls

-	A python script to automatically determine the retinal illumination in Zemax Optic Studio through the ZOSPy API


When using these data/scripts, please cite the above mentioned paper.

The presented code and data are made available for research purposes only, no rights can be derived from them.

These methods has been tested using Zemax Optic Studio version 20.3.2, python version 3.7.5 and ZOSPy version 0.6.0.

Prior to running the script, make sure that the STL files supplied with this script are copied to the OpticStudio
r'Objects/CAD Files' folder. The exact location (if unknown)  can be obtained by running:

```
import zospy as zp
zos = zp.ZOS()
zos.wakeup()
zos.create_new_application()
objdir = zos.Application.ObjectsDir
zos.Application.CloseApplication()
```
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import zospy as zp


def set_axes_equal_3d(ax):
    """Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Parameters
    ----------
        ax: a matplotlib axis, e.g., as output from plt.gca().
    """

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


zos = zp.ZOS()
zos.wakeup()

# Make sure that Zemax OpticStudio in `Interactive Extension` mode (Programming > Interactive Extension)
zos.connect_as_extension()

oss = zos.get_primary_system()

pachy = 0.55
cornea_irisdist = 3.12
object_distance = 30  # distance object -> pupil center

results = {}
for model in ["NegativeDysphotopsia", "PseudophakicControl"]:
    fp = os.path.join(os.getcwd(), rf"{model}Model.zmx")
    oss.load(fp)

    # Get pointers to source and retina objects
    obj_source = oss.NCE.GetObjectAt(2)
    obj_retina = oss.NCE.GetObjectAt(14)

    # Set number of rays
    obj_source.GetCellAt(12).Value = str(1e5)

    first = True  # use this to get position of detectors on first analysis only
    results[model] = {"Irradiance": {}, "AbsorbedIrradiance": {}, "Flux": {}, "AbsorbedFlux": {}}
    for angle in range(0, 165, 5):
        xnew = np.sin(np.deg2rad(angle)) * object_distance
        znew = np.cos(np.deg2rad(angle)) * object_distance
        obj_source.XPosition = xnew
        obj_source.ZPosition = -(znew - pachy - cornea_irisdist)
        obj_source.TiltAboutY = -angle

        # Trace
        RayTrace = oss.Tools.OpenNSCRayTrace()
        RayTrace.NumberOfCores = 8
        RayTrace.ClearDetectors(0)  # clear the old detector data!
        RayTrace.ScatterNSCRays = True
        RayTrace.UsePolarization = False
        RayTrace.SplitNSCRays = False
        RayTrace.IgnoreErrors = True
        RayTrace.RunAndWaitForCompletion()
        RayTrace.Close()

        # Get data
        fd = obj_retina.GetFacetedObjectData()

        centroids = []
        irradiance = []
        absorbed_irradiance = []
        flux = []
        absorbed_flux = []

        for facenum in range(fd.NumberOfFaces):
            fd.CurrentFace = facenum
            if first:
                verts = np.array([list(fd.GetVertex(vertnum)[1:]) for vertnum in range(fd.NumberOfVertices)])
                centroids.append(verts.mean(axis=0))
            irradiance.append(fd.Irradiance)
            absorbed_irradiance.append(fd.AbsorbedIrradiance)
            flux.append(fd.Flux)
            absorbed_flux.append(fd.AbsorbedFlux)

        if first:
            results[model]["Centroids"] = np.array(centroids)
            first = False  # Make sure centroids are only read in once
        results[model]["Irradiance"][angle] = np.array(irradiance)
        results[model]["AbsorbedIrradiance"][angle] = np.array(absorbed_irradiance)
        results[model]["Flux"][angle] = np.array(flux)
        results[model]["AbsorbedFlux"][angle] = np.array(absorbed_flux)

# Show results
cumulative_irr_nd = np.array(
    [results["NegativeDysphotopsia"]["Irradiance"][key] for key in results["NegativeDysphotopsia"]["Irradiance"].keys()]
).sum(axis=0)

cumulative_irr_co = np.array(
    [results["PseudophakicControl"]["Irradiance"][key] for key in results["PseudophakicControl"]["Irradiance"].keys()]
).sum(axis=0)

fig = plt.figure()
ax1 = fig.add_subplot(121, projection=Axes3D.name)
ax2 = fig.add_subplot(122, projection=Axes3D.name)

vmax = np.max([cumulative_irr_nd.max(), cumulative_irr_co.max()])
filter_nd = cumulative_irr_nd != 0
ax1.scatter(
    *results["NegativeDysphotopsia"]["Centroids"][filter_nd].T[np.array([0, 2, 1])],
    c=cumulative_irr_nd[filter_nd],
    cmap="Greys_r",
    vmin=0,
    vmax=vmax,
    s=1,
)

filter_co = cumulative_irr_co != 0
ax2.scatter(
    *results["PseudophakicControl"]["Centroids"][filter_co].T[np.array([0, 2, 1])],
    c=cumulative_irr_co[filter_co],
    cmap="Greys_r",
    vmin=0,
    vmax=vmax,
    s=1,
)

ax1.set_title("ND")
ax2.set_title("Control")

set_axes_equal_3d(ax1)
set_axes_equal_3d(ax2)

ax1.set_xlabel("x")
ax1.set_ylabel("z")
ax1.set_zlabel("y")

ax2.set_xlabel("x")
ax2.set_ylabel("z")
ax2.set_zlabel("y")

plt.show()
