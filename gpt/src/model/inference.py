from src.data_preprocessing.tokenizer import load_gpt_tokenizer
from src.model.gpt_model import load_fine_tuned_gpt_model

def generate_text(prompt, tokenizer_name_or_path, model_dir, max_length=50, num_return_sequences=1):
    tokenizer = load_gpt_tokenizer(tokenizer_name_or_path)
    model = load_fine_tuned_gpt_model(model_dir)

    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    output_sequences = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_p=0.95,
        top_k=50,
    )

    generated_sequences = []
    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        generated_sequence = generated_sequence.tolist()
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)
        generated_sequences.append(text)

    return generated_sequences