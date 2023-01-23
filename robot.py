import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import time

class ROBOT:
    def __init__(self,solutionID):
        self.solutionID = solutionID
        self.motors = {}
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system(f'rm brain{self.solutionID}.nndf')

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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[bytes(jointName, 'utf-8')].Set_Value(self.robot, desiredAngle)
                #print(neuronName + ' ' + jointName + ' ' + str(desiredAngle))

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)

        basePosition = basePositionAndOrientation[0]

        xPosition = basePosition[0]
        
        with open(f'tmp{self.solutionID}.txt','w') as file:
            file.write(str(xPosition))

        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')