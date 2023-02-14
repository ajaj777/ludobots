import math
import random
from link import *
from joint import *

class RandomCreature():
    def __init__(self, dimension=1, numLinks=5, linkTypes=['rectangle']):
        self.dimension = dimension
        self.numLinks = numLinks
        self.linkTypes = linkTypes
        self.generate_links()
        self.generate_joints()

    def generate_links(self):
        self.links = []
        self.maxZ = 0
        self.numSensors = 0
        for i in range(self.numLinks):
            currType = random.choice(self.linkTypes)
            if currType == 'rectangle':
                curr = RectangleLink(f'Link{i}',random=1)
                
                self.maxZ = curr.height if curr.height > self.maxZ else self.maxZ

                self.links.append(curr)
                if curr.sensor == 1:
                    self.numSensors += 1

    def generate_joints(self):
        # randomly choose # of axes of rotation, and then:
        # choose random axis for each revolute joint
        self.numJoints = 0
        jointAxes = ['1 0 0', '0 1 0', '0 0 1']
        if self.dimension == 1:
            self.joints = []
            for i in range(self.numLinks-1):
                df = random.randint(1,3)
                self.numJoints += df
                randAxes = random.sample(jointAxes,k=df)
                self.joints.append(RevoluteJoint(parent=self.links[i], child=self.links[i+1], axes=randAxes))

    def num_sensors(self):
        return self.numSensors

    def num_joints(self):
        return self.numJoints




