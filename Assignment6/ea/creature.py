import random

import pyrosim.pyrosim as pyrosim

def Generate_Snake():
  # generate a snake along x axis
  # generate all n links(name,position and size) and n-1 joints(name, parent, child, position and jointAxis)
  links, joints = [], []
  link_number = random.randint(3,15) #3 15
  for i in range(link_number):
    size_range = (0.2,1.5) #0.2 1.5
    size_x, size_y, size_z = random.uniform(*size_range), random.uniform(*size_range), random.uniform(*size_range)
    if i ==0:
      pos_x, pos_y, pos_z = size_x/2.0, 0.0, size_z/2.0 #a snake along x axis
    else:
      parent_size_z = links[i-1]['size'][2]
      relative_posz = size_z/2.0 - parent_size_z/2.0 
      pos_x, pos_y, pos_z = size_x/2.0, 0.0, relative_posz #a snake along x axis
    sensor_tag = random.sample([True,False],k=1)[0]
    color_name = 'green' if sensor_tag else 'red'
    link_color = '0 1.0 0 1.0' if sensor_tag else '0 0 1.0 1.0'
    link_dict = {
      "name": f"link{i}",
      "size": [size_x, size_y, size_z],
      "pos": [pos_x, pos_y, pos_z],
      'sensor_tag': sensor_tag, 'color': link_color, 'color_name': color_name,
    }
    links.append(link_dict)

  for i in range(link_number-1):
    parent,child = links[i]['name'], links[i+1]['name']
    joint_name = f'{parent}_{child}'
    parent_size_z = links[i]['size'][2]
    if i ==0:
      position_x, position_y, position_z = links[i]['size'][0], 0, parent_size_z/2.0 #a snake along x axis
    else:
      parent_of_parent_size_z = links[i-1]['size'][2]
      position_x, position_y, position_z = links[i]['size'][0], 0, parent_size_z/2.0 - parent_of_parent_size_z/2.0 #a snake along x axis
    # jointAxis = '0 0 1' #rotate along z axis
    joint_axis_type = random.sample(['z','y'],k=1)[0]
    jointAxis = '0 0 1' if joint_axis_type=='z' else '0 1 0' #rotate along z axis or y axis
    joint_dict = {
      'name': joint_name,
      'parent': parent, 'child': child, 
      'position': [position_x, position_y, position_z], 'jointAxis': jointAxis,
    }
    joints.append(joint_dict)

  #generating urdf
  pyrosim.Start_URDF("./data/body.urdf")
  for i in range(link_number):
    link_dict = links[i]
    pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'], color=link_dict['color'], color_name=link_dict['color_name'])
    if i<link_number-1:
      joint_dict = joints[i]
      pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
      type = "revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
  pyrosim.End()
  return links,joints

def Create_World():
  pyrosim.Start_SDF("./data/world.sdf")
  delta_x, delta_z = 1.5, 0.2
  init_x = 0.75
  mass=100.0
  pyrosim.Send_Cube(name="Box1", pos=[init_x+delta_x*0.5,0,delta_z/2.0] , size=[delta_x,20,delta_z], mass=mass)
  pyrosim.Send_Cube(name="Box2", pos=[init_x+delta_x*1.5,0,(delta_z*2)/2.0] , size=[delta_x,20,delta_z*2], mass=mass)
  pyrosim.Send_Cube(name="Box3", pos=[init_x+delta_x*2.5,0,(delta_z*3)/2.0] , size=[delta_x,20,delta_z*3], mass=mass)
  pyrosim.Send_Cube(name="Box4", pos=[init_x+delta_x*3.5,0,(delta_z*4)/2.0] , size=[delta_x,20,delta_z*4], mass=mass)
  pyrosim.Send_Cube(name="Box5", pos=[init_x+delta_x*4.5,0,(delta_z*5)/2.0] , size=[delta_x,20,delta_z*5], mass=mass)
  pyrosim.Send_Cube(name="Box6", pos=[init_x+delta_x*5.5,0,(delta_z*6)/2.0] , size=[delta_x,20,delta_z*6], mass=mass)
  pyrosim.End()
  return