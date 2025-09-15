# core/command_router.py

from core.tts import speak
from skills.system.app_launcher import launch_notepad, launch_app, load_app_mappings
from skills.general.hello_skill import say_hello
import re
 

def route_command(command):
    """Route commands to appropriate handlers. Returns True if handled, False otherwise."""
    command_lower = command.lower().strip()
 
    # Handle hello/greeting commands
    if any(word in command_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        say_hello()
        return True

    # Handle app launching commands
    elif any(phrase in command_lower for phrase in ["open", "launch", "start", "run"]):
        app_name = extract_app_name(command_lower)
        if app_name:
            speak(f"Opening {app_name}, Sir.")
            success = launch_app(app_name)
            if not success:
                speak(f"I apologize, Sir. I couldn't open {app_name}.")
            return True
        else:
            speak("What application would you like me to open, Sir?")
            return True

    # Handle specific notepad command for backward compatibility
    elif "notepad" in command_lower:
        speak("Opening Notepad, Sir.")
        launch_notepad()
        return True

    # Handle empty commands
    elif command_lower == "":
        speak("Sorry, I didn't catch that.")
        return True

    # Unknown command → return False so LLM can handle it
    return False

def extract_app_name(command):
    """Extract app name from voice command."""
    # Remove common command words
    command = re.sub(r'\b(open|launch|start|run|please|can you|could you)\b', '', command)
    command = command.strip()
    
    # Load app mappings to check against known apps
    app_map = load_app_mappings()
    
    # Try to find exact matches first
    words = command.split()
    
    # Check for multi-word app names
    for i in range(len(words), 0, -1):
        for j in range(len(words) - i + 1):
            potential_app = ' '.join(words[j:j+i])
            if potential_app in app_map:
                return potential_app
    
    # If no exact match, return the cleaned command for fuzzy matching
    return command if command else None
