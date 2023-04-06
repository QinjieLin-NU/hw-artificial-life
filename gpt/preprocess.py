import argparse
from datetime import datetime

import src.data_preprocessing.data_downloader as data_downloader
import src.data_preprocessing.data_transformer as data_transformer
import src.data_preprocessing.constructor as constructor

def parse_args():
    parser = argparse.ArgumentParser(description='Option of preprocessing')
    parser.add_argument('--precision', type=int, help='precision')
    parser.add_argument('--instruction', action='store_true', help='Activate the flag (default: False)')
    return parser.parse_args()

if __name__=="__main__":
    data_dir = "../final/data"
    env_pattern = r"terrain\d+"
    seed_list = ["seed1234", "seed2345"] 
    brain_type = "ea"
    parsed_args = parse_args()
    
    # downloader = data_downloader.DataDownloader()
    # raw_file = downloader.download_file(data_dir, env_pattern, seed_list, brain_type, "./data/raw")
    # print("raw data file:",raw_file)
    raw_file = "./data/raw/data_2304061700.pkl"

    data_tf = data_transformer.DataTransformer()
    preprocessed_file = data_tf.generate_sequence(raw_file, save_dir="./data/preprocessed", subset=None, precision=parsed_args.precision)
    print("preprocessed_file data file:",preprocessed_file) 

    if parsed_args.instruction:
        # alpacaed_path = constructor.construct_alpaca_data(preprocessed_file, output_dir="./data/alpacaed")
        alpacaed_path = constructor.construct_alpaca_data_v2(preprocessed_file, output_dir="./data/alpacaed")  
        print("construct alpaca instructions dataframe:",alpacaed_path)
