import codeop
import numpy

#robot related
length = 2000 #1000 #500 #200
pi = numpy.pi
max_force = 100 #20
numSensorNeurons = 7
numMotorNeurons = 6
motorJointRange = 0.5 #0.8 #0.5 good #0.2
gravity=-9.8

#EArelated
numberOfGenerations= 5 #10
populationSize = 60 #60 #10

# random related
import random
import numpy
seed = 123 #5768 #123 #2345 #12345
random.seed(seed)
numpy.random.seed(seed)