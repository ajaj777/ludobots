import numpy as np



# sensorNeurons = ["Torso","BackLeg","FrontLeg","LeftLeg","RightLeg","FrontLowerLeg","BackLowerLeg","LeftLowerLeg","RightLowerLeg"]
# motorNeurons = ["Torso_BackLeg","Torso_FrontLeg","Torso_LeftLeg","Torso_RightLeg","FrontLeg_FrontLowerLeg","BackLeg_BackLowerLeg","LeftLeg_LeftLowerLeg","RightLeg_RightLowerLeg"]

sensorNeurons = ["Torso","LeftLeg","RightLeg"]
motorNeurons = ["Torso_LeftLeg", "Torso_RightLeg"]

populationSize = 1
numberOfGenerations = 1


steps = 10000

amplitude = np.pi/4
phaseOffset = np.pi/32
frequency = 9

#proportion = 1.5
length = 0.5
width = 1.2
height = 1.25
lh = 0.75
lw = 0.1
ll = 0.1

fh = 0.1
fw = 0.025
fl = 0.05

x = 0
y  = 0
z = height/2 + lh

llx = x - 0.25 * width - 0.5 * lw
lly = y
llz = z - height/2

fl_amplitude = np.pi/4
fl_phaseOffset = 0
fl_frequency = 9

fl_targetAngles = (np.sin(np.linspace(0, 2*np.pi, steps) * fl_frequency + fl_phaseOffset)  * fl_amplitude) 


