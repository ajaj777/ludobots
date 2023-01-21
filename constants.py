import numpy as np

# initial position of an octapod
initialPos = [-3,-3,0]
# number of bots to go in the respective x and y directions (in a square formation with some offset)
numBots = [3,3] 

# dimensions (length, width height) of an octapod torso
dimsTorso = [0.1,0.1,0.05]

sensorNeurons = ["Torso","BackLeg","FrontLeg","LeftLeg","RightLeg","FrontLowerLeg","BackLowerLeg","LeftLowerLeg","RightLowerLeg"]
motorNeurons = ["Torso_BackLeg","Torso_FrontLeg","Torso_LeftLeg","Torso_RightLeg","FrontLeg_FrontLowerLeg","BackLeg_BackLowerLeg","LeftLeg_LeftLowerLeg","RightLeg_RightLowerLeg"]

populationSize = 1
numberOfGenerations = 1

numSensorNeurons = 4
numMotorNeurons = 3

motorRange = 0.35
steps = 4000

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


