import argparse
import os
import pybullet as p
import pybullet_data
import random
import sys
import time

import ea_brain.constants as c
from ea_brain.parallelHillClimber import PARALLEL_HILL_CLIMBER
from ea_brain.solution import SOLUTION
from env.simualtion import SIMULATION

def parse_args():
  parser = argparse.ArgumentParser(description='This is a description of the program.')
  parser.add_argument('--seed', type=int, help='seed')
  parser.add_argument('--env', type=str, help='seed')
  parser.add_argument('--child', type=int, help='seed')
  parser.add_argument('--replay', action='store_true', help='Enable replay')
  return parser.parse_args()

def visualize(envName, seedId, urdfId):
  physicsClient = p.connect(p.GUI)
  p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) #Disable sidebar
  p.resetDebugVisualizerCamera(cameraDistance=1.40, cameraYaw=-53, cameraPitch=-25, cameraTargetPosition=[0.26, -0.34, 0.65]) #reser camera
  p.setAdditionalSearchPath(pybullet_data.getDataPath())
  p.setGravity(0,0,c.gravity)
  with open(f"./data/{envName}/seed{seedId}/body{urdfId}/min_depth.txt", "r") as f:
    robotPosZ = -1*float(f.read())
  robotId = p.loadURDF(f"./data/{envName}/seed{seedId}/body{urdfId}/body.urdf", 
    basePosition=[0,0,robotPosZ])
  plane_id = p.loadURDF("plane.urdf")
  if os.path.exists(f"./data/{envName}/world.sdf"):
    world_id = p.loadSDF(f"./data/{envName}/world.sdf")
  return

def visualize_generation(args):
  start_id = random.randint(0,20)
  c.length = 10
  for x in range(start_id,400,20):
    print("="*10,start_id,"="*10)
    envName = args.env
    seedId = args.seed
    urdfId = x
    directOrGUI = "GUI"
    brainID = "-100"
    # simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName, removeBrain=False)
    # simulation.Run()
    visualize(envName, seedId, urdfId)
    time.sleep(2)
    p.disconnect()

def read_file(urdf_file):
  urdf_str = ""
  with open(urdf_file, "r") as f:
    urdf_str = f.read()
  return urdf_str

def visualize_samechild(args):
  start_id = random.randint(0,20)
  c.length = 10
  for env_name in ["bumper", "step", "obstacle", "terrain"]:
    print("="*10,start_id,"="*10)
    envName = env_name
    seedId = args.seed
    urdfId = start_id
    directOrGUI = "GUI"
    brainID = "-100"
    # simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName, removeBrain=False)
    # simulation.Run()
    visualize(envName, seedId, urdfId)
    time.sleep(2)
    p.disconnect()

def visualize_genration_with_seed(args):
  start_id = random.randint(0,20) if args.child is None else args.child
  env_list = ["step", "terrain", "obstacle", "bumper"] if args.env is None else [args.env]
  for env_name in env_list:
    print("="*10,start_id,"="*10)
    last_urdf_str = ""
    for urdf_id in range(start_id,400,20):
      print("="*10,urdf_id,"="*10)
      envName = env_name
      seedId = args.seed
      urdfId = urdf_id
      directOrGUI = "GUI"
      brainID = "-100"
      urdf_file = f"./data/{envName}/seed{seedId}/body{urdfId}/body.urdf"
      current_urdf_str = read_file(urdf_file)
      if last_urdf_str == current_urdf_str:
        print("="*10,"same urdf","="*10)
        continue
      else:
        last_urdf_str = current_urdf_str
      if args.replay:
        c.length = 100
        simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName, removeBrain=False, disconnect=False)
        simulation.Run()
        time.sleep(1)
      else:
        visualize(envName, seedId, urdfId)
        time.sleep(5)
        p.disconnect()

args = parse_args()
# visualize_generation(args)
# visualize_samechild(args)
visualize_genration_with_seed(args)