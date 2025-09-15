import json
import subprocess
import os
from difflib import get_close_matches


apps_json = r"C:\Users\alpha\projects\jarvis_ai\assets\apps\apps.json"

# --- Load the app mappings from a JSON file ---
def load_app_mappings(filepath=apps_json ):
    with open(filepath, 'r') as f:
        return json.load(f)

# --- Try to open the app if it exists ---
def open_app(app_name, app_map):
    app_name = app_name.lower()
    if app_name in app_map:
        path = app_map[app_name]
        if os.path.exists(path) or path.endswith('.exe') or path in ['notepad.exe', 'calc.exe']:
            subprocess.Popen([path])
            print(f"✅ Opening {app_name}")
        else:
            print(f"⚠️ Path not found for {app_name}: {path}")
    else:
        print(f"❌ App '{app_name}' not found in mapping.")

# --- Fuzzy match user input to closest known app name ---
def fuzzy_find_app(user_input, app_map):
    keys = app_map.keys()
    matches = get_close_matches(user_input.lower(), keys, n=1, cutoff=0.6)
    return matches[0] if matches else None

# --- Simple test loop: enter command like "open chrome" ---
def test_open_app():
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
