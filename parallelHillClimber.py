from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        os.system('rm brain*.nndf')
        os.system('rm fitness*.nndf')

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID+=1
        
    def Evaluate(self, solutions):
        for parent in solutions:
            self.parents[parent].Start_Simulation("GUI")
        for parent in solutions:
            self.parents[parent].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        exit()
        # self.Print()
        # self.Select()
        

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
        # parent does worse because we want negative values
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Show_Best(self):
       # self.parent.Evaluate("GUI")
       pass
        
    def Print(self):
        
        print(f'\nParent: {self.parent.fitness} | Child: {self.child.fitness}\n')