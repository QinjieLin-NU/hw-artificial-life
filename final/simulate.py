import sys

from env.simualtion import SIMULATION

directOrGUI = sys.argv[1]
brainID = sys.argv[2]
urdfId = sys.argv[3]
seedId = int(sys.argv[4])
envName = sys.argv[5]
simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName)
simulation.Run()
simulation.Get_Fitness()
