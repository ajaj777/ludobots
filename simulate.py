from simulation import SIMULATION

# import pybullet as p
# import pybullet_data
# import time as time
# import pyrosim.pyrosim as pyrosim
# import numpy as np 
# import math
# import random
# import constants as c






# backLegSensorValues = np.zeros(c.steps)
# frontLegSensorValues = np.zeros(c.steps)


# np.save('data/fl_targetAnglesValues.npy', c.fl_targetAngles)
# np.save('data/bl_targetAnglesValues.npy', c.bl_targetAngles)

# for i in range(c.steps):
#     p.stepSimulation()
#     backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#     frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
#     pyrosim.Set_Motor_For_Joint(
#     bodyIndex = robotID,
#     jointName = b"Torso_BackLeg",
#     controlMode = p.POSITION_CONTROL,
#     targetPosition = c.bl_targetAngles[i],
#     maxForce = 40)
#     pyrosim.Set_Motor_For_Joint(
#     bodyIndex = robotID,
#     jointName = b"Torso_FrontLeg",
#     controlMode = p.POSITION_CONTROL,
#     targetPosition = c.fl_targetAngles[i],
#     maxForce = 40)
#     time.sleep(1/60)
# p.disconnect()
# np.save('data/backLegSensorValues.npy', backLegSensorValues)
# np.save('data/frontLegSensorValues.npy', frontLegSensorValues)
# #print(backLegSensorValues)

simulation = SIMULATION()
simulation.Run()