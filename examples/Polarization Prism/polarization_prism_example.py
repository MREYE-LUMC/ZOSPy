"""In standalone runs and plots polarization analyses in Prism using total internal reflection."""

import matplotlib.pyplot as plt
import numpy as np

import zospy as zp

##########################
## Input

# Input Jones Vector
jx = 1
jy = 1
x_phase = 0
y_phase = 0


##########################
# Connect to OpticStudio
print("Connecting to Zemax API ...")
zos = zp.ZOS()
zos.wakeup()
zos.create_new_application()
oss = zos.get_primary_system()

# Load example file
example_file = "Prism using total internal reflection.zmx"
print(f"Loading file {example_file} ...")
oss.load(example_file)
oss.load(test_file)

# Polarization
print("Calculating Transmission ...\n")
return_transmission = zp.analyses.polarization.transmission(
    oss, jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase, sampling="64x64"
)
for key, value in return_transmission["Data"].items():
    if key != "Header":
        print("%s  \t%.2f%%" % (key, value["Total Transmission"] * 100))

# Get polarization map
print("\nGenerating Polarization Pupil Map ...")
ret = zp.analyses.polarization.polarization_pupil_map(
    oss, jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase, sampling="17x17"
)
df = ret["Data"]["Table"]

# Plot map
xy_length = len(np.unique(df["Px"]))
for ii in range(len(df)):
    # E-field coordinates
    phi = np.linspace(0, 2 * np.pi) - np.pi / 3
    Ex = np.real(df["Ex"][ii] * np.exp(1j * phi)) / xy_length + df["Px"].iloc[ii]
    Ey = (
        np.real(df["Ey"].iloc[ii] * np.exp(1j * phi + 1j * df["Phase(Deg)"].iloc[ii] * np.pi / 180)) / xy_length
        + df["Py"].iloc[ii]
    )

    # Plot E-field trajectories
    line = plt.plot(Ex, Ey, "k")

    # Add arrows
    line[0].axes.annotate("", xytext=(Ex[0], Ey[0]), xy=(Ex[1], Ey[1]), arrowprops=dict(arrowstyle="->", color="k"))
plt.xlabel("Px")
plt.ylabel("Py")
plt.axis("equal")
plt.title(example_file)
print("Done.")
plt.show()
