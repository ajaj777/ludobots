import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import random
import time
from creature import *

class SOLUTION():
    def __init__(self, id, filename=None, numLinks=10):
        self.myID = id
        self.creature = RandomCreature(numLinks=numLinks)
       
       # weights created in create brain function

    def Set_ID(self, id):
        self.myID = id

    def Get_ID(self):
        return self.myID
    # def Evaluate(self, directOrGUI):
    #     self.Start_Simulation(directOrGUI)
    #     #self.Wait_For_Simulation_To_End()

    def Start_Simulation(self,directOrGUI, sync=False):
        self.Generate()
        if not sync:
            os.system(f'python3 simulate.py ' + directOrGUI +' '+ str(self.myID) + ' 2&>1'+ ' &' )
        else:
            os.system(f'python3 simulate.py ' + directOrGUI +' '+ str(self.myID) + ' 2&>1')
       
    def Wait_For_Simulation_To_End(self):
        fitnessFileName = 'fitness' + str(self.myID) + '.txt'
        timeStepsElapsed = 0
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
            timeStepsElapsed += 1.0
            if timeStepsElapsed > 100 * 120:
                print(f"killing process. waiting for fitness file: {fitnessFileName}") 
                self.fitness = -420000
                return
        with open(fitnessFileName,'r') as file:
            lines = file.readlines()
            self.fitness = float(lines[0])
       # print(self.fitness)
        os.system('rm ' + fitnessFileName)
        os.system(f'rm brain{self.myID}.nndf')

    def Mutate(self):
        randomRow = random.randint(0,self.numSensorNeurons-1)
        randomColumn = random.randint(0,self.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

    def Generate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

    def Create_Body(self):
            pyrosim.Start_URDF("body.urdf")
            
            
            # pyrosim.Send_Joint( name = joint.name, parent= joint.parent.name , child = joint.child.name , type = joint.type, position = pos, jointAxis=joint.axes[0])
            # pyrosim.Send_Cube(name=cube, pos=pos , size=[0,0,0])
            
            mp = self.creature.master_plan
            print(mp)
            curr = mp[0].parent
            pyrosim.Send_Cube(name=curr.name, pos=curr.position, size=curr.dims, color=curr.color)

            for i in range(len(mp)):
                joint = mp[i]
                pyrosim.Send_Joint(name = joint.name, parent = joint.parent.name, child=joint.child.name, type=joint.type, position=joint.position, jointAxis=joint.axis)
                pyrosim.Send_Cube(name = joint.child.name, pos=joint.child.position, size=joint.child.dims, color=joint.child.color)

            pyrosim.End()
            

    def Create_Brain(self):
        self.numSensorNeurons = self.creature.num_sensors()
        self.numMotorNeurons = len(self.creature.joints)
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        for i in range(self.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = self.creature.links[i].name)
        for i in range(self.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name = i + self.numSensorNeurons, jointName = self.creature.joints[i].name)
        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensorNeurons , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-10,-10,c.z] , size=[c.length,c.width,c.height])
        pyrosim.End()