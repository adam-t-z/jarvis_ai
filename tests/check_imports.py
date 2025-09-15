import time

start = time.time()
from core.tts import speak
print("tts loaded in", time.time() - start)

start = time.time()
from skills.system.app_launcher import launch_notepad, launch_app, load_app_mappings
print("app_launcher loaded in", time.time() - start)

start = time.time()
from skills.general.hello_skill import say_hello
print("hello_skill loaded in", time.time() - start)

start = time.time()
from skills.browser_skill import run_browser_task_sync
print("browser_skill loaded in", time.time() - start)
