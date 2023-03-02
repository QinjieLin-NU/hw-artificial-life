import os
import pybullet as p

import ea_brain.constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from env.motor import MOTOR
from env.sensor import SENSOR

class ROBOT:
  def __init__(self, urdfId, brainID, seedId, removeBrain=True):
    self.sensors = dict()
    self.motors = dict()
    self.seedId = seedId
    with open(f"./data/seed{self.seedId}/body{urdfId}/min_depth.txt", "r") as f:
      self.robotPosZ = -1*float(f.read())
    self.robotId = p.loadURDF(f"./data/seed{self.seedId}/body{urdfId}/body.urdf", basePosition=[0,0,self.robotPosZ])
    pyrosim.Prepare_To_Simulate(self.robotId)
    self.Prepare_To_Sense()
    self.Prepare_To_Act()
    self.solutionID = brainID
    self.urdfId = urdfId
    self.nn = NEURAL_NETWORK(f"./data/seed{self.seedId}/body{urdfId}/brain{brainID}.nndf")
    if removeBrain:
      os.system(f"rm ./data/seed{self.seedId}/body{urdfId}/brain{brainID}.nndf") #line67

  def Prepare_To_Sense(self):
    self.sensors = dict()
    for linkName in pyrosim.linkNamesToIndices:
      self.sensors[linkName] = SENSOR(linkName)
  
  def Sense(self,timestep):
    for linkName in self.sensors:
      self.sensors[linkName].Get_Value(timestep)

  def Prepare_To_Act(self):
    self.motors = dict()
    for jointName in pyrosim.jointNamesToIndices:
      self.motors[jointName] = MOTOR(jointName)

  def Act(self, timestep):
    for neuronName in self.nn.Get_Neuron_Names():
      if self.nn.Is_Motor_Neuron(neuronName):
        jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
        desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
        self.motors[jointName].Set_Value(desiredAngle, self.robotId)

  def Save_Values(self):
    for linkName in self.sensors:
      self.sensors[linkName].Save_Values()
  
  def Think(self):
    self.nn.Update()
    # self.nn.Print()

  def Get_Fitness(self):
    stateOfLinkZero = p.getLinkState(self.robotId,0)
    positionOfLinkZero = stateOfLinkZero[0]
    xCoordinateOfLinkZero = positionOfLinkZero[0]
    zCoordinateOfLinkZero = positionOfLinkZero[2]
    #important
    with open(f"./data/seed{self.seedId}/body{self.urdfId}/tmp{self.solutionID}.txt","w") as f:
      f.write(str(xCoordinateOfLinkZero)) #move inside screen
    os.rename(f"./data/seed{self.seedId}/body{self.urdfId}/tmp{self.solutionID}.txt", f"./data/seed{self.seedId}/body{self.urdfId}/fitness{self.solutionID}.txt", )
