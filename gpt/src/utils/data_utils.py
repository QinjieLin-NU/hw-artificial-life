from datetime import datetime
import numpy as np
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

    def round_str(self, precision=None):
        if not precision:
            return f"grid map: {self.sdf_sequence}, goal: {self.goal_sequence}, urdf: {self.urdf_sequence}, score: {self.score_sequence}"
        else:
            round_sdf_sequence, round_urdf_sequence, round_goal_sequence, round_score_sequence = self.round_sequence(precision)
            return f"grid map: {round_sdf_sequence}, goal: {round_goal_sequence}, urdf: {round_urdf_sequence}, score: {round_score_sequence}"
        
    def round_sequence(self, precision=None):
        round_sdf_sequence = np.round(self.sdf_sequence,precision)
        round_urdf_sequence = [
            tuple(round(x, precision) if isinstance(x, float) else x for x in sublist)
            if not isinstance(sublist, str)
            else sublist
            for sublist in [
                (x if not isinstance(x, tuple) else tuple(round(y, precision) if isinstance(y, float) else y for y in x) for x in seq
                )
                for seq in self.urdf_sequence
            ]
        ]
        round_goal_sequence = tuple([round(x,precision) for x in self.goal_sequence])
        round_score_sequence =  tuple([round(x,precision) for x in self.score_sequence])
        return round_sdf_sequence, round_urdf_sequence, round_goal_sequence, round_score_sequence

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