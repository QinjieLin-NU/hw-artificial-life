import numpy

import ea.constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:
  def __init__(self,linkName):
    self.linkName = linkName
    self.Prepare_To_Sense()

  def Prepare_To_Sense(self):
    self.values = numpy.zeros(c.length)

  def Get_Value(self, timestep):
    sensor_value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
    self.values[timestep] = sensor_value

  def Save_Values(self):
    with open(f"./data/{self.linkName}_sensor_values.txt",'wb') as f:
      numpy.save(f, self.values)