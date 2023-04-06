import pandas as pd

from src.utils.data_utils import read_data as read_data
from src.utils.data_utils import save_df as save_df

def construct_alpaca_data(preprocessed_file, output_dir="./data/alpacaed"):
    preprocessed_data = read_data(preprocessed_file)
    df = pd.DataFrame(columns=["instruction", "input_sequence", "output_sequence"])
    for single_data in preprocessed_data:
        sdf_sequence, goal_sequence, urdf_sequence, score_sequence = \
            single_data.sdf_sequence,  single_data.goal_sequence, single_data.urdf_sequence, single_data.score_sequence
        instruction = "Based on the following gridmap and goal, give me the robot description and its score"
        input_sequence = f"Grid map is {sdf_sequence}, the goal position is {goal_sequence}."
        output_sequence = f"Robot description is {urdf_sequence}, its final position is {score_sequence}"
        row_data = pd.DataFrame({"instruction": [instruction], "input_sequence": [input_sequence], "output_sequence": [output_sequence]})
        # df = df.append(row_data, ignore_index=True)
        df = pd.concat([df, row_data], ignore_index=True)
    df_path = save_df(output_dir, df)
    return df_path

def construct_alpaca_data_v2(preprocessed_file, output_dir="./data/alpacaed"):
    preprocessed_data = read_data(preprocessed_file)
    df = pd.DataFrame(columns=["instruction", "input_sequence", "output_sequence"])
    for single_data in preprocessed_data:
        sdf_sequence, goal_sequence, urdf_sequence, score_sequence = \
            single_data.sdf_sequence,  single_data.goal_sequence, single_data.urdf_sequence, single_data.score_sequence
        instruction = "Based on the following gridmap, goal, and final position, give me the robot description"
        input_sequence = f"Grid map is {sdf_sequence}, the goal position is {goal_sequence}, its final position is {score_sequence}"
        output_sequence = f"Robot description is {urdf_sequence},"
        row_data = pd.DataFrame({"instruction": [instruction], "input_sequence": [input_sequence], "output_sequence": [output_sequence]})
        # df = df.append(row_data, ignore_index=True)
        df = pd.concat([df, row_data], ignore_index=True)
    df_path = save_df(output_dir, df)
    return df_path