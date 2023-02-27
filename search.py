import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import sys
from utils import *
import time
from datetime import datetime

#print(sys.argv)
if len(sys.argv) > 1:
    seed_max = int(sys.argv[1])
    times = int(sys.argv[2])
    #times = int(sys.argv[2])
    arrs = []
    seeds = [x for x in range(1,seed_max+1)]
    for j in range(times):
        for seed in seeds:
            phc = PARALLEL_HILL_CLIMBER(seed=seed)
            phc.Evolve()
            phc.Show_Best()
            arrs.append(phc.fitness_data)
        now = str(datetime.now().strftime("%H:%M:%S"))
        uid = seeds[-1]+1+j
        make_fitness_plot(uid, arrs, now, seeds)
else:
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()

phc.Plot()
# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

