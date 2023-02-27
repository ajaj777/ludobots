from solution import SOLUTION
import constants as c
import copy
import os
import math
from datetime import datetime
import numpy as np
import time
import random
from utils import *

class PARALLEL_HILL_CLIMBER():
    def __init__(self, uid=None, filename=None, seed=None, show_first=False,extreme_mutation_flag=0):
       # os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')
        self.seed = seed
        self.uid = uid
        self.show_first = show_first
        self.extreme_mutation_flag = extreme_mutation_flag
        if self.seed:
            random.seed(seed)
        self.fitness_data = np.zeros(c.numberOfGenerations)
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            if filename:
                self.parents[i] = SOLUTION(self.nextAvailableID,filename=filename)
                self.parents[i].first_iteration = copy.deepcopy(self.parents[i])
            else:
                self.parents[i] = SOLUTION(self.nextAvailableID)
                self.parents[i].first_iteration = copy.deepcopy(self.parents[i])
            self.nextAvailableID+=1
    def Evaluate(self, solutions):

        for item in solutions:
            
            solutions[item].Start_Simulation("DIRECT")
        for item in solutions:
            solutions[item].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)

        # record best fitness 
    def Evolve_For_One_Generation(self, curr=0):
       
        self.Record_Best_Fitness(curr)
        self.Spawn()
        self.Mutate(curr, extreme = self.extreme_mutation_flag)
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        
    def Record_Best_Fitness(self,i):
        bestFitness = 0
        for parent in self.parents:
            pf = self.parents[parent].fitness
            bestFitness = pf if pf > bestFitness else bestFitness
        self.fitness_data[i] = bestFitness

    def Spawn(self):
        self.children = {}
        for parent in self.parents:
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self, gen, extreme=0):
        for child in self.children:
            self.children[child].Mutate(gen, extreme=extreme)

    def Select(self):
        
        for parent in self.parents:
            if self.parents[parent].fitness < self.children[parent].fitness:
                
                self.parents[parent] = self.children[parent]
               

    def Show_Best(self):
        best = -math.inf
        bestParent = None
        for parent in self.parents:
            if self.parents[parent].fitness > best:
                bestParent = self.parents[parent]
                best = bestParent.fitness
        bid = bestParent.Get_ID()
        #bestParent.Create_Brain()
        #bestParent.Create_Body()
        now = str(datetime.now().strftime("%H:%M:%S"))
        
        # need to save np weights into a file
        #try:
        label = f'_{self.seed}'
        os.system(f'mv brain{bid}.nndf bestBrain{now}{label}.nndf')
       # os.system(f'rm brain*.nndf')
        np_filename = f'bestBrain{now}{label}.npy'
        urdf_filename = f'bestBody{now}{label}.urdf'
        fitness_filename = f'curve{now}{label}.npy'
        os.system(f'mv body{bid}.urdf {urdf_filename}')
        np.save(fitness_filename, self.fitness_data)
        np.save(np_filename, bestParent.weights)
        print("best fitness found:", bestParent.fitness)
        #bestParent.Start_Simulation('GUI')
        os.system(f'python3 show.py 0 {now}{label}')
        os.system(f'python3 show_files.py brain{bestParent.first_iteration.Get_ID()} body{bestParent.first_iteration.Get_ID()}')
        # except Exception as e:
        #     print(f"Couldn't write some files. {e}")
        #     return
        #os.system('rm brain*')
        #os.system('rm body*')
        #os.system('rm fitness*')
        self.Plot(time=now)
       # print(f"Body and brain ID: {bid}")
    def Plot(self, time=0):
        make_fitness_plot(self.uid, [self.fitness_data], time=time, seeds = [self.seed])
        
    def Print(self):
        for parent in self.parents:
            print(f'\nParent: {self.parents[parent].fitness} | Child: {self.children[parent].fitness}\n')