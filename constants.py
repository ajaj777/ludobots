import numpy as np

steps = 2500

amplitude = np.pi/4
phaseOffset = np.pi/32
frequency = 9



fl_amplitude = np.pi/4
fl_phaseOffset = 0
fl_frequency = 9

fl_targetAngles = (np.sin(np.linspace(0, 2*np.pi, steps) * fl_frequency + fl_phaseOffset)  * fl_amplitude) 
