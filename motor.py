import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.phaseOffset = c.phaseOffset

        self.motorValues = (np.sin(np.linspace(0, 2*np.pi, c.steps) * self.frequency + self.phaseOffset)  * self.amplitude) 
        

    def Set_Value(self,robot,t):
        pyrosim.Set_Motor_For_Joint(
        bodyIndex = robot,
        jointName = self.jointName,
        controlMode = p.POSITION_CONTROL,
        targetPosition = self.motorValues[t],
        maxForce = 40)
