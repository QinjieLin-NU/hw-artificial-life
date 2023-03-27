import os
import sys
import random

import pyrosim.pyrosim as pyrosim
from world.base import WorldBase

class StairWorld(WorldBase):
  def __init__(self, fileName, initPos):
    super().__init__(fileName, initPos)
  
  def Create_SDF(self, roughness=None):
    print("="*10,f"creating stairs","="*10)
    pyrosim.Start_SDF(self.fileName)

    #create terrain
    box_id = 0
    step_init_x = self.initPos[0]
    mass=100.0
    delta_x, delta_z = 1.0, 0.1
    size_y = 4.0
    step_num = 8
    for i in range(step_num):
      pyrosim.Send_Cube(name=f"stair{box_id}", pos=[step_init_x+delta_x*(i+0.5),0,delta_z*(i+1)/2.0] , size=[delta_x,size_y,delta_z*(i+1)], mass=mass)
      box_id+=1

    #add wall 
    super().Add_Wall(pyrosim)
    pyrosim.End()
