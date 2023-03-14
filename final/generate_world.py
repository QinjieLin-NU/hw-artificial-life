from env.simualtion import SIMULATION
from ea_morphology.solution import SOLUTION as m_SOLUTION
from ea_brain.solution import SOLUTION as b_SOLUTION
import os
import sys
import pyrosim.pyrosim as pyrosim
import random

def Create_World(init_x=1.0, option='all', filename=None):
  seed = random.randint(0,50000) 
  seed = 14213 # 33692 #random.randint(0,50000) #8125 #random.randint(0,50000)
  random.seed(seed)
  print("="*40, seed)

  print("="*10,f"creating {option}","="*10)
  if not os.path.exists(f"./data/{option}"):
    os.makedirs(f"./data/{option}")
  if filename is None:
    pyrosim.Start_SDF(f"./data/{option}/world.sdf")
  else:
    pyrosim.Start_SDF(f"./data/{option}/{filename}.sdf")
  box_id = 0

  #create terrain
  if option == 'all' or option == 'terrain':
    terrain_init_x = 0.5
    terrain_x_num, terrain_y_num = 4, 4
    for i in range(terrain_x_num):
      pos_x = terrain_init_x + 0.5 + i
      for j in range(terrain_y_num):
        pos_y = 0.5 + j  -2
        pos_z = random.random() / 10
        mass=100
        pyrosim.Send_Cube(name=f"Box{box_id}", pos=[pos_x,pos_y,pos_z/2.0], size=[1,1,pos_z], mass=mass)
        box_id+=1

  #create obstacle
  if option == 'all' or option == 'obstacle':
    obstacle_init_x = 4.5 if option == 'all' else 0.5
    terrain_x_num, terrain_y_num = 4, 4
    for i in range(terrain_x_num):
      pos_x = obstacle_init_x + 0.5 + i
      for j in range(terrain_y_num):
        pos_y = 0.5 + j  -2
        size_z = 2.0 
        mass=100
        if random.sample([0,0,0,1],1)[0]:
          pyrosim.Send_Cube(name=f"Box{box_id}", pos=[pos_x,pos_y,size_z/2.0], size=[1,1,size_z], mass=mass)
          box_id+=1

  # create bumper
  if option == 'all' or option == 'bumper':
    bumper_init_x =  8.5 if option == 'all' else 0.5
    terrain_x_num = 4
    for i in range(terrain_x_num):
      pos_x = bumper_init_x + 1.0 + i*2
      pos_y = 0.0
      size_z = 0.2
      size_x = 0.1
      mass=100
      pyrosim.Send_Cube(name=f"Box{box_id}", pos=[pos_x,pos_y,size_z/2.0], size=[size_x,4,size_z], mass=mass)
      box_id+=1

  #create steps
  if option == 'all' or option == 'step':
    step_init_x = 16.5 if option == 'all' else 1.0
    mass=100.0
    delta_x, delta_z = 1.0, 0.1
    size_y = 4.0
    step_num = 8
    for i in range(step_num):
      pyrosim.Send_Cube(name=f"Box{box_id}", pos=[step_init_x+delta_x*(i+0.5),0,delta_z*(i+1)/2.0] , size=[delta_x,size_y,delta_z*(i+1)], mass=mass)
      box_id+=1

  #add wall
  print("="*10,"ending","="*10)
  length = 40.0
  height = 2.0
  pyrosim.Send_Cube(name=f"Box{box_id}", pos=[0, -2.3 ,height/2.0] , size=[length,0.5,height], mass=mass)
  box_id+=1
  pyrosim.Send_Cube(name=f"Box{box_id}", pos=[0, 2.3 ,height/2.0] , size=[length,0.5,height], mass=mass)
  box_id+=1

  pyrosim.End()
  return

if __name__=="__main__":
  seedId = 0
  directOrGUI = "GUI"
  brainID = "-1"
  urdfId = 0
  envName = "bumper" if len(sys.argv)<2 else sys.argv[1]

  m = m_SOLUTION(m_id=urdfId,seed_id=seedId, env_name=envName)
  b = b_SOLUTION(inputId=-1,urdfId=urdfId, seedId=seedId, envName=envName)
  b.Generate_Brain()
  # Create_World(option=envName)
  simulation = SIMULATION(directOrGUI, brainID, urdfId, seedId, envName, removeBrain=False)
  import time 
  time.sleep(1000)
  simulation.Run()

