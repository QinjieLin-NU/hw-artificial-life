import os
import sys
import random

import pyrosim.pyrosim as pyrosim
from world.base import WorldBase

class MazeWorld(WorldBase):
  def __init__(self, fileName, initPos):
    super().__init__(fileName, initPos)
  
  def Create_SDF(self,):
    print("="*10,f"creating maze","="*10)
    pyrosim.Start_SDF(self.fileName)

    #create terrain
    box_id = 0
    obstacle_init_x = self.initPos[0]
    terrain_x_num, terrain_y_num = 4, 4
    for i in range(terrain_x_num):
      pos_x = obstacle_init_x + 0.5 + i
      for j in range(terrain_y_num):
        pos_y = 0.5 + j  -2
        size_z = 2.0 
        size_x, size_y = 1, 1
        mass=100
        if random.sample([0,0,0,1],1)[0]:
          pyrosim.Send_Cube(name=f"maze{box_id}", pos=[pos_x,pos_y,size_z/2.0], size=[size_x,size_y,size_z], mass=mass)
          box_id+=1

    #add wall 
    super().Add_Wall(pyrosim)
    pyrosim.End()