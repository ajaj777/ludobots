import numpy as np
import random

class Link():
    def __init__(self, name, random=1):
        self.name = name
        self.random = random

class RectangleLink(Link):
    def __init__(self,name,random,**args):
        Link.__init__(self,name, random=random)
        if self.random:
            self.generate()
        else:
            self.length = args['length']
            self.width = args['width']
            self.height = args['height']
            self.color = args['color']
            self.sensor = args['sensor']

    def generate(self):
        dimensions = np.random.rand(1,3)
        self.length = dimensions[0][0]
        self.width = dimensions[0][1]
        self.height = dimensions[0][2]
        self.sensor = random.randint(0,1)
        self.dims = [self.length, self.width, self.height]
        if self.sensor == 1:
            self.color = 'green'
        else:
            self.color = 'blue'