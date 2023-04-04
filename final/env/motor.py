import numpy
import pybullet as p

import ea_brain.constants as c
import pyrosim.pyrosim as pyrosim

class MOTOR:
  def __init__(self, jointName):
    self.jointName = jointName
    # self.Prepare_To_Act()
    self.max_force = c.max_force

  def Set_Value(self, desiredAngle, robotId):
    pyrosim.Set_Motor_For_Joint(
      bodyIndex = robotId,
      jointName = self.jointName,
      controlMode = p.POSITION_CONTROL,
      targetPosition = desiredAngle,
      maxForce = self.max_force)
  