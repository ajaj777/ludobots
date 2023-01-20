import numpy as np



sensorNeurons = ["Torso","BackLeg","FrontLeg","LeftLeg","RightLeg"]
motorNeurons = ["Torso_BackLeg","Torso_FrontLeg","Torso_LeftLeg","Torso_RightLeg",]

populationSize = 1
numberOfGenerations = 1

numSensorNeurons = 4
numMotorNeurons = 3

steps = 2000

amplitude = np.pi/4
phaseOffset = np.pi/32
frequency = 9

length = 1
width = 1
height = 1
x = 0
y  = 0
z = 1


fl_amplitude = np.pi/4
fl_phaseOffset = 0
fl_frequency = 9

fl_targetAngles = (np.sin(np.linspace(0, 2*np.pi, steps) * fl_frequency + fl_phaseOffset)  * fl_amplitude) 


