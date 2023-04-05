import numpy as np
import torch
from torch.utils.data import Dataset
from transformers import GPT2Config, DataCollatorForLanguageModeling, Trainer, TrainingArguments

from src.data_preprocessing.tokenizer import load_gpt_tokenizer
from src.model.gpt_model import load_gpt_model

class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, max_length):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]
        encoding = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=self.max_length)
        return {key: tensor.squeeze(0) for key, tensor in encoding.items()}

def train_gpt_model(dataset, model_name_or_path, 
    output_dir, trainer_save_dir, 
    training_args=None, max_length=128):
    # Load pre-trained GPT model and tokenizer
    model_name_or_path = "gpt2"
    tokenizer = load_gpt_tokenizer(model_name_or_path)
    model = load_gpt_model(model_name_or_path)
    config = GPT2Config.from_pretrained(model_name_or_path)
    # initialize torch dataset
    train_dataset = CustomDataset(data=dataset, tokenizer=tokenizer, max_length=max_length)
    if training_args is None:
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=1,
            per_device_train_batch_size=8,
            save_steps=10_000,
            save_total_limit=2,
        )    
    # Fine-tune the model using your dataset
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
        train_dataset=train_dataset,
    )
    trainer.train()
    trainer.save_model(trainer_save_dir)