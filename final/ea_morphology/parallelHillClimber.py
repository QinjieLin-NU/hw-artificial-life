import copy
import matplotlib.pyplot as plt
import numpy
import os
import ray
import random

from ea_morphology.solution import SOLUTION
import ea_morphology.constants as c

def set_seed(seedId):
  random.seed(seedId)
  numpy.random.seed(seedId)

class PARALLEL_HILL_CLIMBER:
  def __init__(self, seedId, envName):
    os.system(f"rm -r ./data/{envName}/seed{seedId}/body*")
    self.envName =  envName
    self.seedId = seedId
    set_seed(seedId)
    self.average_fitness_history = []
    self.parents = {}
    self.nextAvailableID = 0
    # for i in range(c.populationSize):
    #   self.parents[i] = SOLUTION(self.nextAvailableID, self.seedId, self.envName)
    #   self.nextAvailableID += 1
    ray.init()
    @ray.remote
    def Generate_SOLUTION(taskId, taskSeed, solutionSeed, envName):
      set_seed(taskSeed)
      s = SOLUTION(taskId, solutionSeed, envName)
      return s
    ray_seeds = [random.randint(0,10000) for i in range(c.populationSize)]
    ray_tasks = [Generate_SOLUTION.remote(i, ray_seeds[i], self.seedId,envName) for i in range(c.populationSize)]
    ray_results = ray.get(ray_tasks)
    self.parents = {index: element for index, element in enumerate(ray_results)}
    self.nextAvailableID += c.populationSize

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
    # for k in self.children.keys():
      # self.children[k].Mutate()
    @ray.remote
    def Mutate_Once(taskSeed, taskSolution, taskKey):
      set_seed(taskSeed)
      taskSolution.Mutate()
      return (taskKey, taskSolution)
    ray_seeds = [random.randint(0,10000) for  k in self.children.keys()]
    ray_tasks = [Mutate_Once.remote(ray_seeds[i], self.children[k], k) for  (i,k) in enumerate(self.children.keys())]
    ray_results = ray.get(ray_tasks)
    self.children = {index: element for index, element in ray_results}

  def Select(self):
    for k in self.parents.keys():
      if self.parents[k].fitness < self.children[k].fitness:
        self.parents[k] = self.children[k]

  def Print(self):
    print("="*30,f"iter{self.iter}","="*30)
    print("parents:",end=" ")
    for k in self.parents.keys():
      print("%.4f" % (self.parents[k]).fitness, end=" ")
    print()
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
    print(f"best parent of seed-{self.seedId}:",sorted_parents[-1][1].fitness)
    # plt.plot(self.average_fitness_history), plt.ylabel("Average fitness"), plt.xlabel("generation"), plt.show()
    sorted_parents[-1][1].Replay_Best()
    os.system(f"cp -r ./data/{self.envName}/seed{self.seedId}/body{sorted_parents[-1][1].m_id} ./data/{self.envName}/seed{self.seedId}/bodybest")
