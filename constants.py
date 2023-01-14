import numpy as np

steps = 1000

bl_amplitude = np.pi/4
bl_phaseOffset = np.pi/32
bl_frequency = 9

bl_targetAngles = (np.sin(np.linspace(0, 2*np.pi, steps) * bl_frequency + bl_phaseOffset)  * bl_amplitude) 

fl_amplitude = np.pi/4
fl_phaseOffset = 0
fl_frequency = 9

fl_targetAngles = (np.sin(np.linspace(0, 2*np.pi, steps) * fl_frequency + fl_phaseOffset)  * fl_amplitude) 
