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
        self.received_joints = []
        
class RectangleLink(Link):
    def __init__(self,name,random,scale=[0.2,1], position=None, s=None, **args):
        Link.__init__(self,name, random=random, scale=scale, position=position)
        if self.random:
            self.generate(sensor=s)
        else:
            # remove 'self' in front of width,length,height
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

    def set_sensor(self, val):
        self.sensor = val
        if self.sensor == 1:
            self.color = 'green'
        else:
            self.color = 'blue'

    def generate(self, sensor=None):
        dimensions = np.random.rand(1,3) 
        #print(dimensions)
        self.length = dimensions[0][0] * (self.scale[1]-self.scale[0]) + self.scale[0]
        self.width = dimensions[0][1] * (self.scale[1]-self.scale[0]) + self.scale[0]
        self.height = dimensions[0][2] * (self.scale[1]-self.scale[0]) + self.scale[0]
        
        self.dims = [self.length, self.width, self.height]
        if sensor is None:
            self.sensor = random.randint(0,1)
        else:
            self.sensor = sensor
            
        if self.sensor == 1:
            self.color = 'green'
        else:
            self.color = 'blue'
       

    