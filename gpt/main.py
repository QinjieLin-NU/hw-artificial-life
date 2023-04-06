from datetime import datetime
from transformers import TrainingArguments

import src.model.trainer as trainer
from src.utils.data_utils import read_data as read_data

if __name__=="__main__":
    preprocessed_file = "./data/preprocessed/data_2304041728.pkl"
    trainer_output_dir = "./data/tutorial/model"
    trainer_save_dir = f"./data/tutorial/finetuned_model_{datetime.now().strftime('%y%m%d%H%M')}"
    
    preprocessed_data = read_data(preprocessed_file)
    dataset = [seq.round_str(2) for seq in preprocessed_data]
    seed = 2345 #1234 #42
    max_length = 512 #256 #128
    training_args = TrainingArguments(
        output_dir=trainer_output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=100,
        save_total_limit=2,
        seed=seed,
    )
    trainer.train_gpt_model(
        dataset=dataset, 
        model_name_or_path="gpt2", 
        output_dir=trainer_output_dir, 
        trainer_save_dir=trainer_save_dir, 
        training_args=training_args,
        max_length=max_length)
