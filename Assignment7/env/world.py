import pybullet as p

class WORLD:
  def __init__(self):
    self.plane_id = p.loadURDF("plane.urdf")
    self.world_id = p.loadSDF("./data/world.sdf")