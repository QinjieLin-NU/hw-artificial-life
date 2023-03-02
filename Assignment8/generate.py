import copy
import numpy
import os
import random
import sys
import time

from ea_morphology.solution import *

def set_seed(seedId):
  random.seed(seedId)
  numpy.random.seed(seedId)

seed = random.randint(0,50000)
# seed = 39846 #46168
set_seed(seed)
print("="*40, seed)
seed=0
m = SOLUTION(0,seed)
m.Visualize()

# seed = random.randint(0,50000)
# set_seed(seed)
# print("="*20, seed)

m2 = copy.deepcopy(m)
m2.Set_ID(10)
m2.Mutate()
m2.Visualize()

