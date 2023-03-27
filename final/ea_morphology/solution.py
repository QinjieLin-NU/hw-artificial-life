import copy
import numpy as np
import os
import pybullet as p
import random
import time

import ea_morphology.constants as c
from ea_morphology.colorPalette import sensored_palette as sensored_palette
from ea_morphology.colorPalette import unsensored_palette as unsensored_palette
import pyrosim.pyrosim as pyrosim

class Edge:
  def __init__(self, pos, axis, expand_direction):
    self.pos = pos
    self.axis = axis
    self.expand_direction = expand_direction      

class Node:
  def __init__(self, attached_edge, edge_direction_history, geometry_type, size, pos, sensor_tag, color, color_name, children):
    self.attached_edge = attached_edge
    self.edge_direction_history = edge_direction_history
    self.geometry_type = geometry_type
    self.size = size
    self.pos = pos
    self.sensor_tag = sensor_tag
    self.color = color
    self.color_name = color_name
    self.children = children

def Random_Node(parent_node,expand_direction):
  def joint_expand_list():
    if second_or_not:
      return [x/2.0 for x in expand_direction]
    else:
      # return expand_direction
      direction_index = [i for (i,e) in enumerate(expand_direction) if e!=0][-1]
      direction_history = [h[direction_index] for h in parent_node.edge_direction_history if h[direction_index]!=0]
      if len(direction_history) == 0:
        diag = np.array([x/2.0 for x in expand_direction]) + np.array([x/2.0 for x in parent_node.edge_direction_history[-1]])
        # return [x/2.0 for x in expand_direction] #TODO
        return list(diag)
      else:
        if direction_history[-1]*expand_direction[direction_index]<0:
          return [0 for x in expand_direction]
        else:
          return expand_direction
  def joint_trans_list():
    trans_pos = [0,0,0]
    pos_or_neg = 1 if sum(expand_direction)>0 else -1 #TODO
    for i in range(len(expand_direction)):
      pos_range = parent_node.size[i]
      # 0 means same level, -1 means upper, 1 means lower
      if second_or_not: #TODO
        pos_range = pos_range/2.0
      #TODO 1 or 1/2
      if expand_direction[i]==0:
        d = random.sample([0,pos_or_neg],k=1)[0]*pos_range
        trans_pos[i]=d
        if d != 0:
          break
        # if second_or_not and d==0:
    return trans_pos
  def link_trans_list():
    link_trans_matrix = [1/2,1/2,1/2]
    pos_or_neg = 1 if sum(expand_direction)>0 else -1 #TODO
    others_factor = 0
    for i in range(len(expand_direction)):
      link_trans_matrix[i] = link_trans_matrix[i]*pos_or_neg if expand_direction[i]!=0 else link_trans_matrix[i]*others_factor #TODO check
    return link_trans_matrix
  def get_joint_axis():
    joint_axis = ['0']*3
    # pick one 0 in edge_pos and change the same index of joint_axis to 1
    rotated_axis_index = []
    for (i,p) in enumerate(edge_pos):
      if p == 0:
        rotated_axis_index.append(i)
    joint_axis[random.sample(rotated_axis_index,k=1)[0]] = '1'
    return ' '.join(joint_axis)
  root_or_not = not(parent_node and expand_direction)
  second_or_not = False
  # link type
  type_range = c.link_type_range
  link_type = random.sample(type_range, k=1)[0]
  # link size
  size_range = c.link_size_range
  size = [random.uniform(*size_range), random.uniform(*size_range), random.uniform(*size_range)]
  if link_type == "sphere":
    size = [size[0]]*3
  elif link_type == "cylinder":
    size = [size[0], size[0], size[2]] #TODO this assume we don't rotate the cylinder
  #joint
  edge = None 
  edge_direction_history = []
  if not root_or_not:
    if parent_node.attached_edge is None:
      second_or_not = True
    edge_pos = list(np.array(parent_node.size) * np.array(joint_expand_list())) #exapnd direction transition
    # edge_pos = list(np.array(edge_pos) + np.array(joint_trans_list())) #TODO position transtion
    edge_axis = get_joint_axis() 
    edge = Edge(edge_pos, edge_axis, expand_direction)
    edge_direction_history = parent_node.edge_direction_history+[expand_direction]
  # link pos
  if root_or_not:
    link_trans_matrix = [0,0,0] 
    pos = np.array(size)*np.array(link_trans_matrix)
  else:
    pos = np.array(size)*np.array(link_trans_list()) 
  if parent_node:
    node_depth = len(parent_node.edge_direction_history) + 1
  else:
    node_depth = 0
  sensor_tag = random.sample([True,False],k=1)[0]
  color_name = list(sensored_palette.keys())[node_depth] if sensor_tag else list(unsensored_palette.keys())[node_depth]
  color = sensored_palette[color_name] if sensor_tag else unsensored_palette[color_name]
  n = Node(edge, edge_direction_history, link_type, size, pos, sensor_tag, color, color_name, [])
  return n

def Traverse_Node(root_node):
  # BFS
  stack = [(root_node,0)]
  visited_nodes = []
  while stack:
    (n,d) = stack.pop(0)
    visited_nodes.append((n,d))
    for c in n.children:
      if c:
        stack.append((c,d+1))
  return visited_nodes

def Find_Min_Depth(root_node):
  # DFS
  stack = [(root_node,root_node.size[2]/-2.0)]
  min_depth = 0
  while stack:
    (n,d) = stack.pop()
    min_depth = min(d,min_depth)
    for c in n.children:
      if c:
        if all([x is None for x in c.children]):
          stack.append((c,d+c.attached_edge.pos[2]-c.size[2]/2.0))
        else:
          stack.append((c,d+c.attached_edge.pos[2]))
  return min_depth

def Expand_Node(root_node, depth):
  #TODO
  maximum_depth = c.maximum_depth
  minimum_depth = c.minimum_depth
  # check if arrive deepest level
  if depth>=maximum_depth:
    return 
  # check if the node is leave
  root_node.children=[]
  leaf_or_not = True if random.random() < c.node_leaf_prob else False
  if leaf_or_not and depth>=minimum_depth:
    return 
  # expand the node if not leave
  expand_directions = c.expand_directions
  for (i,direction) in enumerate(expand_directions):
    # cutting tree
    if root_node.edge_direction_history and np.all((np.array(root_node.edge_direction_history[-1])+np.array(direction))==0):
      root_node.children.append(None)
      continue
    #TODO
    expand_or_not = True if random.random() < c.node_expand_prob else False
    if expand_or_not:
      #print("before randoming", depth, i)
      child = Random_Node(root_node, direction) 
      Expand_Node(child, depth+1)
      root_node.children.append(child)
    else:
      root_node.children.append(None)
  return 

def Mutate(tree_root):
  mutated_tree = copy.deepcopy(tree_root)
  ns = Traverse_Node(mutated_tree)
  (n,d) = random.sample(ns,k=1)[0]
  # print("Mutating",n.size)
  Expand_Node(n,d)
  return mutated_tree

def Convert_Tree_to_Urdf(root_node, file_name):
  if not os.path.exists(os.path.dirname(os.path.dirname(os.path.dirname(file_name)))):
    os.makedirs(os.path.dirname(os.path.dirname(os.path.dirname(file_name))))
  if not os.path.exists(os.path.dirname(os.path.dirname(file_name))):
    os.makedirs(os.path.dirname(os.path.dirname(file_name)))
  if not os.path.exists(os.path.dirname(file_name)):
    os.makedirs(os.path.dirname(file_name))
  #out min depth
  min_depth = Find_Min_Depth(root_node)
  with open(os.path.dirname(file_name)+"/min_depth.txt","w") as f:
    f.write(str(min_depth))
  #traverse the tree
  links, joints = {}, {}
  link_id = 0
  stack = [(None,root_node)]
  while stack:
    (parent_name,n) = stack.pop(0); link_id += 1; link_name = f"link{link_id}"
    links[link_name] = {
      "name": link_name, "geometry_type": n.geometry_type, "size": n.size, "pos": n.pos,
      'sensor_tag': n.sensor_tag, "color": n.color, "color_name": n.color_name,
    }
    if n.attached_edge:
      joint_name = f"{parent_name}_{link_name}"
      joints[joint_name] = {
        'name': joint_name,
        'parent': parent_name, 'child': link_name, 
        'position': n.attached_edge.pos, 'jointAxis': n.attached_edge.axis,
      }
    # print(n.edge_direction_history)
    for c in n.children:
      parent_name = link_name
      if c:
        stack.append((parent_name,c))
  # generate urdf file
  pyrosim.Start_URDF(file_name)
  for link_dict in links.values():
    pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'], color=link_dict['color'], color_name=link_dict['color_name'], geometry_type=link_dict["geometry_type"])
  for joint_dict in joints.values():
    pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
      type = "revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
  pyrosim.End()
  return list(links.values()), list(joints.values())

def Check_Self_Collision(urdf_file):
  physicsClient = p.connect(p.DIRECT)
  robot_id = p.loadURDF(urdf_file, flags=p.URDF_USE_SELF_COLLISION+p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT)
  # Enable self-collision checking
  p.setCollisionFilterGroupMask(robot_id, -1, 1, 1)
  p.setCollisionFilterPair(robot_id, robot_id, -1, -1, 0)
  # Check for collisions
  p.stepSimulation()
  contact_points = p.getContactPoints(bodyA=robot_id, bodyB=robot_id)
  collision = False
  if len(contact_points) > 0:
    # print("="*30,"self collision happens")
    collision = True
  p.disconnect() 
  return collision #TODO

class SOLUTION:
  def __init__(self, m_id, seed_id, env_name="all"):
    self.m_id = m_id
    self.seed = seed_id
    self.env_name = env_name
    self.urdf_folder = f"./data/{self.env_name}/seed{self.seed}/body{m_id}"
    self.tree_root = Random_Node(None,None)
    Expand_Node(self.tree_root, depth=0)
    while self.Check_Collision_and_Num():
      self.tree_root = Random_Node(None,None)
      Expand_Node(self.tree_root, depth=0)
    
  def Set_ID(self,input_id):
    self.m_id = input_id
    self.urdf_folder = f"./data/{self.env_name}/seed{self.seed}/body{self.m_id}"
  
  def Mutate(self):
    urdf_file = f"{self.urdf_folder}/body.urdf"
    self_collision=True
    while self_collision or one_link or zero_sensor:
      mutated_root = Mutate(self.tree_root)
      links, joints = Convert_Tree_to_Urdf(mutated_root, urdf_file)
      self_collision = Check_Self_Collision(urdf_file)
      one_link = (len(links)==1 )
      zero_sensor = (sum([l['sensor_tag'] for l in links]) == 0)
    # self.Traverse()
    self.tree_root = mutated_root 
    # self.Traverse()

  def Traverse(self):
    vn = Traverse_Node(self.tree_root)
    for (n,d) in vn:
      print(d,n.size)

  def Generate_URDF(self):
    urdf_file = f"{self.urdf_folder}/body.urdf"
    Convert_Tree_to_Urdf(self.tree_root, urdf_file)
  
  def Check_Collision_and_Num(self):
    urdf_file = f"{self.urdf_folder}/body.urdf"
    links, joints = Convert_Tree_to_Urdf(self.tree_root, urdf_file)
    one_link = (len(links)==1 )
    zero_sensor = (sum([l['sensor_tag'] for l in links])==0)
    return (Check_Self_Collision(urdf_file) or one_link or zero_sensor)
  
  def Visualize(self):
    urdf_file = f"{self.urdf_folder}/body.urdf"
    links, joints = Convert_Tree_to_Urdf(self.tree_root, urdf_file)
    physicsClient = p.connect(p.GUI)
    p.loadURDF(urdf_file)
    input()
    p.disconnect()
  
  def Start_Simulation(self,directOrGUI):
    self.Generate_URDF()
    brain_seed = random.randint(0,99999)
    os.system(f"python3 search_brain.py --urdf_id {self.m_id} --morphology_seed {self.seed} --brain_seed {brain_seed} --env_name {self.env_name} > /dev/null 2>&1 &")
    # os.system(f"python3 search_brain.py --urdf_id {self.m_id} --morphology_seed {self.seed} --brain_seed {brain_seed} --env_name {self.env_name} ")
    return
  
  def Replay_Best(self):
    os.system(f"python3 replay_brain.py best {self.m_id} {self.seed} {self.env_name} > /dev/null 2>&1 &")
    return

  def Replay_Random(self):
    os.system(f"python3 replay_brain.py random {self.m_id} {self.seed} > /dev/null 2>&1 &")
    return

  def Wait_For_Simulation_To_End(self):
    fitness_file = f"{self.urdf_folder}/best_fitness.txt"
    print("waiting",self.m_id)
    while not os.path.exists(fitness_file):
      time.sleep(0.001)
    print("finish waiting",self.m_id)
    time.sleep(0.001)
    for i in range(20):
      try:
        with open(fitness_file, "r") as f:
          self.fitness = float(f.read())
        break
      except:
        print(f"retrying {i}")
        time.sleep(0.01)