from core.openrouter_client import OpenRouterClient
from core.tts import speak

# Initialize client with error handling
try:
    client = OpenRouterClient()
except ValueError as e:
    print(f"⚠️ {e}")
    client = None

def handle_conversation(user_text):
    """Handle conversational responses using LLM."""
    if not client:
        speak("Sorry, I'm unable to process that request right now.")
        return None
        
    if not user_text or not user_text.strip():
        speak("I didn't catch that. Could you repeat?")
        return None
    
    messages = [
        {
            "role": "system", 
            "content": "Your name is Sami, a helpful and respectful AI assistant. "
                      "You are speaking to your user who you address as 'Sir'. "
                      "Be polite, concise, and helpful. Avoid emojis in responses. "
                      "Keep responses brief and natural for voice interaction."
        },
        {"role": "user", "content": user_text.strip()}
    ]
    
    response = client.get_response(messages)
    
    if response:
        speak(response)
        return response
    else:
        fallback_msg = "I'm sorry, I couldn't process that request."
        speak(fallback_msg)
        return fallback_msg
