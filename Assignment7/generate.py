import sys
import time
from ea.creature import Generate_Snake,Geneate_Climber
from env.simualtion import SIMULATION

directOrGUI = 'GUI'
brainID = '-100'

Geneate_Climber()
time.sleep(1)

# import urdfpy

# # Load the URDF file
# robot = urdfpy.URDF.load("./data/body.urdf")


simulation = SIMULATION(directOrGUI, brainID, removeBrain=False, onlyView=True)
simulation.Run()
simulation.Get_Fitness()
