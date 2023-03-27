import os
import sys
import random

class WorldBase:
  def __init__(self, fileName, initPos):
    print("="*10, "world base","="*10)
    self.fileName = fileName
    self.initPos = initPos
    folderName = os.path.dirname(fileName)
    if not os.path.exists(folderName):
      os.makedirs(folderName)

  def Create_SDF(self):
    pass

  def Add_Wall(self, pyrosim):
    #add wall
    box_id=0
    print("="*10,"add wall","="*10)
    length = 40.0
    height = 2.0
    mass = 100
    pyrosim.Send_Cube(name=f"wall{box_id}", pos=[0, -2.3 ,height/2.0] , size=[length,0.5,height], mass=mass)
    box_id+=1
    pyrosim.Send_Cube(name=f"wall{box_id}", pos=[0, 2.3 ,height/2.0] , size=[length,0.5,height], mass=mass)
    box_id+=1
    return