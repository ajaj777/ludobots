from solution import SOLUTION
import constants as c
import copy
import os
import math
from datetime import datetime

class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID+=1
        
    def Evaluate(self, solutions):
        for item in solutions:
            solutions[item].Start_Simulation("DIRECT")
        for item in solutions:
            solutions[item].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        
        
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
        bestParent.Start_Simulation('GUI')
        
        
    def Print(self):
        for parent in self.parents:
            print(f'\nParent: {self.parents[parent].fitness} | Child: {self.children[parent].fitness}\n')