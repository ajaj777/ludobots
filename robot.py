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
import math
import utils
import sys
class ROBOT:
    def __init__(self,solutionID,brain=None, body=None):
        self.solutionID = solutionID
        self.motors = {}
        self.nn = None
        self.robot = None
        if brain:
            self.nn = NEURAL_NETWORK(brain)
        else:
            self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        if body:
            self.robot = p.loadURDF(body)
        else:
            self.robot = p.loadURDF(f"body{self.solutionID}.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.position_data = np.ndarray((c.steps,3))
        #os.system(f'rm brain{self.solutionID}.nndf')

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
       

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
           # print(jointName)
            index = pyrosim.jointNamesToIndices[jointName]
            jointType = p.getJointInfo(self.robot,index)[2]
            self.motors[jointName] = MOTOR(jointName, jointType)
           
            
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

    def Get_Fitness(self):
        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)

        # basePosition = basePositionAndOrientation[0]
        X_pos = []
        for i in range(p.getNumJoints(self.robot)):
            X_pos.append(p.getLinkState(self.robot,i)[0][0])
        
        
        # with open(f'robot{self.solutionID}.txt','w') as f:
        #     f.write(str(X_pos))

        avg_x  = np.mean(X_pos)
       
        fitness = abs(avg_x)
        #fitness = abs(basePosition[0])
        #fitness = basePosition[0]
        with open(f'tmp{self.solutionID}.txt','w') as file:
            file.write(str(fitness))

        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')

    def Print_Fitness(self):
        X_pos = []
        for i in range(p.getNumJoints(self.robot)):
            X_pos.append(p.getLinkState(self.robot,i)[0][0])
        
        
        # with open(f'robot{self.solutionID}.txt','w') as f:
        #     f.write(str(X_pos))

        avg_x  = np.mean(X_pos)
       
        fitness = abs(avg_x)
        print(f"Fitness value of this simulation: {fitness}")