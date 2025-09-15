import os
import time
import requests  # Use the requests library for HTTP requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Ensure the API key is loaded
if not api_key:
    print("Error: OPENROUTER_API_KEY is not set in the .env file.")
    exit(1)

# OpenRouter API URL
api_url = "https://openrouter.ai/api/v1/chat/completions"  # This might need adjustment based on OpenRouter's actual endpoint

# Test function to measure speed and check connection
def test_openrouter_speed():
    try:
        # Simple prompt to test the connection and speed
        prompt = "Answer in a conversational manner. What is the capital of Saudi?"

        # Define the payload (the data we're sending to the API)
	# openrouter/sonoma-dusk-alpha    ==> fastest
	# openrouter/sonoma-sky-alpha
	# mistralai/mistral-small-3.2-24b-instruct:free   ==> pretty close to the above two
	# mistralai/mistral-7b-instruct:free
	# cognitivecomputations/dolphin-mistral-24b-venice-edition:free  ==> longest answer I think
	# google/gemma-3n-e2b-it:free
	# deepseek/deepseek-chat-v3-0324:free
	# nvidia/nemotron-nano-9b-v2:free
        data = {
            "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",  # Model name, adjust if needed
            "messages": [{"role": "user", "content": prompt}]
        }

        # Define the headers, including the API key for authentication
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Record the start time
        start_time = time.time()

        # Send the request to OpenRouter
        response = requests.post(api_url, json=data, headers=headers)

        # Check for rate limit error (429) and handle it
        if response.status_code == 429:
            reset_time = response.headers.get('Retry-After', 60)  # Default to 60 seconds if Retry-After is not provided
            print(f"Rate limit hit. Retrying after {reset_time} seconds...")
            time.sleep(int(reset_time))  # Wait for the specified duration
            return test_openrouter_speed()  # Retry the request

        # Calculate the time taken for the request to complete
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Check if the response was successful (status code 200)
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                output_text = response_data['choices'][0]['message']['content']
                print(f"Response: {output_text}")
                print(f"Time taken for the request: {elapsed_time:.2f} seconds")
            else:
                print("Error: No valid response from OpenRouter.")
        else:
            print(f"Error: Received status code {response.status_code} from OpenRouter.")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Run the test
test_openrouter_speed()
