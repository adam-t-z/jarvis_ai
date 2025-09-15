import json
import subprocess
import os
from difflib import get_close_matches

# --- Load the app mappings from a JSON file ---
def load_app_mappings(filepath='assets/apps/apps.json'):
    """Load app mappings from JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Could not find app mappings file: {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"⚠️ Error reading JSON file: {filepath}")
        return {}

# --- Try to open the app if it exists ---
def open_app(app_name, app_map):
    """Open an application by name using the app mapping."""
    app_name = app_name.lower()
    if app_name in app_map:
        path = app_map[app_name]
        if os.path.exists(path) or path.endswith('.exe') or path in ['notepad.exe', 'calc.exe']:
            try:
                subprocess.Popen([path])
                print(f"✅ Opening {app_name}")
                return True
            except Exception as e:
                print(f"⚠️ Error opening {app_name}: {e}")
                return False
        else:
            print(f"⚠️ Path not found for {app_name}: {path}")
            return False
    else:
        print(f"❌ App '{app_name}' not found in mapping.")
        return False

# --- Fuzzy match user input to closest known app name ---
def fuzzy_find_app(user_input, app_map):
    """Find the closest matching app name using fuzzy matching."""
    keys = app_map.keys()
    matches = get_close_matches(user_input.lower(), keys, n=1, cutoff=0.6)
    return matches[0] if matches else None

# --- Launch app by name with fuzzy matching ---
def launch_app(app_name):
    """Launch an app by name, with fuzzy matching support."""
    app_map = load_app_mappings()
    if not app_map:
        print("⚠️ No app mappings available")
        return False
    
    # Try exact match first
    if open_app(app_name, app_map):
        return True
    
    # Try fuzzy match
    matched_app = fuzzy_find_app(app_name, app_map)
    if matched_app:
        print(f"🔍 Did you mean '{matched_app}'?")
        return open_app(matched_app, app_map)
    
    print(f"❓ Could not find app matching '{app_name}'")
    return False

# --- Legacy function for backward compatibility ---
def launch_notepad():
    """Launch notepad - legacy function for backward compatibility."""
    return launch_app("notepad")

# --- Simple test loop: enter command like "open chrome" ---
def test_open_app():
    """Test function to interactively launch apps."""
    app_map = load_app_mappings()

    while True:
        user_input = input("🗣️ Say something (or type 'exit'): ").strip().lower()

        if user_input == 'exit':
            print("👋 Goodbye!")
            break

        # Try to extract app name (very simple logic for demo)
        words = user_input.split()
        for word in words:
            matched_app = fuzzy_find_app(word, app_map)
            if matched_app:
                open_app(matched_app, app_map)
                break
        else:
            print("❓ Couldn't understand which app to open.")

# --- Run the test ---
if __name__ == "__main__":
    test_open_app()
