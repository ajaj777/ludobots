import numpy as np
import sys
import time
from utils import *

file = sys.argv[1]

np_arr = np.load(f'curve{file}.npy')
print(np_arr)
make_fitness_plot([np_arr], time=file.split('_')[0],seeds=[0])