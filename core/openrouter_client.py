import os
import requests
import time
from typing import List, Dict, Optional

class OpenRouterClient:
    def __init__(self, api_key=None, model="openrouter/sonoma-dusk-alpha", timeout=30, max_retries=3):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.timeout = timeout
        self.max_retries = max_retries

    def get_response(self, messages: List[Dict]) -> Optional[str]:
        """Get response from OpenRouter with error handling and retries."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": messages
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url, 
                    headers=headers, 
                    json=data, 
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
            except requests.exceptions.Timeout:
                print(f"⏱️ Request timeout (attempt {attempt + 1}/{self.max_retries})")
            except requests.exceptions.ConnectionError:
                print(f"🌐 Connection error (attempt {attempt + 1}/{self.max_retries})")
            except requests.exceptions.HTTPError as e:
                print(f"🚨 HTTP error: {e.response.status_code} (attempt {attempt + 1}/{self.max_retries})")
            except KeyError:
                print("❌ Unexpected response format from OpenRouter")
                return None
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return None
            
            if attempt < self.max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
        
        print("❌ Failed to get response after all retries")
        return None
