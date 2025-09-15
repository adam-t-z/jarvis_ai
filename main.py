# main.py
from dotenv import load_dotenv
load_dotenv()

from core.voice_input import listen, listen_with_timeout
from core.command_router import route_command
from core.conversation import handle_conversation
from core.tts import speak
from core.wake_word_listener import listen_continuously, SAMI_WAKE_WORDS

def handle_wake_word_activation(wake_word: str):
    """Handle actions when wake word is detected."""
    # Only respond to "Sami" - enter continuous conversation mode
    if wake_word.lower() == "sami":
        speak("Yes, Sir?")
        
        # Enter continuous conversation mode
        sami_continuous_mode()

def sami_continuous_mode():
    """Continuous conversation mode for Sami - stays active until dismissed."""
    # Exit phrases that end the conversation
    exit_phrases = [
        "that's all", "thats all", "that is all",
        "bye", "goodbye", "stop listening", "stop", 
        "enough", "dismiss", "thank you that's all"
    ]
    
    conversation_count = 0
    
    try:
        while True:
            # Listen for the next command/conversation with 15-second timeout
            command = listen_with_timeout(15)
            
            # Handle timeout case
            if command == "TIMEOUT":
                speak("I haven't heard anything for a while, Sir. I'll return to silent mode now.")
                print("🤫 Sami AI Assistant returning to silent mode")
                break
            
            if not command or not command.strip():
                # If no command, prompt gently
                if conversation_count == 0:
                    speak("How may I assist you, Sir?")
                else:
                    speak("Anything else, Sir?")
                continue
            
            conversation_count += 1
            command_lower = command.lower().strip()
            
            # Check for exit phrases
            if any(phrase in command_lower for phrase in exit_phrases):
                # Polite dismissal
                if "thank" in command_lower:
                    speak("You're welcome, Sir. I live to serve.")
                else:
                    speak("Very well, Sir. I'll be here if you need me.")
                break
            
            # Check if user is calling Sami again (reinforcement)
            if any(word in command_lower.split() for word in SAMI_WAKE_WORDS):
                speak("Yes, Sir? I'm still listening.")
                continue
            
            # Process the command through normal routing
            try:
                handled = route_command(command)
                
                # If not handled by command router, use conversational AI
                if not handled:
                    handle_conversation(command)
                
            except Exception as e:
                speak("I apologize, Sir. I encountered an error. Please try again.")
                
    except KeyboardInterrupt:
        speak("Goodbye, Sir.")
    except Exception as e:
        speak("I apologize, Sir. I need to step away for a moment.")
def main():
    """Main application loop with wake word detection."""
    print("🤫 Sami AI Assistant running in silent mode")
    
    try:
        # Start wake word detection using speech recognition
        listen_continuously(handle_wake_word_activation)
            
    except KeyboardInterrupt:
        speak("Goodbye, Sir!")
    except Exception as e:
        print(f"Failed to start Sami AI: {e}")


if __name__ == "__main__":
    main()
