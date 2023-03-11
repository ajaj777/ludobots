# Final Project (The Artist Route) 

This project was created using the Pyrosim library (https://ccappelle.github.io/pyrosim/) and pybullet. Codebase adapted from the MOOC ludobots course (https://www.reddit.com/r/ludobots/).

Video:
[ video link here ]

Gif: 

[ imgur link here? ]

## Examples of Random versus Evolved Creatures: 

## How Does This All Work?

![GenoPheno](https://user-images.githubusercontent.com/13933221/224508630-6e72d590-7f54-4ffa-b81e-36c15bab8ad5.jpg)
![Mutations](https://user-images.githubusercontent.com/13933221/224508636-bb0abfdb-9dc3-486b-a005-d2acdf830e9a.jpg)
![PHC](https://user-images.githubusercontent.com/13933221/224508640-85c10921-71ea-483e-aede-b630aab58b72.jpg)

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

```search.py``` can be used to conduct evolution. 

Usage:
```python3 search.py 5 1```

Would sequentially evolve 5 creatures optimizing for locomotion using 5 random seeds, one time. 

```python3 search.py random 7 2```

Would sequentially evolve 7 creatures optimizing for locomotion using 5 random seeds, twice. 










