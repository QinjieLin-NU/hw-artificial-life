from datetime import datetime
from transformers import TrainingArguments

import src.data_preprocessing.data_downloader as data_downloader
import src.data_preprocessing.data_transformer as data_transformer
import src.model.trainer as trainer
import src.utils.seed_utils as seed_utils

if __name__=="__main__":
    # data_dir = "../final/data"
    # env_pattern = r"terrain\d+"
    # seed_list = ["seed1234", "seed2345"] 
    # brain_type = "ea"
    # rawdata_dir = "./data/raw"
    # proprocessdata_dir = "./data/preprocessed"
    
    # downloader = data_downloader.DataDownloader()
    # raw_file = downloader.download_file(data_dir, env_pattern, seed_list, brain_type, rawdata_dir)
    # print("raw data file:",raw_file)

    # data_tf = data_transformer.DataTransformer()
    # preprossed_file = data_tf.generate_sequence(raw_file, save_dir=proprocessdata_dir, subset=None)
    # print("preprossed_file data file:",preprossed_file) 

    preprossed_file = "./data/preprocessed/data_2304041728.pkl"
    trainer_output_dir = "./data/tutorial/model"
    trainer_save_dir = f"./data/tutorial/finetuned_model_{datetime.now().strftime('%y%m%d%H%M')}"
    seed = 2345 #1234 #42
    max_length = 512 #256 #128
    seed_utils.set_seeds(seed)
    dataset = data_transformer.preprocess_data(preprossed_file)
    training_args = TrainingArguments(
        output_dir=trainer_output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=100,
        save_total_limit=2,
    )
    trainer.train_gpt_model(
        dataset=dataset, 
        model_name_or_path="gpt2", 
        output_dir=trainer_output_dir, 
        trainer_save_dir=trainer_save_dir, 
        training_args=training_args,
        max_length=max_length)
