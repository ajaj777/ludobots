import sys
from parallelHillClimber import PARALLEL_HILL_CLIMBER

seed = sys.argv[1]
times = sys.argv[2]
extreme_mutation_flag = 1

phc = PARALLEL_HILL_CLIMBER(seed=seed, show_first=True, extreme_mutation_flag=1)
phc.Evolve()
phc.Show_Best()