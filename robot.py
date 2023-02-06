import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import time
import numpy as np
import constants as c
class ROBOT:
    def __init__(self,solutionID):
        self.solutionID = solutionID
        self.motors = {}
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.position_data = np.ndarray((c.steps,3))
        self.z_threshold_count = 0
        self.z_threshold = 2 * c.lh + c.fh + 0.25 * c.height
        #os.system(f'rm brain{self.solutionID}.nndf')

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

    def Record_Fitness(self, i):
        position = p.getBasePositionAndOrientation(self.robot)[0]
        for j in range(3):
            self.position_data[i][j] = position[j]
        if position[2] > self.z_threshold:
            self.z_threshold_count += 1

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)

        basePosition = basePositionAndOrientation[0]

        z_fraction = self.z_threshold_count / c.steps
        fitness = (z_fraction**2) * basePosition[0] * (basePosition[2]**2)
        with open(f'tmp{self.solutionID}.txt','w') as file:
            file.write(str(fitness))

        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')