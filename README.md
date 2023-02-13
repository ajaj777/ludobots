# ludobots
# ludobots

Assignment 5: (LOCATED IN 'WAITERS' BRANCH)

I created a humanoid, bipedal creature and randomly evolved it to gauge what types of locomotion would allow it to maintain 
an upright posture while also traveling. The body of the creature contains a torso, two arms, each consisting of two components (where the upper component can rotate along two axes), and two legs each consisting of two components and 'feet'. 

My highest priority goal was to ensure that the final, evolved result remained upright (whether on its legs or on its legs while also using its arms as support) for as long as possible, and then, all else equal, to favor the creatures that also moved along the x-axis the most. (I can later generalize this to something like 'most movement towards the goal', whatever the goal ends up being). 

Thus, my fitness function works as follows:

I set a 'z_threshold'. Any robot whose torso, at *any* step of the simulation falls below 'z_threshold,' is assigned a fitness value of -100. (Could be replaced with any other very negative number that nothing else would approach.) Then, before I begin 'evolving,' any of the creatures, I continually regenerate the starting parents until at least three of them meet this 'z_threshold'. This is so that I don't waste time evolving creatures whose starting configurations are so distant from my goal that they will never be able to stand upright.

Once I have at least three creatures that always remain above this specified z value, (I use the value 1.2 because that is roughly the height of the 'waist' of the robot), I apply the following fitness function:

fitness = (z_mean)^5 * (x_distance_traveled * 0.1)

where 'z_mean' is the average z_value across all simulation steps of the robot's torso, and 'x_distance_traveled' is the total *absolute* value of the ending X coordinate value of the robot's torso. 

Fascinatingly, z_thresholds set too high result in it being nearly impossible to evolve a robot to adopt natural, bipedal movement. However, setting to 1.2 (other values were also tested in this neighborhood) seems to be generous enough to allow robots to evolve in a reasonable amount of computation (though still taking ~30+ minutes), while also somewhat satisfying the goal of 'remain upright' and 'travel as far as possible'. The final evolved creature from my simulations relied heavily on its arms (sort of like a gorilla) to move, rather than walking as a human might. 

HOW TO REPLICATE:

python3 show.py bestWeights23:36:15_normal

This command will first run a random, first-gen simulation, followed by the final evolved form. 

python3 search.py

This command will redo evolution. (Be aware, it carries out the process described above and will take over 30 minutes).
