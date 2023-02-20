import sys

from env.simualtion import SIMULATION

directOrGUI = sys.argv[1]
brainID = sys.argv[2]
simulation = SIMULATION(directOrGUI, brainID)
simulation.Run()
simulation.Get_Fitness()
