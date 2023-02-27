import sys
import numpy as np
from solution import SOLUTION
import constants as c
import time
num = 3
links = 8
c.steps = 5000
random = int(sys.argv[1])

def show(filename):
    # rand_soln = SOLUTION(0)
    # rand_soln.Start_Simulation("GUI")
    # time.sleep(10)
    soln = SOLUTION(1, filename=filename)
    soln.Start_Simulation("GUI")

def show_random(num, links):
    for i in range(num):
        soln = SOLUTION(i,numLinks=links)
        soln.Start_Simulation("GUI",sync=True)

if random:
    if len(sys.argv) > 2:
        num = int(sys.argv[2])
    if len(sys.argv) > 3:
        links = int(sys.argv[3])
    show_random(num, links)

else:

    timestamp = sys.argv[2]
    brain_file = f'bestBrain{timestamp}.nndf'
    body_file = f'bestBody{timestamp}.urdf'
    
    soln = SOLUTION(1, brain = brain_file, body = body_file)
    soln.Show()