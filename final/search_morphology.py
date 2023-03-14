import argparse
import os
import random
import sys

import generate_world
from ea_morphology.parallelHillClimber import PARALLEL_HILL_CLIMBER

def parse_args():
  parser = argparse.ArgumentParser(description='This is a description of the program.')
  parser.add_argument('--seed', type=int, help='seed')
  parser.add_argument('--env', type=str, required=True, help='seed')
  return parser.parse_args()

#must before Create_world
parsed_args = parse_args()
seed = random.randint(0,50000) if parsed_args.seed is None else parsed_args.seed

#creating world.sdf
env_name = 'all' if parsed_args.env is None else parsed_args.env
generate_world.Create_World(option=env_name)

#co-evolution
print("="*10,f"seed:{seed}","="*10)
phc = PARALLEL_HILL_CLIMBER(seed, env_name)
phc.Evolve()
phc.Show_Best()