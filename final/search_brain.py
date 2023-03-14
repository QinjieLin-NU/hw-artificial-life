import argparse
import os
import sys

from  ea_brain.parallelHillClimber import PARALLEL_HILL_CLIMBER

def parse_args():
  parser = argparse.ArgumentParser(description='This is a description of the program.')
  parser.add_argument('--brain_seed', type=int,  required=True, help='seed')
  parser.add_argument('--morphology_seed', type=int,  required=True, help='seed')
  parser.add_argument('--urdf_id', type=int, required=True, help='body ID')
  parser.add_argument('--env_name', type=str, required=True, help='env Name')
  return parser.parse_args()

parsed_args = parse_args()
urdfId = parsed_args.urdf_id
seedId = parsed_args.morphology_seed
brain_seedId = parsed_args.brain_seed
envName = parsed_args.env_name

phc = PARALLEL_HILL_CLIMBER(urdfId, seedId, envName, brain_seedId)
phc.Evolve()
phc.Save_Best()