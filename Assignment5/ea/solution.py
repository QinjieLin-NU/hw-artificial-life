import numpy
import os
import random
import time

import ea.constants as c
import pyrosim.pyrosim as pyrosim



class SOLUTION:
  def __init__(self, inputId):
    self.weights = numpy.random.rand(c.numSensorNeurons,c.numMotorNeurons)
    self.weights = 2*self.weights -1
    self.myID = inputId

  def Evaluate(self, directOrGUI='DIRECT'):
    self.Create_World()
    self.Generate_Body()
    self.Generate_Brain()
    os.system(f"START python simulate.py {directOrGUI} {self.myID}")
    while not os.path.exists(f"./data/fitness{self.myID}.txt"):
      time.sleep(0.01)
    with open(f"./data/fitness{self.myID}.txt", "r") as f:
      self.fitness = float(f.read())
    os.system(f"del .\\data\\fitness{self.myID}.txt")

  def Start_Simulation(self,directOrGUI='DIRECT'):
    self.Create_World()
    self.Generate_Body()
    self.Generate_Brain()
    os.system(f"START python simulate.py {directOrGUI} {self.myID}")

  def Wait_For_Simulation_To_End(self):
    while not os.path.exists(f"./data/fitness{self.myID}.txt"):
      time.sleep(0.01)
    time.sleep(0.1)
    with open(f"./data/fitness{self.myID}.txt", "r") as f:
      self.fitness = float(f.read())
    os.system(f"del .\\data\\fitness{self.myID}.txt")

  def Mutate(self):
    randomRow,randomColumn = random.randint(0,c.numSensorNeurons-1), random.randint(0,c.numMotorNeurons-1)
    self.weights[randomRow,randomColumn] =  random.random()*2-1
  
  def Set_ID(self, inputId):
    self.myID = inputId

  def Create_World(self):
    pyrosim.Start_SDF("./data/world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-2.5,2.5,0.5] , size=[1,1,1])
    pyrosim.End()
    return

  def Generate_Body(self):
    pyrosim.Start_URDF("./data/body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[0.5,0.5,0.5])

    pyrosim.Send_Joint( name = "Torso_LeftWing" , parent= "Torso" , child = "LeftWing" ,\
    type = "revolute", position = [0,-0.25,1], jointAxis='1 0 0')
    pyrosim.Send_Cube(name="LeftWing", pos=[0,-0.5,0] , size=[1,1,0.1])
    pyrosim.Send_Joint( name = "Torso_RightWing" , parent= "Torso" , child = "RightWing" ,\
    type = "revolute", position = [0,0.25,1], jointAxis='1 0 0')
    pyrosim.Send_Cube(name="RightWing", pos=[0,0.5,0] , size=[1,1,0.1])
    pyrosim.Send_Joint( name = "Torso_Crest" , parent= "Torso" , child = "Crest" ,\
    type = "revolute", position = [0,0,1.25], jointAxis='1 0 0')
    pyrosim.Send_Cube(name="Crest", pos=[0,0,0.1] , size=[0.5,0.1,0.2])

    pyrosim.End()
    return

  def Generate_Brain(self):
    pyrosim.Start_NeuralNetwork(f"./data/brain{self.myID}.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftWing")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "RightWing")
    pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Crest")

    pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_LeftWing")
    pyrosim.Send_Motor_Neuron(name = 5 , jointName = "Torso_RightWing")
    pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_Crest")

    for currentRow  in range(c.numSensorNeurons):
      for currentColumn  in range(c.numMotorNeurons):
        pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , \
          weight = self.weights[currentRow][currentColumn] )
    pyrosim.End()
    return
  
