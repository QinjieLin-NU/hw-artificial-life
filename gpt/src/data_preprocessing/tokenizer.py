from transformers import GPT2Tokenizer

def load_gpt_tokenizer(pretrained_model_name_or_path):
    tokenizer = GPT2Tokenizer.from_pretrained(pretrained_model_name_or_path)
    pad_token_exists = tokenizer.pad_token is not None
    if not pad_token_exists:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer
