import sys

import ea.constants as c
from ea.parallelHillClimber import PARALLEL_HILL_CLIMBER
from ea.solution import SOLUTION
from env.simualtion import SIMULATION

option = sys.argv[1]
c.length = 1300
if option=="best":
  directOrGUI = "GUI"
  brainID = "-100"
  simulation = SIMULATION(directOrGUI, brainID, removeBrain=False)
  simulation.Run()
if option=="random":
  s = SOLUTION(inputId=-1)
  s.Generate_Brain()
  directOrGUI = "GUI"
  brainID = "-1"
  simulation = SIMULATION(directOrGUI, brainID, removeBrain=False)
  simulation.Run()
