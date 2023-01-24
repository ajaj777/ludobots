import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import time
import constants as c

class ROBOT:
    def __init__(self,solutionID, bodyIndex):
        self.solutionID = solutionID
        self.bodyIndex = bodyIndex
        self.motors = {}
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        
        self.robot = p.loadURDF(f"body{self.bodyIndex}.urdf")
       
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
           # print(jointName)
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self,t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)
        
    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Act(self,t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorRange
                self.motors[bytes(jointName, 'utf-8')].Set_Value(self.robot, desiredAngle)
                #print(neuronName + ' ' + jointName + ' ' + str(desiredAngle))

    def Get_Fitness(self):
        # modify to be 1 or 0 depending on if this robot is outside of the enclosure walls
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]
        yPosition = basePosition[1]
        fitness = 0
        if yPosition < c.enclosureStart[1]-c.enclosureBoxDims[1]/2:
            fitness = 1.0
        else:
            fitness = 0.0
        return fitness