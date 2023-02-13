import copy
import matplotlib.pyplot as plt
import os

from ea.creature import Generate_Snake,Create_World
from ea.solution import SOLUTION
import ea.constants as c

class PARALLEL_HILL_CLIMBER:
  def __init__(self):
    os.system("rm ./data/brain*.nndf"), os.system("rm ./data/fitness*.txt"), os.system("rm ./data/tmp*.txt") 
    self.parents = {}
    self.nextAvailableID = 0

    links,joints = Generate_Snake()
    Create_World()
    for i in range(c.populationSize):
      self.parents[i] = SOLUTION(self.nextAvailableID, links, joints)
      self.nextAvailableID += 1
    self.average_fitness_history = []

  def Evolve(self):
    self.Evaluate(self.parents)
    for currentGeneration in range(c.numberOfGenerations):
      self.iter = currentGeneration
      self.Evolve_For_One_Generation()
    pass
  
  def Evolve_For_One_Generation(self):
    self.Spawn()
    self.Mutate()
    self.Evaluate(self.children)
    self.Print()
    self.Select()
    self.Save()
  
  def Evaluate(self, solutions, directOrGUI='DIRECT'):
    for k in solutions.keys():
      solutions[k].Start_Simulation(directOrGUI)
    for k in solutions.keys():
      solutions[k].Wait_For_Simulation_To_End()

  def Spawn(self):
    self.children = {}
    for k in self.parents.keys():
      self.children[k] = copy.deepcopy(self.parents[k])
      self.children[k].Set_ID(self.nextAvailableID)
      self.nextAvailableID += 1

  def Mutate(self):
    for k in self.children.keys():
      self.children[k].Mutate()

  def Select(self):
    for k in self.parents.keys():
      if self.parents[k].fitness < self.children[k].fitness:
        self.parents[k] = self.children[k]

  def Print(self):
    print("="*30,f"iter{self.iter}","="*30)
    print("parents:",end=" ")
    for k in self.parents.keys():
      print("%.4f" % (self.parents[k]).fitness, end=" ")
    print("childrens:",end=" ")
    for k in self.children.keys():
      print("%.4f" % self.children[k].fitness, end=" ")
    print()
    # print("="*50)
  
  def Save(self):
    avg_fit= sum([self.parents[k].fitness for k in self.parents.keys()])/len(self.parents)
    self.average_fitness_history.append(avg_fit)

  def Show_Best(self):
    sorted_parents = sorted(self.parents.items(), key=lambda x: x[1].fitness)
    print(f"best parent of seed-{c.seed}:",sorted_parents[-1][1].fitness)
    # plt.plot(self.average_fitness_history), plt.ylabel("Average fitness"), plt.xlabel("generation"), plt.show()
    sorted_parents[-1][1].Start_Simulation('GUI')
    sorted_parents[-1][1].Generate_Brain("-100")

