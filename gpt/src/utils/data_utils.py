from datetime import datetime
import os
import pickle
import re

class RawData:
    def __init__(
        self,
        env_name,
        brain_name,
        search_seed,
        env_seed,
        env_sdf,
        goal,
        robot_urdf,
        score,
    ):
        self.env_name = env_name
        self.brain_name = brain_name
        self.search_seed = search_seed
        self.env_seed = env_seed
        self.env_sdf = env_sdf
        self.goal = goal
        self.robot_urdf = robot_urdf
        self.score = score

    def __str__(self):
        return (
            f"Data(\n"
            f"  env_name={self.env_name},\n"
            f"  brain_name={self.brain_name},\n"
            f"  search_seed={self.search_seed},\n"
            f"  env_seed={self.env_seed},\n"
            f"  env_sdf={self.env_sdf[0:50]},\n"
            f"  goal={self.goal},\n"
            f"  robot_urdf={self.robot_urdf[0:50]},\n"
            f"  score={self.score}\n"
            ")"
        )

class PreprocessedData:
    def __init__(
        self,
        sdf_sequence,
        goal_sequence,
        urdf_sequence,
        score_sequence,
    ):
        self.sdf_sequence = sdf_sequence
        self.goal_sequence = goal_sequence
        self.urdf_sequence = urdf_sequence
        self.score_sequence = score_sequence

    def __str__(self):
        return f"grid map: {self.sdf_sequence}, goal: {self.goal_sequence}, urdf: {self.urdf_sequence}, score: {self.score_sequence}"

def save_data(file_dir, input_data):
    now = datetime.now()
    formatted_now = now.strftime("%y%m%d%H%M")
    file_path = f"{file_dir}/data_{formatted_now}.pkl"
    with open(file_path, "wb") as file:
        pickle.dump(input_data, file)
    return file_path

def read_data(file_path):
    with open(f"{file_path}", "rb") as file:
        loaded_data = pickle.load(file)
    return loaded_data