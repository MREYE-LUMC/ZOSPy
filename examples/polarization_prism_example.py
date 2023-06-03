"""
In standalone runs and plots polarization 
analyses in Prism using total internal reflection.
"""

import zospy as zp
import matplotlib.pyplot as plt
import numpy as np


##########################
## Input

# Input Jones Vector
jx = 1
jy = 1
x_phase = 0
y_phase = 0


##########################
# Connect to OpticStudio
print('Connecting to Zemax API ...')
zos = zp.ZOS()
zos.wakeup()
zos.create_new_application()
oss = zos.get_primary_system()

# Load example file
file = "Prism using total internal reflection.zmx"
test_file = zos.Application.SamplesDir + "\\Sequential\\Tilted systems & prisms\\" + file
print('Loading file "%s" ...' %file)
oss.load(test_file)

# Polarization
print('Calculating Transmission ...\n')
ret0 = zp.analyses.transmission(oss, jx=jx, jy=jy,
                                x_phase=x_phase, y_phase=y_phase,
                                sampling='64x64')
for key, value in ret0['Data'].items():
    if key != 'Header':
        print('%s  \t%.2f%%' %(key,value['Total Transmission']*100))

# Get polarization map
print('\nGenerating Polarization Pupil Map ...')
ret = zp.analyses.polarization_pupil_map(oss, jx=jx, jy=jy,
                                         x_phase=x_phase, y_phase=y_phase,
                                         sampling='17x17')
df = ret['Data']['Table']

# Plot map
xylen =  len(np.unique(df['Px']))
for ii in range(len(df)):
    # E-field coordinates
    phi = np.linspace(0,2*np.pi)-np.pi/3
    Ex = np.real(df['Ex'][ii]*np.exp(1j*phi))/xylen+df['Px'].iloc[ii]
    Ey = np.real(df['Ey'].iloc[ii]*np.exp(1j*phi+1j*df['Phase(Deg)'].iloc[ii]*np.pi/180))/xylen+df['Py'].iloc[ii]

    # Plot E-field trajectories
    line = plt.plot(Ex,Ey,'k')

    # Add arrows
    line[0].axes.annotate('',
        xytext=(Ex[0], Ey[0]),
        xy=(Ex[1], Ey[1]),
        arrowprops=dict(arrowstyle="->", color='k'))
plt.xlabel('Px')
plt.ylabel('Py')
plt.axis('equal')
plt.title(file)
print('Done.')
plt.show()
