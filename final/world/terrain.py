import os
import sys
import random

import pyrosim.pyrosim as pyrosim
from world.base import WorldBase

import numpy as np

class GridMap:
    def __init__(self, range_x, range_y, resolution):
        self.range_x = range_x
        self.range_y = range_y
        self.resolution = resolution

        self.num_cells_x = int((range_x[1] - range_x[0]) / resolution)
        self.num_cells_y = int((range_y[1] - range_y[0]) / resolution)

        self.grid_map = np.zeros((self.num_cells_x, self.num_cells_y))

    def get_cell(self, x, y):
        cell_x = int((x - self.range_x[0]) / self.resolution)
        cell_y = int((y - self.range_y[0]) / self.resolution)
        return self.grid_map[cell_x, cell_y]

    def set_cell(self, x, y, value):
        cell_x = int((x - self.range_x[0]) / self.resolution)
        cell_y = int((y - self.range_y[0]) / self.resolution)
        self.grid_map[cell_x, cell_y] = value

    def cell_position(self, cell_x, cell_y):
        x = self.range_x[0] + cell_x * self.resolution + self.resolution / 2
        y = self.range_y[0] + cell_y * self.resolution + self.resolution / 2
        return (x, y)

    def world_to_grid(self, x, y):
        grid_x = int((x - self.range_x[0]) / self.resolution)
        grid_y = int((y - self.range_y[0]) / self.resolution)
        return grid_x, grid_y

    def set_subrange(self, range_x, range_y, value):
        # Find the grid coordinates of the subrange
        start_x_grid, _ = self.world_to_grid(range_x[0], 0)
        end_x_grid, _ = self.world_to_grid(range_x[1], 0)
        _, start_y_grid = self.world_to_grid(0, range_y[0])
        _, end_y_grid= self.world_to_grid(0, range_y[1])

        for x in range(start_x_grid, end_x_grid ):
            for y in range(start_y_grid, end_y_grid):
                # self.set_cell(x, y, value)
                self.grid_map[x,y] = value

    def print_grid_map(self):
        print(self.grid_map)

class TerrainWorld(WorldBase):
  def __init__(self, fileName, initPos):
    super().__init__(fileName, initPos)
  
  def Create_SDF(self, roughness=None, resolution=0.25, range_x=(-0.5,4.5), range_y=(-1.5,1.5)):
    print("="*10,f"creating Terrain","="*10)
    pyrosim.Start_SDF(self.fileName)

    grid_map = GridMap(range_x, range_y, resolution)
    for x in range(grid_map.num_cells_x):
      for y in range(grid_map.num_cells_y):
        grid_height = random.random() / 10
        grid_map.grid_map[x,y] = grid_height
    grid_map.set_subrange((-0.5,0.5), range_y, 0.01)

    box_id = 0   
    for x in range(grid_map.num_cells_x):
      for y in range(grid_map.num_cells_y):
        (pos_x, pos_y) = grid_map.cell_position(x, y)
        mass=1000
        pyrosim.Send_Cube(name=f"terrain{box_id}", pos=[pos_x,pos_y,grid_map.grid_map[x,y]/2.0], 
          size=[grid_map.resolution,grid_map.resolution,grid_map.grid_map[x,y]], mass=mass)
        box_id+=1

    #add wall 
    super().Add_Wall(pyrosim, pos_y=1.8)
    pyrosim.End()
