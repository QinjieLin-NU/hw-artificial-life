import numpy
import os
import random
import time
import xml.etree.ElementTree as ET

import pyrosim.pyrosim as pyrosim

def get_joints_links(file_name):
  root = ET.parse(file_name)
  links, joints = [], []
  for l in root.findall("link"):
    color_name = l.findall('visual')[0].findall('material')[0].get('name')
    sensor_tag = True if color_name == 'green' else False
    links.append({'name': l.get('name'),
                  'sensor_tag': sensor_tag})
  for j in root.findall("joint"):
    joints.append({'name': j.get('name')})
  return links, joints

class SOLUTION:
  def __init__(self, inputId, urdfId, seedId):
    self.urdfId = urdfId
    self.seedId = seedId
    self.urdf_file = f"./data/seed{self.seedId}/body{self.urdfId}/body.urdf"
    links, joints = get_joints_links(self.urdf_file)
    self.links, self.link_num = links, len(links)
    self.joints, self.joint_num = joints, len(joints)
    self.sensor_num, self.motor_num = sum([l['sensor_tag'] for l in links]), len(joints)
    self.weights = numpy.random.rand(self.sensor_num,self.motor_num)
    self.weights = 2*self.weights -1
    self.myID = inputId

  def Start_Simulation(self,directOrGUI='DIRECT'):
    self.Generate_Brain()
    os.system(f"python3 simulate.py {directOrGUI} {self.myID} {self.urdfId} {self.seedId} > /dev/null 2>&1 &")
    # os.system(f"python3 simulate.py {directOrGUI} {self.myID} {self.urdfId} {self.seedId} &")

  def Wait_For_Simulation_To_End(self):
    while not os.path.exists(f"./data/seed{self.seedId}/body{self.urdfId}/fitness{self.myID}.txt"):
      time.sleep(0.001)
    time.sleep(0.001)
    with open(f"./data/seed{self.seedId}/body{self.urdfId}/fitness{self.myID}.txt", "r") as f:
      self.fitness = float(f.read())
    os.system(f"rm ./data/seed{self.seedId}/body{self.urdfId}/fitness{self.myID}.txt")

  def Mutate(self):
    randomRow,randomColumn = random.randint(0,self.sensor_num-1), random.randint(0,self.motor_num-1)
    self.weights[randomRow,randomColumn] =  random.random()*2-1
  
  def Set_ID(self, inputId):
    self.myID = inputId

  def Generate_Brain(self,prefix=None):
    if prefix is None:
      file_prefix = self.myID
    else:
      file_prefix = prefix
    #generate brain
    pyrosim.Start_NeuralNetwork(f"./data/seed{self.seedId}/body{self.urdfId}/brain{file_prefix}.nndf")
    neuron_id = 0
    for i in range(self.link_num):
      if self.links[i]['sensor_tag']:
        pyrosim.Send_Sensor_Neuron(name = neuron_id , linkName = self.links[i]['name'])
        neuron_id += 1
    for i in range(self.motor_num):
      pyrosim.Send_Motor_Neuron(name = neuron_id , jointName = self.joints[i]['name'])
      neuron_id += 1
    for currentRow  in range(self.sensor_num):
      for currentColumn  in range(self.motor_num):
        pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn+self.sensor_num , \
          weight = self.weights[currentRow][currentColumn] )
    pyrosim.End()
    return

