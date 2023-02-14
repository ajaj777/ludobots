import math
import random
from link import *

class RandomCreature():
    def __init__(self, dimension=1, numLinks=5, linkTypes=['rectangle']):
        self.dimension = dimension
        self.numLinks = numLinks
        self.linkTypes = linkTypes
        self.generate_links()

    def generate_links(self):
        self.links = []
        for i in range(self.numLinks):
            currType = random.choice(self.linkTypes)
            if currType == 'rectangle':
                self.links.append(RectangleLink())

    def generate_joints(self):
        # randomly choose # of axes of rotation, and then:
        # choose random axis for each revolute joint
        jointAxes = ['1 0 0', '0 1 0', '0 0 1']
        self.joints = []
        for i in range(self.numLinks-1):
            df = math.randint(1,3)
            randAxes = random.sample(jointAxes,k=df)
            self.joints.append(randAxes)


    def build_urdf(self):
        pass


