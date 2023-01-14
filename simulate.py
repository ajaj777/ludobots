import pybullet as p
import pybullet_data
import time as time
import pyrosim.pyrosim as pyrosim
import numpy as np 
import math
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotID = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

steps = 10000
pyrosim.Prepare_To_Simulate(robotID)
backLegSensorValues = np.zeros(steps)
frontLegSensorValues = np.zeros(steps)

for i in range(steps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotID,
    jointName = b"Torso_BackLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = (random.random()*math.pi)-(math.pi/2),
    maxForce = 75)
    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotID,
    jointName = b"Torso_FrontLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = (random.random()*math.pi)-(math.pi/2),
    maxForce = 75)
    time.sleep(1/60)
p.disconnect()
np.save('data/backLegSensorValues.npy', backLegSensorValues)
np.save('data/frontLegSensorValues.npy', frontLegSensorValues)
#print(backLegSensorValues)

