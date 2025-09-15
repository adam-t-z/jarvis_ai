from faster_whisper import WhisperModel
import time

# Load model
model_size = "tiny"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Transcribe
start = time.time()
segments, info = model.transcribe("test.mp3")
end = time.time()

# Output transcription
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

print(f"\n⏱️ Transcription took {end - start:.2f} seconds")
