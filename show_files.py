
import sys
import numpy as np
from solution import SOLUTION
import constants as c
import time


brain_file = f'{sys.argv[1]}.nndf'
body_file = f'{sys.argv[2]}.urdf'

soln = SOLUTION(1, brain = brain_file, body = body_file)
soln.Show()