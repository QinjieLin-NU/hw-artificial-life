import argparse
import random
import sys

import ea_brain.constants as c
from ea_brain.parallelHillClimber import PARALLEL_HILL_CLIMBER
from ea_brain.solution import SOLUTION
from env.simualtion import SIMULATION

def parse_args():
  parser = argparse.ArgumentParser(description='This is a description of the program.')
  parser.add_argument('--brain', type=str, required=True, help='best or random')
  parser.add_argument('--urdf', type=str,  required=True, help='best or random')
  parser.add_argument('--seed', type=int,  required=True, help='seed')
  parser.add_argument('--env', type=str, required=True, help='env Name')
  return parser.parse_args()

args = parse_args()
option = args.brain
urdfId = random.randint(0,420) if args.urdf=="random" else args.urdf
print("="*10,f"{urdfId}")
seedId = args.seed
envName = args.env
c.length = 2000

if option=="best":
  directOrGUI = "GUI"
  brainID = "-100"
  simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName, removeBrain=False)
  simulation.Run()
if option=="random":
  s = SOLUTION(inputId=-1, urdfId=urdfId, seedId=seedId, envName=envName)
  s.Generate_Brain()
  directOrGUI = "GUI"
  brainID = "-1"
  simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId,envName, removeBrain=False)
  simulation.Run()
