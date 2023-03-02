import sys

from env.simualtion import SIMULATION

directOrGUI = sys.argv[1]
brainID = sys.argv[2]
urdfId = sys.argv[3]
seedId = int(sys.argv[4])
simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId)
simulation.Run()
simulation.Get_Fitness()
