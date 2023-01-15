import constants as c
import numpy as np 
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkname):
        self.linkname = linkname
        self.values = np.zeros(c.steps)
        
    def Get_Value(self,t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkname)
        if t == c.steps - 1:
            print(self.values)