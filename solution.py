import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import random

class SOLUTION():
    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(3,2) * 2 - 1

    def SetID(self, id):
        self.myID = id

    def Evaluate(self, directOrGUI):
        self.Generate()
        
        os.system(f'python3 simulate.py ' + directOrGUI +' '+ str(self.myID) + ' &' )
        # read in fitness.txt
        with open('fitness.txt','r') as file:
            lines = file.readlines()
            self.fitness = float(lines[0])


    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0,1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Generate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

    def Create_Body(self):
            pyrosim.Start_URDF("body.urdf")
            pyrosim.Send_Cube(name="Torso", pos=[c.x,c.y,c.z] , size=[c.length,c.width,c.height])
            pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-0.5,0,1.0])
            pyrosim.Send_Cube(name="FrontLeg", pos=[-0.5,0,-0.5] , size=[c.length,c.width,c.height])
            pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.5,0,1.0])
            pyrosim.Send_Cube(name="BackLeg", pos=[0.5,0,-0.5] , size=[c.length,c.width,c.height])
            pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+3 , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2,2,c.z] , size=[c.length,c.width,c.height])
        pyrosim.End()