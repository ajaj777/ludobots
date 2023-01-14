from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time as time

class SIMULATION:
    def __init__(self):
        
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT()
        pyrosim.Prepare_To_Simulate(self.robot.robotID)

    def Run(self):
        for i in range(c.steps):
            print(i)
            p.stepSimulation()
            time.sleep(1/120)
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # pyrosim.Set_Motor_For_Joint(
            # bodyIndex = robotID,
            # jointName = b"Torso_BackLeg",
            # controlMode = p.POSITION_CONTROL,
            # targetPosition = c.bl_targetAngles[i],
            # maxForce = 40)
            # pyrosim.Set_Motor_For_Joint(
            # bodyIndex = robotID,
            # jointName = b"Torso_FrontLeg",
            # controlMode = p.POSITION_CONTROL,
            # targetPosition = c.fl_targetAngles[i],
            # maxForce = 40)
            # time.sleep(1/60)
        #p.disconnect()
        
    def __del__(self):

        p.disconnect()