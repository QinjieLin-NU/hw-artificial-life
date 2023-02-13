import codeop
import numpy

#robot related
length = 2000 #1000 #500 #200
pi = numpy.pi
max_force = 30 #100 #20
motorJointRange = 1.0 #0.5 #0.8 #0.5 good #0.2
gravity=-9.8

#EArelated
numberOfGenerations= 2 #10
populationSize = 40 #60 #10

# random related
import random
import numpy
seed = random.randint(0,50000) #12474 #8989 #12345 #98798 #8989 #2345 #5768 #123 #2345 #12345
random.seed(seed)
numpy.random.seed(seed)