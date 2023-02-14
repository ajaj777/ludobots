import sys
import numpy as np
from solution import SOLUTION
import constants as c
import time

filename = sys.argv[1]
num = 1
links = 5
if len(sys.argv) > 2:
    num = int(sys.argv[2])
if len(sys.argv) > 3:
    links = int(sys.argv[3])

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

if filename == 'random':
    show_random(num,links)
else:
    show(filename)