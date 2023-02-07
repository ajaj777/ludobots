import sys
import numpy as np
from solution import SOLUTION
import constants as c
import time

filename = sys.argv[1]
steps = c.steps
if len(sys.argv) > 2:
    steps = sys.argv[2]

def show(filename,steps):
    rand_soln = SOLUTION(0)
    rand_soln.Start_Simulation("GUI")
    time.sleep(10)
    soln = SOLUTION(1, filename=filename)
    soln.Start_Simulation("GUI")


show(filename,steps)