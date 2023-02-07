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
    # self.Create_World()
    # self.Generate_Body()
    self.Generate_Brain()
    os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")
    while not os.path.exists(f"./data/fitness{self.myID}.txt"):
      time.sleep(0.01)
    with open(f"./data/fitness{self.myID}.txt", "r") as f:
      self.fitness = float(f.read())
    os.system(f"rm ./data/fitness{self.myID}.txt")

  def Start_Simulation(self,directOrGUI='DIRECT'):
    # only generate once
    # self.Create_World()
    # self.Generate_Body()
    self.Generate_Brain()
    os.system(f"python3 simulate.py {directOrGUI} {self.myID} > /dev/null 2>&1 &")
    # os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")

  def Wait_For_Simulation_To_End(self):
    # print("checking",self.myID)
    while not os.path.exists(f"./data/fitness{self.myID}.txt"):
      time.sleep(0.001)
    time.sleep(0.001)
    # print("complete",self.myID)
    with open(f"./data/fitness{self.myID}.txt", "r") as f:
      self.fitness = float(f.read())
    os.system(f"rm ./data/fitness{self.myID}.txt")

  def Mutate(self):
    randomRow,randomColumn = random.randint(0,c.numSensorNeurons-1), random.randint(0,c.numMotorNeurons-1)
    self.weights[randomRow,randomColumn] =  random.random()*2-1
  
  def Set_ID(self, inputId):
    self.myID = inputId

  def Create_World_v0(self):
    pyrosim.Start_SDF("./data/world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-2.5,2.5,0.5] , size=[1,1,1])
    pyrosim.End()
    return

  def Create_World(self):
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
    # pyrosim.Send_Cube(name="Box7", pos=[init_x+delta_x*6.5,0,(delta_z*7)/2.0] , size=[delta_x,20,delta_z*7])
    # pyrosim.Send_Cube(name="Box8", pos=[init_x+delta_x*7.5,0,(delta_z*8)/2.0] , size=[delta_x,20,delta_z*8])
    # pyrosim.Send_Cube(name="Box9", pos=[init_x+delta_x*8.5,0,(delta_z*9)/2.0] , size=[delta_x,20,delta_z*9])
    # pyrosim.Send_Cube(name="Box10", pos=[init_x+delta_x*9,0,(delta_z*10/2.0] , size=[delta_x,20,delta_z*10])
    pyrosim.End()
    return

  def Generate_Bird(self):
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

  def Generate_Body(self):

    pyrosim.Start_URDF("./data/body.urdf")

    body_width, leg_length = 0.3,0.4 #0.4, 0.5 #0.3, 0.4
    
    pyrosim.Send_Cube(name="Torso", pos=[0,0,leg_length*2+body_width/2.0+0.05] , size=[body_width,body_width,body_width])
    pyrosim.Send_Joint( name = "Torso_UpperLeg" , parent= "Torso" , child = "UpperLeg" ,\
    type = "revolute", position = [0,0,leg_length*2+0.05], jointAxis='0 1 0')
    pyrosim.Send_Cube(name="UpperLeg", pos=[0,0,-leg_length/2.0] , size=[0.1,0.1,leg_length])    
    pyrosim.Send_Joint( name = "UpperLeg_LowerLeg" , parent= "UpperLeg" , child = "LowerLeg" ,\
    type = "revolute", position = [0,0,-leg_length], jointAxis='0 1 0')
    pyrosim.Send_Cube(name="LowerLeg", pos=[0,0,-leg_length/2.0] , size=[0.1,0.1,leg_length])

    foot_width=0.1 #0.05
    pyrosim.Send_Joint( name = "LowerLeg_FrontFoot" , parent= "LowerLeg" , child = "FrontFoot" ,\
    type = "revolute", position = [0,0,-leg_length], jointAxis='0 1 0')
    pyrosim.Send_Cube(name="FrontFoot", pos=[0.25,0,-0.025,] , size=[0.5,foot_width,0.05])
    pyrosim.Send_Joint( name = "LowerLeg_BackFoot" , parent= "LowerLeg" , child = "BackFoot" ,\
    type = "revolute", position = [0,0,-leg_length], jointAxis='0 1 0')
    pyrosim.Send_Cube(name="BackFoot", pos=[-0.25,0,-0.025] , size=[0.5,foot_width,0.05])
    pyrosim.Send_Joint( name = "LowerLeg_RightFoot" , parent= "LowerLeg" , child = "RightFoot" ,\
    type = "revolute", position = [0,0,-leg_length], jointAxis='1 0 0')
    pyrosim.Send_Cube(name="RightFoot", pos=[0,-0.25,-0.025] , size=[foot_width,0.5,0.05])
    pyrosim.Send_Joint( name = "LowerLeg_LeftFoot" , parent= "LowerLeg" , child = "LeftFoot" ,\
    type = "revolute", position = [0,0,-leg_length], jointAxis='1 0 0')
    pyrosim.Send_Cube(name="LeftFoot", pos=[0,0.25,-0.025] , size=[foot_width,0.5,0.05])

    pyrosim.End()
    return

  def Generate_Brain(self,):
    pyrosim.Start_NeuralNetwork(f"./data/brain{self.myID}.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "UpperLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LowerLeg")
    pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "FrontFoot")
    pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "BackFoot")
    pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "RightFoot")
    pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "LeftFoot")

    pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Torso_UpperLeg")
    pyrosim.Send_Motor_Neuron(name = 8 , jointName = "UpperLeg_LowerLeg")
    pyrosim.Send_Motor_Neuron(name = 9 , jointName = "LowerLeg_FrontFoot")
    pyrosim.Send_Motor_Neuron(name = 10, jointName = "LowerLeg_BackFoot")
    pyrosim.Send_Motor_Neuron(name = 11, jointName = "LowerLeg_RightFoot")
    pyrosim.Send_Motor_Neuron(name = 12, jointName = "LowerLeg_LeftFoot")

    for currentRow  in range(c.numSensorNeurons):
      for currentColumn  in range(c.numMotorNeurons):
        pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , \
          weight = self.weights[currentRow][currentColumn] )
    pyrosim.End()
    return

  def Save_Brain(self, prefix=None):
    pyrosim.Start_NeuralNetwork(f"./data/brain{prefix}.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "UpperLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LowerLeg")
    pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "FrontFoot")
    pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "BackFoot")
    pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "RightFoot")
    pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "LeftFoot")

    pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Torso_UpperLeg")
    pyrosim.Send_Motor_Neuron(name = 8 , jointName = "UpperLeg_LowerLeg")
    pyrosim.Send_Motor_Neuron(name = 9 , jointName = "LowerLeg_FrontFoot")
    pyrosim.Send_Motor_Neuron(name = 10, jointName = "LowerLeg_BackFoot")
    pyrosim.Send_Motor_Neuron(name = 11, jointName = "LowerLeg_RightFoot")
    pyrosim.Send_Motor_Neuron(name = 12, jointName = "LowerLeg_LeftFoot")

    for currentRow  in range(c.numSensorNeurons):
      for currentColumn  in range(c.numMotorNeurons):
        pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , \
          weight = self.weights[currentRow][currentColumn] )
    pyrosim.End()
    return

