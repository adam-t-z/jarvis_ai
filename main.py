import time
from dotenv import load_dotenv
load_dotenv()

from core.voice_input import listen, listen_with_timeout
from core.command_router import route_command
from core.conversation import handle_conversation
from core.tts import speak
from core.wake_word_listener import listen_continuously, SARAH_WAKE_WORDS

import warnings
warnings.filterwarnings("ignore")


def handle_wake_word_activation(wake_word: str):
    print(f"[DEBUG] Wake word detected: {wake_word}")
    start = time.time()

    print(wake_word)
    # Only respond to "Sarah" - enter continuous conversation mode
    if wake_word.lower() == "sarah":
        print("[DEBUG] Responding to wake word...")
        speak("Yes, Sir?")
        
        print("[DEBUG] Entering continuous conversation mode...")
        sarah_continuous_mode()

    print(f"[DEBUG] handle_wake_word_activation finished in {time.time() - start:.2f} seconds")


def sarah_continuous_mode():
    """Continuous conversation mode for Sarah - stays active until dismissed."""
    exit_phrases = [
        "that's all", "thats all", "that is all",
        "bye", "goodbye", "stop listening", "stop", 
        "enough", "dismiss", "thank you that's all"
    ]
    
    conversation_count = 0
    
    try:
        while True:
            print("[DEBUG] Listening for command (timeout 15s)...")
            listen_start = time.time()
            command = listen_with_timeout(15)
            listen_duration = time.time() - listen_start
            print(f"[DEBUG] listen_with_timeout returned in {listen_duration:.2f} seconds: '{command}'")

            if command == "TIMEOUT":
                speak("I haven't heard anything for a while, Sir. I'll return to silent mode now.")
                print("🤫 Sarah AI Assistant returning to silent mode")
                break
            
            if not command or not command.strip():
                if conversation_count == 0:
                    speak("How may I assist you, Sir?")
                else:
                    speak("Anything else, Sir?")
                continue
            
            conversation_count += 1
            command_lower = command.lower().strip()
            
            if any(phrase in command_lower for phrase in exit_phrases):
                speak("You're welcome, Sir. I live to serve.")
                break
            
            if any(word in command_lower.split() for word in SARAH_WAKE_WORDS):
                speak("Yes, Sir? I'm still listening.")
                continue
            
            # Process the command through normal routing
            try:
                print(f"[DEBUG] Routing command: {command}")
                route_start = time.time()
                handled = route_command(command)
                route_duration = time.time() - route_start
                print(f"[DEBUG] route_command took {route_duration:.2f} seconds, handled={handled}")
                
                if not handled:
                    print("[DEBUG] Handling conversation with LLM...")
                    conv_start = time.time()
                    handle_conversation(command)
                    conv_duration = time.time() - conv_start
                    print(f"[DEBUG] handle_conversation took {conv_duration:.2f} seconds")
                
            except Exception as e:
                speak("I apologize, Sir. I encountered an error. Please try again.")
                print(f"[ERROR] Exception in command processing: {e}")
                
    except KeyboardInterrupt:
        speak("Goodbye, Sir.")
    except Exception as e:
        speak("I apologize, Sir. I need to step away for a moment.")
        print(f"[ERROR] Exception in sarah_continuous_mode: {e}")

def main():
    print("🤫 Sarah AI Assistant starting...")
    start = time.time()
    
    try:
        print("Initializing wake word detection...")
        listen_continuously(handle_wake_word_activation)
    except KeyboardInterrupt:
        speak("Goodbye, Sir!")
    except Exception as e:
        print(f"Failed to start Sarah AI: {e}")
    
    print(f"Startup + run time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
