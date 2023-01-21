import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import random
import time

class SOLUTION():
    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(len(c.sensorNeurons),len(c.motorNeurons)) * 2 - 1


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
        self.Create_Swarm()
        #self.Create_Body()
        self.Create_Brain()

    def Create_Swarm(self):
        currentTorsoPos = c.initialPos # initial position [x,y,z] of torso of an octapod
        for i in range(c.numBots[0]):
            for j in range(c.numBots[1]):
                bIndex = c.numBots[0] * i + j
                self.Create_Body(bIndex,initPos=currentTorsoPos)

    def Create_Body(self, bodyIndex, initPos=[c.x,c.y,c.z]):
            x = initPos[0]
            y = initPos[1]
            z = initPos[2]
            dt = c.dimsTorso
            pyrosim.Start_URDF(f"body{bodyIndex}.urdf")
            
            pyrosim.Send_Cube(name="Torso", pos=initPos , size= dt)
            pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [x + 0.0, y + dt[1]/2, z + dt[2]], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="FrontLeg", pos=[0.0,0.5,0.0] , size=[0.2,1,0.2])

            pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [x + 0.0, y - dt[1]/2, z + dt[2]], jointAxis='1 0 0')
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
        # use the same brain for all octapods; we want the behavior to be generalized and not specific to starting location
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        for i in range(len(c.sensorNeurons)):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = c.sensorNeurons[i])

        for i in range(len(c.motorNeurons)):
            pyrosim.Send_Motor_Neuron(name = i + len(c.sensorNeurons), jointName = c.motorNeurons[i])

        for currentRow in range(len(c.sensorNeurons)):
            for currentColumn in range(len(c.motorNeurons)):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + len(c.sensorNeurons) , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        

    def Create_World(self):
        # create an enclosure for the octapod swarm to escape from
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2,2,c.z] , size=[c.length,c.width,c.height])
        pyrosim.End()