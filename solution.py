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

    def Get_ID(self):
        return self.myID
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
        os.system(f'rm brain{self.myID}.nndf')
        
    def Mutate(self):
        randomRow = random.randint(0,len(c.sensorNeurons)-1)
        randomColumn = random.randint(0,len(c.motorNeurons)-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Generate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

    def Create_Body(self):
            pyrosim.Start_URDF("body.urdf")
            pyrosim.Send_Cube(name="Torso", pos=[c.x,c.y,c.z] , size=[c.length,c.width,c.height])

            pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [0,-0.25,2*c.lh + c.fh], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="LeftLeg", pos=[0,0,-c.lh/2] , size=[0.2,0.2,c.lh])

            pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0,0.25,2*c.lh], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="RightLeg", pos=[0,0,-c.lh/2] , size=[0.2,0.2,c.lh])

            pyrosim.Send_Joint( name = "Torso_LowerLeftLeg" , parent= "LeftLeg" , child = "LowerLeftLeg" , type = "revolute", position = [0.0,0.0,-c.lh], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0.0,0.0,-c.lh/2] , size=[0.2,0.2,c.lh])

            pyrosim.Send_Joint( name = "Torso_LowerRightLeg" , parent= "RightLeg" , child = "LowerRightLeg" , type = "revolute", position = [0.0,0.0,-c.lh], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="LowerRightLeg", pos=[0.0,0.0,-c.lh/2] , size=[0.2,0.2,c.lh])

            # add feet

            pyrosim.Send_Joint( name = "LowerLeftLeg_LeftFoot" , parent= "LowerLeftLeg" , child = "LeftFoot" , type = "revolute", position = [0.0,0.0,-c.lh], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="LeftFoot", pos=[0.0,0.0,-c.fh/2] , size=[c.fw,c.fl,c.fh])

            pyrosim.Send_Joint( name = "LowerRightLeg_RightFoot" , parent= "LowerRightLeg" , child = "RightFoot" , type = "revolute", position = [0.0,0.0,-c.lh], jointAxis='0 1 0')
            pyrosim.Send_Cube(name="RightFoot", pos=[0.0,0.0,-c.fh/2] , size=[c.fw,c.fl,c.fh])

            # add arms 

            pyrosim.Send_Joint( name = "Torso_LeftArm" , parent= "Torso" , child = "LeftArm" , type = "revolute", position = [0.0,-c.width/2, c.z + 0.1], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="LeftArm", pos=[0.0,-c.al/2,0.0] , size=[c.aw,c.al,c.ah])

            pyrosim.Send_Joint( name = "Torso_RightArm" , parent= "Torso" , child = "RightArm" , type = "revolute", position = [0.0,c.width/2, c.z + 0.1], jointAxis='1 0 0')
            pyrosim.Send_Cube(name="RightArm", pos=[0.0,c.al/2,0.0] , size=[c.aw,c.al,c.ah])

            pyrosim.Send_Joint( name = "LeftArm_LowerLeftArm" , parent= "LeftArm" , child = "LowerLeftArm" , type = "revolute", position = [0.0,-c.al, 0.0], jointAxis='0 0 1')
            pyrosim.Send_Cube(name="LowerLeftArm", pos=[0.0,-c.al/2,0.0] , size=[c.aw,c.al,c.ah])

            pyrosim.Send_Joint( name = "RightArm_LowerRightArm" , parent= "RightArm" , child = "LowerRightArm" , type = "revolute", position = [0.0,c.al, 0.0], jointAxis='0 0 1')
            pyrosim.Send_Cube(name="LowerRightArm", pos=[0.0,c.al/2,0.0] , size=[c.aw,c.al,c.ah])

            # add 'tray'
            

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
        for currentRow in range(len(c.sensorNeurons)):
            for currentColumn in range(len(c.motorNeurons)):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + len(c.sensorNeurons) , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2,2,c.z] , size=[c.length,c.width,c.height])
        pyrosim.End()