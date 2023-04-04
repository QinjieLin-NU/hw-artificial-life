import os
import sys
import random

import pyrosim.pyrosim as pyrosim
from world.base import WorldBase

class TerrainWorld(WorldBase):
  def __init__(self, fileName, initPos):
    super().__init__(fileName, initPos)
  
  def Create_SDF(self, roughness=None):
    print("="*10,f"creating Terrain","="*10)
    pyrosim.Start_SDF(self.fileName)

    #create terrain
    box_id = 0
    terrain_init_x = self.initPos[0]
    terrain_x_num, terrain_y_num = 4, 4
    for i in range(terrain_x_num):
      pos_x = terrain_init_x + 0.5 + i
      for j in range(terrain_y_num):
        pos_y = 0.5 + j  -2
        pos_z = random.random() / 5 #/ 10
        mass=100
        pyrosim.Send_Cube(name=f"terrain{box_id}", pos=[pos_x,pos_y,pos_z/2.0], size=[1,1,pos_z], mass=mass)
        box_id+=1
    
    #add wall 
    super().Add_Wall(pyrosim)
    pyrosim.End()
