# Assignment 6: 1D Snakes

This project was created using the Pyrosim library (https://ccappelle.github.io/pyrosim/) and pybullet. Codebase adapted from the MOOC ludobots course (https://www.reddit.com/r/ludobots/).

Video:
https://youtu.be/8WBtRqn6ARE

Sample images of program output:

A snake with 5 links.\
<img width="521" alt="Screen Shot 2023-02-13 at 10 47 33 PM" src="https://user-images.githubusercontent.com/13933221/218642113-62280953-880b-45ac-b4f7-a75d4a8fb0e6.png"> \
\
A snake with 25 links.\
<img width="470" alt="Screen Shot 2023-02-13 at 10 48 20 PM" src="https://user-images.githubusercontent.com/13933221/218642150-d5ac13a0-2539-4022-98ad-1de524b3436e.png">\
\
A snake with 50 links.\
<img width="334" alt="Screen Shot 2023-02-13 at 10 48 48 PM" src="https://user-images.githubusercontent.com/13933221/218642174-91f30afc-4b5a-4306-b784-cc7657ab1415.png">\
\
1D snakes are generated as chains of connected rectangular links with random dimensions (length, width, height) in the interval [0,1). Each link is randomly chosen to possess a sensor or not. Those that have sensors are colored green and those that lack sensors are colored blue. Each link is randomly connected to its neighbor(s) with a joint that has randomly selected axes of revolution and randomly selected degrees of freedom. For example, one joint might revolve around the x-axis only (axes=['1 0 0']), while another may revolve around the y- and z-axes (axes=['0 1 0', '0 1 1']). 

The snake moves according to a fully connected 2-layer neural network consisting of sensor neurons and motor neurons, initially assigned random weights. If desired, the snakes can be evolved according to a specified fitness function using a parallel hill climber method. (Refer to 'waiters' branch for more details and for the necessary code modifications.) 

Commands to replicate the content presented in the video:

```python3 show.py random [number of creatures] [OPTIONAL: number of links per creature (default=5)]```

e.g.\
```python3 show.py random 5```

Would sequentially simulate 5 randomly generated 1D snakes each with 5 links.

```python3 show.py random 3 10```

Would sequentially simulate 3 randomly generated 1D snakes each with 10 links.



