from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer from Hugging Face
model_name = "gpt2"  # You can replace with "gpt2-medium", "gpt2-large", or "gpt2-xl" for larger models

tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Encode input text (this will be the prompt)
input_text = "The capital of UAE is... "
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate text from the model
output = model.generate(input_ids, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)

# Decode the generated output and print it
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
