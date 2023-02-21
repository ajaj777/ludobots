import numpy as np
import random

class Link():
    def __init__(self, name, random=1, scale=[0.3,0.3], position=None):
        self.name = name
        self.random = random
        self.scale = scale
        self.position = position
        self.prev_direction = None
        self.abs_pos = None

class RectangleLink(Link):
    def __init__(self,name,random,scale=[0.2,1], position=None, **args):
        Link.__init__(self,name, random=random, scale=scale, position=position)
        if self.random:
            self.generate()
        else:
            self.width = args['width']
            self.length = args['length']
            self.height = args['height']
            self.sensor = args['sensor']
            self.dims = [self.length, self.width, self.height]
            if self.sensor == 1:
                self.color = 'green'
            else:
                self.color = 'blue'
        dirs = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        self.open_faces = dirs

    def generate(self):
        dimensions = np.random.rand(1,3) 
        print(dimensions)
        self.length = dimensions[0][0] * (self.scale[1]-self.scale[0]) + self.scale[0]
        self.width = dimensions[0][1] * (self.scale[1]-self.scale[0]) + self.scale[0]
        self.height = dimensions[0][2] * (self.scale[1]-self.scale[0]) + self.scale[0]
        self.sensor = random.randint(0,1)
        self.dims = [self.length, self.width, self.height]
        print(self.dims)
        if self.sensor == 1:
            self.color = 'green'
        else:
            self.color = 'blue'