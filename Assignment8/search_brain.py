import os
import sys

from  ea_brain.parallelHillClimber import PARALLEL_HILL_CLIMBER

urdfId = sys.argv[1] 
seedId = int(sys.argv[2])

phc = PARALLEL_HILL_CLIMBER(urdfId, seedId)
phc.Evolve()
phc.Save_Best()