import os,sys

how_many = 10
if len(sys.argv) > 1:
    how_many = int(sys.argv[1])


for i in range(how_many):
    os.system('python3 search.py')
