from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        pass
        # self.parent.Evaluate("GUI")
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        # parent does worse because we want negative values
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Show_Best(self):
       # self.parent.Evaluate("GUI")
       pass
        
    def Print(self):
        
        print(f'\nParent: {self.parent.fitness} | Child: {self.child.fitness}\n')