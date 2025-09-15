from llama_cpp import Llama
import time

# Initialize the model
llm = Llama(
    model_path="./TinyLlama-1.1B-Chat-v1.0-Q4_K_S.gguf",  # Path to your GGUF model file
    n_ctx=4096,  # Increased context size for better coherence
    n_threads=8,  # Use more threads if your CPU has many cores (adjust based on your machine)
    use_fp16=True  # Enable half-precision if your model and hardware support it
)

# Define a more structured prompt
prompt = """
Write a short story about a brave knight who embarks on a quest to find a legendary treasure hidden deep within a dangerous forest. 
The forest is full of mystical creatures, and the knight must solve riddles to pass through. 
Make the story exciting, mysterious, and full of twists and turns. 
Start by describing the knight and their motivation for the quest. 
Then, introduce the mystical creatures and riddles that challenge the knight. 
Finally, make sure the ending is a surprising twist that leaves the reader wondering.
"""

# Measure the time taken to generate a response
start_time = time.time()

# Generate a response with adjusted max_tokens, temperature, and top_p for better creativity
response = llm(prompt, max_tokens=800, temperature=0.7, top_p=0.95)

# Calculate the elapsed time
elapsed_time = time.time() - start_time

# Print the response and the time it took
print(f"Response: {response}")
print(f"Time taken: {elapsed_time:.4f} seconds")
