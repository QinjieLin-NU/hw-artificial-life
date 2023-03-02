import numpy
import pybullet as p
import pybullet_data
import numpy
import os
import random
import time

import pyrosim.pyrosim as pyrosim
import ea_brain.constants as c
from env.robot import ROBOT
from env.world import WORLD

def set_seed(seedId):
  random.seed(seedId)
  numpy.random.seed(seedId)

class SIMULATION:
  def __init__(self, directOrGUI, brainID, urdfId, seedId, removeBrain=True, onlyView=False):
    if directOrGUI == 'DIRECT':
      self.physicsClient = p.connect(p.DIRECT)#DIRECT GUI
    if directOrGUI == 'GUI':
      self.physicsClient = p.connect(p.GUI)#DIRECT GUI
      p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) #Disable sidebar
      p.resetDebugVisualizerCamera(cameraDistance=1.4, cameraYaw=-69, cameraPitch=-38, cameraTargetPosition=[0.07, -0.18, -0.03]) #reser camera
    self.directOrGUI=directOrGUI
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,c.gravity)
    self.seedId = seedId
    set_seed(seedId)
    self.world = WORLD()
    self.robot = ROBOT(urdfId=urdfId, brainID=brainID, seedId=seedId, removeBrain=removeBrain)
    self.onlyView = onlyView
  
  def Run(self):
    if self.onlyView:
      input()
      exit()
    input()
    for t in range(c.length):
      # print(p.getDebugVisualizerCamera())
      if self.directOrGUI=="GUI":
        time.sleep(1/200)
      p.stepSimulation()
      self.robot.Sense(t)
      self.robot.Think()
      self.robot.Act(t)

  def __del__(self):
    p.disconnect()

  def Get_Fitness(self):
    self.robot.Get_Fitness()