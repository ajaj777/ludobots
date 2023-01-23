from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time as time
import os

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.solutionID = solutionID
        self.directOrGUI = directOrGUI
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        #zoom out camera view
        p.resetDebugVisualizerCamera(cameraDistance = 20, cameraYaw = 0.0, cameraPitch = -45.0, cameraTargetPosition=[0,0,0])
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        # replace single robot with swarm of robots
        self.swarm = {}
        self.total_bots = c.numBots[0] * c.numBots[1]
        for bodyIndex in range(self.total_bots):
            self.swarm[bodyIndex] = ROBOT(self.solutionID,bodyIndex)
        #os.system(f'rm brain{self.solutionID}.nndf')

        #pyrosim.Prepare_To_Simulate(self.robot.robotID)

    def Run(self):
        #print("REACHED RUN")
        #exit()

        for i in range(c.steps):
            p.stepSimulation()
            for robot in self.swarm:
                self.swarm[robot].Sense(i)
                self.swarm[robot].Think()
                self.swarm[robot].Act(i)
            
            if self.directOrGUI != "DIRECT":
                time.sleep(1/240)
            #time.sleep(1/240)

    def Get_Fitness(self):
        # modify to maximize number of octapods that escape certain x/y box (i.e. where the enclosure walls are)
        # this is where a file is written to.
        fitness = 0.0
        for robot in self.swarm:
            fitness += self.swarm[robot].Get_Fitness()

        with open(f'tmp{self.solutionID}.txt','w') as file:
            file.write(str(fitness))

        os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')

    def __del__(self):

        p.disconnect()