from transformers import GPT2LMHeadModel, GPT2Config

def load_gpt_model(pretrained_model_name_or_path):
    config = GPT2Config.from_pretrained(pretrained_model_name_or_path)
    model = GPT2LMHeadModel.from_pretrained(pretrained_model_name_or_path, config=config)
    return model

def load_fine_tuned_gpt_model(model_dir):
    config = GPT2Config.from_pretrained(model_dir)
    model = GPT2LMHeadModel.from_pretrained(model_dir, config=config)
    return model