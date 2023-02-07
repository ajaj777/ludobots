import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import sys

print(sys.argv)
if len(sys.argv) > 1:
    print("Using a file.")
    global filename
    filename = sys.argv[1]
    phc = PARALLEL_HILL_CLIMBER(filename=filename)
    phc.Evolve()
    phc.Show_Best()
else:
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()

# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

