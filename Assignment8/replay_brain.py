import sys

import ea_brain.constants as c
from ea_brain.parallelHillClimber import PARALLEL_HILL_CLIMBER
from ea_brain.solution import SOLUTION
from env.simualtion import SIMULATION

option = sys.argv[1]
urdfId = sys.argv[2]
seedId = int(sys.argv[3])
c.length = 10000
if option=="best":
  directOrGUI = "GUI"
  brainID = "-100"
  simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, removeBrain=False)
  simulation.Run()
if option=="random":
  s = SOLUTION(inputId=-1, urdfId=urdfId, seedId=seedId)
  s.Generate_Brain()
  directOrGUI = "GUI"
  brainID = "-1"
  simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, removeBrain=False)
  simulation.Run()
