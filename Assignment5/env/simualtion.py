import numpy
import pybullet as p
import pybullet_data
import time

import pyrosim.pyrosim as pyrosim
import ea.constants as c
from env.robot import ROBOT
from env.world import WORLD

class SIMULATION:
  def __init__(self, directOrGUI, brainID):
    if directOrGUI == 'DIRECT':
      self.physicsClient = p.connect(p.DIRECT)#DIRECT GUI
    if directOrGUI == 'GUI':
      self.physicsClient = p.connect(p.GUI)#DIRECT GUI
    self.directOrGUI=directOrGUI
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,c.gravity)
    self.world = WORLD()
    self.robot = ROBOT(brainID=brainID)
  
  def Run(self):
    for t in range(c.length):
      # print(f"loop: {t}")
      if self.directOrGUI:
        time.sleep(1/1000)
      p.stepSimulation()
      self.robot.Sense(t)

      #16
      self.robot.Think()

      self.robot.Act(t)
    self.robot.Save_Values()

  def __del__(self):
    p.disconnect()

  def Get_Fitness(self):
    self.robot.Get_Fitness()