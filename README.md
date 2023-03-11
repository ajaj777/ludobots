# Final Project (The Artist Route) 

This project was created using the Pyrosim library (https://ccappelle.github.io/pyrosim/) and pybullet. Codebase adapted from the MOOC ludobots course (https://www.reddit.com/r/ludobots/).

Video: \
https://youtu.be/wO4xQoxgRGM

Gif: 

[ imgur link here? ]

## Examples of Random versus Evolved Creatures: 
 
 This random creature was very good at moving in circles, but it hardly displaced itself from its starting position.<br>
 <p align='center'>
 <img width="211" alt="Screen Shot 2023-03-11 at 5 07 32 PM" src="https://user-images.githubusercontent.com/13933221/224515385-aa0193fd-5603-4ccd-bd08-040da1a84416.png"><br></p>
 
 This random creature lacks an organized structure and struggles to move.<br>
 <p align='center'>
<img width="337" alt="Screen Shot 2023-03-11 at 5 08 13 PM" src="https://user-images.githubusercontent.com/13933221/224515404-01e72d6f-47c7-4e07-aeb8-f6c9def63e5b.png"><br>
</p?

One evolved creature learned to move by 'flapping' its left and right arms, purposefully setting itself off balance so that it would fall forward. As it fell, it would flap again, and in this way consistently travel<br>
 <p align='center'>
<img width="288" alt="Screen Shot 2023-03-11 at 5 12 01 PM" src="https://user-images.githubusercontent.com/13933221/224515522-9c4f5b1a-5bbd-4b27-a72e-7875c039d11e.png"><br>
</p>

The following creature was my favorite product of evolution. Despite its miniature size and inherent disadvantage (since larger creatures have an inherent advantage in our fitness function), the 'jumping' gait this creature evolved allowed it to outperform its peers (see end of Youtube video linked above).<br>
 <p align='center'>
<img width="172" alt="Screen Shot 2023-03-11 at 5 09 52 PM" src="https://user-images.githubusercontent.com/13933221/224515459-317347e2-4a5d-41ac-9b2d-b9397df45ca2.png">
</p>

## How Does This All Work?
We use a direct encoding that is a one-to-one map from genotype (genes) to phenotype (physical gene expression). We store a list of 'links' and a list of joints representing how the links are connected. We also track the brain of each creature, which is a fully connected neural network linking sensor neurons and motor neurons. (See 'locomotion' branch for more details.)
<p align='center'>
<img width="450" alt="Screen Shot 2023-03-11 at 1 49 20 PM" src="https://user-images.githubusercontent.com/13933221/224508701-1c2b1a76-7085-4fe2-a8ad-d766b2d3b1c9.png">
<br>
 </p>
We evolve for 100 generations. During earlier generations, we make more dramatic alterations such as changing the number of links or their arrangement. As evolution reaches its later generations, we make smaller tweaks, such as altering the size of links and the synpactic weights between neurons.
<p align='center'>
<img width="500" alt="Screen Shot 2023-03-11 at 1 50 49 PM" src="https://user-images.githubusercontent.com/13933221/224508780-6120e2e4-c74c-4756-b242-f2f6533dda22.png">
<br>
 </p>
Our method of evolution is a parallel hill climber. A population starting with 100 randomly generated creatures is maintained. At each generation, parents give rise to one child each. If the child performs better, it takes the place of its parent. This lets us guarantee that the quality of creatures only improves across evolution. At the end, we choose the best creature we have found so far, and crown it winner. 
<p align='center'>
<img width="700" alt="Screen Shot 2023-03-11 at 1 51 13 PM" src="https://user-images.githubusercontent.com/13933221/224508802-19237243-f8ca-450c-ab91-cdfa5513d47a.png">
<br>
 </p>
Our experiment conducted this evolution across 10 different random seeds, for 100 generations each, with 10 population members. This gives us a total of 10*100*10 = 10,000 simulations. Below is a graph denoting the quality (fitness) of the best creature at the current generation. We evolved creatures for locomotion along the x-axis.
<p align='center'>
 <img width="635" alt="Screen Shot 2023-03-11 at 2 05 21 PM" src="https://user-images.githubusercontent.com/13933221/224509340-cf4d445d-dbe8-4e0e-95d3-57cb59afba69.png">
</p>

### Commands to Visualize Creatures 

```show.py``` can be used to visualize creatures, both random and evolved.

View **random** creatures:

```python3 show.py 1 [QUANTITY (default 1)] [NUM_LINKS? (default random)]```

- Quantity: how many to visualize in sequence?
- Num_links: random number of links for each creature (default) or a particular number?

To simply show a random creature with a random number of links, run:
```python3 show.py 1```

View **evolved** creatures:

```python3 show.py 0 [UID]```

-UID: Timestamp with seed appended. E.g. ```python3 show.py 1 23:04:58_1``` would run ```bestBrain23:04:58_1``` with its associated body ```bestBody23:04:58_1``` (which used a random seed of ```1```).


**Conduct evolution**:

```search.py``` can be used to conduct evolution. **constants.py is where you can change population size, generations, and number of steps per sim**

Usage:
```python3 search.py 5 1```

Would sequentially evolve 5 creatures optimizing for locomotion using 5 random seeds, one time. 

```python3 search.py random 7 2```

Would sequentially evolve 7 creatures optimizing for locomotion using 5 random seeds, twice. 










