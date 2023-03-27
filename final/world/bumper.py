import os
import sys
import random

import pyrosim.pyrosim as pyrosim
from world.base import WorldBase

class BumperWorld(WorldBase):
  def __init__(self, fileName, initPos):
    super().__init__(fileName, initPos)
  
  def Create_SDF(self, roughness=None):
    print("="*10,f"creating bumper","="*10)
    pyrosim.Start_SDF(self.fileName)

    #create terrain
    box_id = 0
    bumper_init_x =  self.initPos[0]
    terrain_x_num = 4
    for i in range(terrain_x_num):
      pos_x = bumper_init_x + 1.0 + i*2
      pos_y = 0.0
      size_z = 0.2
      size_x = 0.1
      mass=100
      pyrosim.Send_Cube(name=f"bumper{box_id}", pos=[pos_x,pos_y,size_z/2.0], size=[size_x,4,size_z], mass=mass)
      box_id+=1

    #add wall 
    super().Add_Wall(pyrosim)
    pyrosim.End()
