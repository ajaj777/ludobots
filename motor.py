import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.phaseOffset = c.phaseOffset
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
        pass
