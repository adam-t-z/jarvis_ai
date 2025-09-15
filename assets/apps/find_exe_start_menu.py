import os
import json
import win32com.client

# ✅ Only use the current user's Start Menu path
START_MENU_PATHS = [
    os.environ.get("APPDATA") + "\\Microsoft\\Windows\\Start Menu\\Programs"
]

def get_shortcut_target(path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    return shortcut.Targetpath

def create_app_mapping():
    app_map = {}
    for base in START_MENU_PATHS:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith(".lnk"):
                    full_path = os.path.join(root, file)
                    try:
                        target = get_shortcut_target(full_path)
                        if target and os.path.isfile(target):
                            name = os.path.splitext(file)[0].lower()
                            app_map[name] = target
                    except Exception as e:
                        print(f"Failed to resolve {full_path}: {e}")
    return app_map

def save_app_mapping(app_map, filename="apps.json"):
    with open(filename, "w") as f:
        json.dump(app_map, f, indent=4)
    print(f"✅ Saved {len(app_map)} apps to {filename}")

if __name__ == "__main__":
    apps = create_app_mapping()
    save_app_mapping(apps)
