import numpy as np
import math

# enclosure bottomleft
enclosureStart = [-10,-2]
# enclosure size
enclosureLength = 2
#enclosure box dims
enclosureBoxDims = [1,1,2]
# number of bots to go in the respective x and y directions (in a square formation with some offset)
numBots = [3,3] 

# initial position of an octapod
initialPos = [0,0,3]

# dimensions (length, width height) of an octapod torso
dimsTorso = [0.75,0.75,0.4]

# sensorNeurons = ["Torso","BackLeg","FrontLeg","LeftLeg","RightLeg","FrontLowerLeg","BackLowerLeg","LeftLowerLeg","RightLowerLeg"]
# motorNeurons = ["Torso_BackLeg","Torso_FrontLeg","Torso_LeftLeg","Torso_RightLeg","FrontLeg_FrontLowerLeg","BackLeg_BackLowerLeg","LeftLeg_LeftLowerLeg","RightLeg_RightLowerLeg"]

sensorNeurons = ["Torso","BackLeg","FrontLeg","LeftLeg","RightLeg","TopLeg", "BottomLeg", "BottomLowerLeg"]
motorNeurons = ["Torso_BackLeg","Torso_FrontLeg","Torso_LeftLeg","Torso_RightLeg","Torso_TopLeg","Torso_BottomLeg","BottomLeg_BottomLowerLeg"]

populationSize = 10
numberOfGenerations = 10

# numSensorNeurons = 4
# numMotorNeurons = 3

motorRange = np.pi / 4
steps = 1000

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

