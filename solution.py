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
            
            links = self.creature.links
            joints = self.creature.joints
            self.motorNeuronList = []


            def next_pos(direction, prev_direction, link_dims):
                d = direction
                pd = prev_direction
                ld = link_dims
                return [(pd[0]+d[0])*ld[0]/2,
                        (pd[1]+d[1])*ld[1]/2,
                        (pd[2]+d[2])*ld[2]/2]

            def add_joint(joint, pos):
                if len(joint.axes) == 1:
                    pyrosim.Send_Joint( name = joint.name, parent= joint.parent.name , child = joint.child.name , type = joint.type, position = pos, jointAxis=joint.axes[0])
                    self.motorNeuronList.append(joint.name)
                else:
                    temp_cubes = [f'{joint.parent.name}{joint.child.name}{x}' for x in range(len(joint.axes)-1)]
                    for cube in temp_cubes:
                         pyrosim.Send_Cube(name=cube, pos=pos , size=[0,0,0])

                    cube_chain = []
                    cube_chain.append(joint.parent.name)
                    for cube in temp_cubes:
                        cube_chain.append(cube)
                    cube_chain.append(joint.child.name)

                    for i in range(len(cube_chain)-1):
                        jName = f'{cube_chain[i]}_{cube_chain[i+1]}'
                        self.motorNeuronList.append(jName)
                        currPos = None
                        if i==0:
                            currPos = pos
                        else:
                            currPos = [0,0,0]
                        pyrosim.Send_Joint(name = jName, parent= cube_chain[i] , child = cube_chain[i+1] , type = joint.type, position = currPos, jointAxis=joint.axes[i])

           

            dirs = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]

            pyrosim.Send_Cube(name=links[0].name, pos=[c.x,c.y,self.creature.startZ] , size=links[0].dims, color=links[0].color)
            d = dirs[random.randint(0,len(dirs)-1)]
            add_joint(joints[0], [ c.x + d[0] * links[0].dims[0]/2 ,c.y + d[1]*links[0].dims[1]/2, self.creature.startZ + d[2]*links[0].dims[2]/2])

            prev_dir = d
            for i in range(1,len(joints)):
                # choose among six faces for next link
                
                # now these are all relative
                pyrosim.Send_Cube(name=links[i].name, pos=[d[0]*links[i].dims[0]/2,d[1]*links[i].dims[1]/2,d[2]*links[i].dims[2]/2] , size=links[i].dims, color=links[i].color)
                d = dirs[random.randint(0,len(dirs)-1)]
                curr_pos = next_pos(d,prev_dir,links[i].dims)
                prev_dir = d
                add_joint(joints[i], curr_pos)
                
                
                
            pyrosim.Send_Cube(name=links[-1].name, pos=[d[0]*links[-1].dims[0]/2,d[1]*links[-1].dims[1]/2,d[2]*links[-1].dims[2]/2] , size=links[-1].dims, color=links[-1].color)

            pyrosim.End()
            

    def Create_Brain(self):
        self.numSensorNeurons = self.creature.num_sensors()
        self.numMotorNeurons = len(self.motorNeuronList)
        self.weights = np.random.rand(self.numSensorNeurons,self.numMotorNeurons) * 2 - 1

        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        for i in range(self.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = self.creature.links[i].name)
        for i in range(self.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name = i + self.numSensorNeurons, jointName = self.motorNeuronList[i])
        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensorNeurons , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-10,-10,c.z] , size=[c.length,c.width,c.height])
        pyrosim.End()