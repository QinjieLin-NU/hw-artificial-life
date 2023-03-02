import os
import random

from  ea_morphology.parallelHillClimber import PARALLEL_HILL_CLIMBER

seed = random.randint(0,50000) 
phc = PARALLEL_HILL_CLIMBER(seed)
phc.Evolve()
phc.Show_Best()