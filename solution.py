import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import random
import time
from creature import *
from simulation import SIMULATION

class SOLUTION():
    def __init__(self, id, brain=None, body=None, numLinks=8):
        self.myID = id
        self.creature = RandomCreature(uid = self.myID, numLinks=numLinks)
        self.brain = brain
        self.body = body

       # weights created in create brain function

    def Show(self):
        g = SIMULATION("GUI",self.myID, brain=self.brain, body=self.body)
        g.Run()
        g.Print_Fitness()

    def Set_ID(self, id):
        self.myID = id
        self.creature.uid = self.myID

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
            if timeStepsElapsed > 100 * 10:
                print(f"killing process. waiting for fitness file: {fitnessFileName}") 
                self.fitness = -420000
                return
        with open(fitnessFileName,'r') as file:
            lines = file.readlines()
            self.fitness = float(lines[0])
       # print(self.fitness)
        os.system('rm ' + fitnessFileName)
       #os.system(f'rm brain{self.myID}.nndf')

    def Mutate(self, gen, extreme=0):
        # mutate brain
        randomRow = random.randint(0,self.numSensorNeurons-1)
        randomColumn = random.randint(0,self.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 - 1
        # mutate body plan
        if gen < 0.5 * c.numberOfGenerations:
            self.creature.small_mutate(extreme=extreme)

    def Generate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

    def Create_Body(self):
            pyrosim.Start_URDF(f"body{self.myID}.urdf")
            
            
            # pyrosim.Send_Joint( name = joint.name, parent= joint.parent.name , child = joint.child.name , type = joint.type, position = pos, jointAxis=joint.axes[0])
            # pyrosim.Send_Cube(name=cube, pos=pos , size=[0,0,0])
            
            mp = self.creature.master_plan
            #print(mp)
            curr = mp[0].parent
            link_dict = {}
            pyrosim.Send_Cube(name=curr.name, pos=curr.position, size=curr.dims, color=curr.color)
            link_dict[curr.name] = True
            for i in range(len(mp)):
                joint = mp[i]
                pyrosim.Send_Joint(name = joint.name, parent = joint.parent.name, child=joint.child.name, type=joint.type, position=joint.position, jointAxis=joint.axis)
                if joint.child.name not in link_dict:
                    pyrosim.Send_Cube(name = joint.child.name, pos=joint.child.position, size=joint.child.dims, color=joint.child.color)
                    link_dict[joint.child.name] = True
                if joint.parent.name not in link_dict:
                    pyrosim.Send_Cube(name = joint.parent.name, pos=joint.parent.position, size=joint.parent.dims, color=joint.parent.color)
                    link_dict[joint.parent.name] = True
                

            pyrosim.End()
            

    def Create_Brain(self):

        sensor_list = [x for x in self.creature.links if x.sensor == 1]
       # print(sensor_list)
        self.numSensorNeurons = len(sensor_list)
        if self.numSensorNeurons == 0:
            self.creature.links[0].set_sensor(1)
            self.numSensorNeurons = 1
            sensor_list = [self.creature.links[0]]
        self.numMotorNeurons = len(self.creature.joints)
        # CANNOT CALL CREATE BRAIN AGAIN! THIS IS WHERE IT RANDOMLY ASSIGNS WEIGHTS
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        for i, link in enumerate(sensor_list):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = link.name)
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