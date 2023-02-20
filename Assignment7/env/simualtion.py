import numpy
import pybullet as p
import pybullet_data
import time

import pyrosim.pyrosim as pyrosim
import ea.constants as c
from env.robot import ROBOT
from env.world import WORLD

class SIMULATION:
  def __init__(self, directOrGUI, brainID, removeBrain=True, onlyView=False):
    if directOrGUI == 'DIRECT':
      self.physicsClient = p.connect(p.DIRECT)#DIRECT GUI
    if directOrGUI == 'GUI':
      self.physicsClient = p.connect(p.GUI)#DIRECT GUI
      p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) #Disable sidebar
      p.resetDebugVisualizerCamera(cameraDistance=4.0, cameraYaw=-60, cameraPitch=-50, cameraTargetPosition=[1.8, -3.1, 1.4]) #reser camera
    self.directOrGUI=directOrGUI
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,c.gravity)
    self.world = WORLD()
    self.robot = ROBOT(brainID=brainID,removeBrain=removeBrain)
    self.onlyView = onlyView
  
  def Run(self):
    if self.onlyView:
      input()
      exit()
    for t in range(c.length):
      # print(p.getDebugVisualizerCamera())
      if self.directOrGUI=="GUI":
        time.sleep(1/800)
      p.stepSimulation()
      self.robot.Sense(t)
      self.robot.Think()
      self.robot.Act(t)

  def __del__(self):
    p.disconnect()

  def Get_Fitness(self):
    self.robot.Get_Fitness()