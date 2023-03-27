from env.simualtion import SIMULATION
from ea_morphology.solution import SOLUTION as m_SOLUTION
from ea_brain.solution import SOLUTION as b_SOLUTION
from world.terrain import TerrainWorld
from world.maze import MazeWorld
from world.bumper import BumperWorld
from world.stair import StairWorld
import os
import sys
import random

def Create_World(init_x=1.0, option='all'):
  seed = random.randint(0,50000) 
  seed = 14213 # 33692 #random.randint(0,50000) #8125 #random.randint(0,50000)
  random.seed(seed)
  print("="*40, seed)
  if option == "terrain":
    tw = TerrainWorld(fileName=f"./data/{option}/world.sdf", initPos=[0.5, 0, 0]) 
    tw.Create_SDF()
  elif option == "obstacle":
    tw = MazeWorld(fileName=f"./data/{option}/world.sdf", initPos=[0.5, 0, 0]) #4.5
    tw.Create_SDF()
  elif option == "bumper":
    tw = BumperWorld(fileName=f"./data/{option}/world.sdf", initPos=[0.5, 0, 0]) #8.5
    tw.Create_SDF()
  elif option == "step":
    tw = StairWorld(fileName=f"./data/{option}/world.sdf", initPos=[0.5, 0, 0]) #12.5
    tw.Create_SDF()

if __name__=="__main__":
  seedId = 0
  directOrGUI = "GUI"
  brainID = "-1"
  urdfId = 0
  envName = "bumper" #"step" #"bumper" #"obstacle" #"terrain" 

  # from ea_morphology.solution import Check_Self_Collision
  # xx = Check_Self_Collision("/home/ubuntu/mnt_magics/code_ws/ros/artificiallife/hw-artificial-life/final/data/bumper/seed0/body0/body.urdf")
  # print(xx)

  m = m_SOLUTION(m_id=urdfId,seed_id=seedId, env_name=envName)
  b = b_SOLUTION(inputId=-1,urdfId=urdfId, seedId=seedId, envName=envName)
  b.Generate_Brain()
  Create_World(option=envName)

  simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName, removeBrain=False)
  import time 
  time.sleep(1000)
  simulation.Run()

