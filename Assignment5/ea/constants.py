import codeop
import numpy

#robot related
length = 400 #200
pi = numpy.pi
max_force = 100 #20
numSensorNeurons = 7
numMotorNeurons = 6
motorJointRange = 0.2
gravity=-0.0#-9.8

#EArelated
numberOfGenerations= 1 #10
populationSize = 1 #10

# random related
import random
import numpy
seed = 5678
random.seed(seed)
numpy.random.seed(seed)