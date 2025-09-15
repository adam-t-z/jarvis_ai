import subprocess
import time
import os

# === Configuration ===
audio_file = "test.mp3"
output_dir = "output"
model_size = "tiny"
device = "cpu"
compute_type = "int8"

# === Build Command ===
command = [
    "whisperx",
    audio_file,
    "--output_dir", output_dir,
    "--model", model_size,
    "--device", device,
    "--compute_type", compute_type
]

# === Run and Time ===
print(f"Running WhisperX on {audio_file}...")
start_time = time.time()

try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    duration = time.time() - start_time

    print("\n✅ Transcription completed.")
    print(f"⏱️  Time taken: {duration:.2f} seconds")
    print(f"📁 Output saved in: {os.path.abspath(output_dir)}")

except subprocess.CalledProcessError as e:
    print("\n❌ An error occurred while running WhisperX.")
    print("Command Output:")
    print(e.stdout)
    print("Error Output:")
    print(e.stderr)
