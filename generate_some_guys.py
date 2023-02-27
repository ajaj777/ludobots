import os,sys

seeds = [1,2,3,4,5]
how_many = 10
if len(sys.argv) > 1:
    seed_max = int(sys.argv[1])


os.system(f'python3 search.py {seed_max}')
