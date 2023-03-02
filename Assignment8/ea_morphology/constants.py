import codeop
import numpy

#link
link_size_range = (0.1,0.2)  #(0.05,0.4) #(0.2,0.2) 
maximum_depth = 3#2
minimum_depth = 2#2
node_leaf_prob = 0.4#0.1
node_expand_prob = 0.6#0.6
joint_gap = 0.0001
expand_directions = [
  [1+joint_gap, 0, 0], 
  #[-1-joint_gap, 0, 0], 
  [0, 1+joint_gap, 0], 
  [0, -1-joint_gap, 0], 
  # [0, 0, 1+joint_gap], 
  [0, 0, -1-joint_gap],
]

#EArelated
numberOfGenerations= 20 #5 #10
populationSize = 20 #60 #10
