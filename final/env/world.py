import os
import pybullet as p

class WORLD:
  def __init__(self, envName):
    self.plane_id = p.loadURDF("plane.urdf")
    if os.path.exists(f"./data/{envName}/world.sdf"):
      # print("loading world")
      self.world_id = p.loadSDF(f"./data/{envName}/world.sdf")