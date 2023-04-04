"""
pandas_raw_dataframe:
env_name, brain_name, search_seed, env_seed, env_sdf(string), goal(x,10), robot_urdf(string), score(x,1.15),

transformed_dataframe:
env_grid_map, (4x4) 
goal, (1x3)
robor_urdf (node_name, link_type, link_size, sensor_tag) 
1 (parent_name, node_name, joint_axis, joint_type)  (node_name, link_type, link_size, sensor_tag)
2 (parent_name, joint_axis, joint_type, node_name, link_type, link_size, sensor_tag, sensor_tag)
score_pos, (1x3)

tokenize_dataframe:
"""
from datetime import datetime
import os
import pickle
import re

from src.utils.data_utils import RawData as RawData
from src.utils.data_utils import save_data as save_data

def read_file(file_path):
    with open(file_path,"r") as f:
        file_str = f.read()
    return file_str

def read_rawdata(data_dir, env_pattern, seed_list, brain_type, 
fitness_file, body_file, brain_file, world_file):
    raw_data_dirs = []
    raw_data_list = []
    for e in os.listdir(data_dir):
        env_path = os.path.join(data_dir,e)
        match = re.match(r"[A-Za-z]+(\d+)", e)
        if match:
            env_seed = int(match.group(1))
        if os.path.isdir(env_path) and re.match(env_pattern,e):
            for s in os.listdir(env_path):
                seed_path = os.path.join(env_path,s)
                if os.path.isdir(seed_path) and (s in seed_list):
                    for b in os.listdir(seed_path):
                        if re.match(r"body\d+",b):
                            body_path = os.path.join(seed_path,b)
                            raw_data_dirs.append(body_path)
                            raw_data = RawData(
                                env_name=e,
                                brain_name=brain_type,
                                search_seed=s,
                                env_seed=env_seed,
                                env_sdf=read_file(os.path.join(env_path, world_file)),
                                goal=(100, 0, 0),
                                robot_urdf=read_file(os.path.join(body_path, body_file)),
                                score=(float(read_file(os.path.join(body_path, fitness_file))), 0 , 0),
                            )
                            raw_data_list.append(raw_data)
    return raw_data_list

class DataDownloader:
    def __init__(self):
        self.fitness_file = "best_fitness.txt"
        self.body_file = "body.urdf"
        self.brain_file = "brain-100.nndf"
        self.world_file = "world.sdf"

    def download_file(self, data_dir="../final/data", env_pattern =r"terrain\d+",
    seed_list = ["seed1234", "seed2345"], brain_type = "ea", saving_dir="./data/raw"):
        raw_data_list = read_rawdata(data_dir, env_pattern, seed_list, brain_type,
        self.fitness_file, self.body_file, self.brain_file, self.world_file)
        file_path = save_data(saving_dir, raw_data_list)
        return file_path

if __name__=="__main__":
    data_dir = "../final/data"
    env_pattern = r"terrain\d+"
    seed_list = ["seed1234", "seed2345"] 
    brain_type = "ea"
    saving_dir = "../../data/raw"

    fitness_file = "best_fitness.txt"
    body_file = "body.urdf"
    brain_file = "brain-100.nndf"
    world_file = "world.sdf"
    
    raw_data_list = read_rawdata(data_dir, env_pattern, seed_list, brain_type,
        fitness_file, body_file, brain_file, world_file, saving_dir)
    save_data(raw_data_list)