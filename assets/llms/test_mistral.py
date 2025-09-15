import requests

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get values from environment
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("HF_API_URL")

# Headers for the API request, including the Authorization Bearer Token
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

# Function to query the Hugging Face model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Query payload (chat with a user message)
response = query({
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"
})

# Print the model's response
print(response["choices"][0]["message"])
