import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import random
import time

class SOLUTION():
    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    # def Evaluate(self, directOrGUI):
    #     self.Start_Simulation(directOrGUI)
    #     #self.Wait_For_Simulation_To_End()

    def Start_Simulation(self,directOrGUI):
        self.Generate()
        os.system(f'python3 simulate.py ' + directOrGUI +' '+ str(self.myID) + ' 2&>1'+ ' &' )
       
    def Wait_For_Simulation_To_End(self):
        fitnessFileName = 'fitness' + str(self.myID) + '.txt'
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        with open(fitnessFileName,'r') as file:
            lines = file.readlines()
            self.fitness = float(lines[0])
       # print(self.fitness)
        os.system('rm ' + fitnessFileName)

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomColumn = random.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Generate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

    def Create_Body(self):
            pyrosim.Start_URDF("body.urdf")
            pyrosim.Send_Cube(name="Torso", pos=[c.x,c.y,c.z] , size=[c.length,c.width,c.height])
            pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.0,0.5,1.0], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="FrontLeg", pos=[0.0,0.5,0.0] , size=[0.2,1,0.2])

            pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0.0,-0.5,1.0,], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="BackLeg", pos=[0.0,-0.5,0.0] , size=[0.2,1,0.2])

            pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,0.0,1.0], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0.0,0.0] , size=[1,0.2,0.2])

            pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0.0,1.0], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0.0,0.0] , size=[1,0.2,0.2])

            pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0.0,1.0,0.0], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0.0,0.0,-0.5] , size=[0.2,0.2,1])

            pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0.0,-1.0,0.0], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="BackLowerLeg", pos=[0.0,0.0,-0.5] , size=[0.2,0.2,1])

            pyrosim.Send_Joint( name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1.0,0.0,0.0], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0.0,0.0,-0.5] , size=[0.2,0.2,1])

            pyrosim.Send_Joint( name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1.0,0.0,0.0], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="RightLowerLeg", pos=[0.0,0.0,-0.5] , size=[0.2,0.2,1])

            pyrosim.End()
            

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        for i in range(len(c.sensorNeurons)):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = c.sensorNeurons[i])
        for i in range(len(c.motorNeurons)):
            pyrosim.Send_Motor_Neuron(name = i + len(c.sensorNeurons), jointName = c.motorNeurons[i])
        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        # pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        # pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + len(c.sensorNeurons) , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2,2,c.z] , size=[c.length,c.width,c.height])
        pyrosim.End()