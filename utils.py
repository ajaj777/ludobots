import math
import matplotlib.pyplot as plt
import time
def euclidean_distance(p,q):
            
        return math.pow((p[0]-q[0])**2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2,
                                        1/2)


def euclidean_distance2d(p,q):
        return math.pow((p[0]-q[0])**2 + (p[1] - q[1]) ** 2, 1/2)
def make_fitness_plot(uid, fitness_arrs, time, seeds=None):
        # fitness_arrs: list of np arrays (shape 1,c.numGenerations) to plot on same graph
        # seeds: list of seeds that correspond to fitness arrs. Defaults None
        plt.figure(uid)
        if len(seeds) > 1:
                title_seeds = ''.join(f'{x},' for x in seeds)[:-1]
                plt.title(f'Fitness Curves for Random Seeds {title_seeds}')
        for i,arr in enumerate(fitness_arrs):
            line = plt.plot(arr)[0]
            line.set_label(seeds[i])
        plt.legend()
        seed_str = "".join(str(x) for x in seeds)
        label = f'FitnessPlot_{time}_{seed_str}.png'
        plt.xlabel('Generations')
        plt.ylabel('Fitness (avg abs X position of links)')
        #plt.xticks(range(0,len(fitness_arrs[0])))
        plt.savefig(label)
       # plt.show()
        
