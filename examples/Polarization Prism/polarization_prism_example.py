"""In standalone runs and plots polarization analyses in Prism using total internal reflection."""
from pathlib import Path

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

# Load example file; OpticStudio requires absolute paths
example_file = Path("Prism using total internal reflection.zmx").absolute()
print(f"Loading file {example_file} ...")
oss.load(str(example_file))

# Polarization
print("Calculating Transmission ...")
return_transmission = zp.analyses.polarization.transmission(
    oss, jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase, sampling="64x64"
)

print(
    f"{return_transmission.Data.FieldPos}  \t{return_transmission.Data.TotalTransmission * 100}%"
)

# Get polarization map
print("\nGenerating Polarization Pupil Map ...")
result = zp.analyses.polarization.polarization_pupil_map(
    oss, jx=jx, jy=jy, x_phase=x_phase, y_phase=y_phase, sampling="17x17"
)
df = result.Data.Table

# Plot map
xy_length = len(np.unique(df["Px"]))
for ii in range(len(df)):
    # E-field coordinates
    phi = np.linspace(0, 2 * np.pi) - np.pi / 3
    Ex = np.real(df["Ex"][ii] * np.exp(1j * phi)) / xy_length + df["Px"].iloc[ii]
    Ey = (
        np.real(
            df["Ey"].iloc[ii]
            * np.exp(1j * phi + 1j * df["Phase(Deg)"].iloc[ii] * np.pi / 180)
        )
        / xy_length
        + df["Py"].iloc[ii]
    )

    # Plot E-field trajectories
    line = plt.plot(Ex, Ey, "k")

    # Add arrows
    line[0].axes.annotate(
        "",
        xytext=(Ex[0], Ey[0]),
        xy=(Ex[1], Ey[1]),
        arrowprops=dict(arrowstyle="->", color="k"),
    )
plt.xlabel("Px")
plt.ylabel("Py")
plt.axis("equal")
plt.title(example_file.stem)
print("Done.")
plt.show()
