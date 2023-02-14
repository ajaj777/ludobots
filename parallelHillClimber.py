from solution import SOLUTION
import constants as c
import copy
import os
import math
from datetime import datetime
import numpy as np

class PARALLEL_HILL_CLIMBER():
    def __init__(self, filename=None):
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            if filename:
                self.parents[i] = SOLUTION(self.nextAvailableID,filename=filename)
            else:
                self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID+=1
        
    def Evaluate(self, solutions):
        for item in solutions:
            solutions[item].Start_Simulation("DIRECT")
        for item in solutions:
            solutions[item].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        low = -math.inf
        fitness_list = []
        positives = []
        for parent in self.parents:
            fitness_list.append(self.parents[parent].fitness)
            positives = [x for x in fitness_list if x > 0]
        
        attempts = 0
        while len(positives) < 3:
            print("\n\nRegenerating first generation...\n\n")
            os.system('rm brain*.nndf')
            os.system('rm fitness*.txt')
            print("Positive fitnesses: ", positives)
            reg_count = 0
            for parent in self.parents:
                
                if self.parents[parent].fitness < 0:
                    self.parents[parent] = SOLUTION(self.nextAvailableID)
                    self.nextAvailableID += 1
                    reg_count += 1

            print(f"Regen {reg_count} parents.")
            self.Evaluate(self.parents)
            fitness_list = []
            for parent in self.parents:
                fitness_list.append(self.parents[parent].fitness)
                positives = [x for x in fitness_list if x > 0]

            attempts += 1
        
        final = {}
        for parent in self.parents:
            if self.parents[parent].fitness > 0:
                final[parent] = self.parents[parent]

        self.parents = final
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        

    def Spawn(self):
        self.children = {}
        for parent in self.parents:
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()

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
        bestParent.Create_Brain()
        now = str(datetime.now().strftime("%H:%M:%S"))
        

        os.system(f'mv brain{bid}.nndf bestBrain{now}.nndf')
        os.system(f'rm brain*.nndf')
        # need to save np weights into a file
        good_threshold = 1
        label = 'normal'
        if bestParent.fitness > good_threshold:
            label = 'good'

        if c.z_threshold == 1.5:
            label = 'OneFive'

        np_filename = f'bestWeights{now}_{label}.npy'
        np.save(np_filename, bestParent.weights)
        bestParent.Start_Simulation('GUI')
        
        
    def Print(self):
        for parent in self.parents:
            print(f'\nParent: {self.parents[parent].fitness} | Child: {self.children[parent].fitness}\n')