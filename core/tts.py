from kokoro import KPipeline
import sounddevice as sd
import soundfile as sf
import os
import threading  # Use threading to avoid blocking the main thread during initialization

# Global variables
pipeline = None
initialized = False

def initialize_pipeline():
    global pipeline, initialized
    if not initialized:
        print("🔄 Initializing TTS pipeline...")
        pipeline = KPipeline(lang_code='a')
        pipeline.load_voice('af_heart')
        _ = list(pipeline("Warming up.", voice='af_heart'))
        initialized = True
        print("✅ TTS pipeline ready.")

# Start the TTS initialization in a separate thread
def start_initialization():
    threading.Thread(target=initialize_pipeline, daemon=True).start()

# Start initialization as soon as the script is loaded
start_initialization()

# Pre-recorded responses
AUDIO_RESPONSES = {
    "yes, sir?": "audio_responses/yes_sir.wav",
    "how may i assist you, sir?": "audio_responses/how_may_i_assist.wav",
    "anything else, sir?": "audio_responses/anything_else.wav",
    "you're welcome, sir. i live to serve.": "audio_responses/youre_welcome.wav",
    "goodbye, sir!": "audio_responses/goodbye.wav",
}

def speak(text: str, voice: str = 'af_heart'):
    print(f"Assistant: {text}")
    try:
        key = text.strip().lower()
        if key in AUDIO_RESPONSES:
            filepath = AUDIO_RESPONSES[key]
            if os.path.isfile(filepath):
                audio, samplerate = sf.read(filepath)
                sd.play(audio, samplerate=samplerate)
                sd.wait()
                return
            else:
                print(f"⚠️ Audio file not found: {filepath}")

        # Ensure the pipeline is initialized before use
        if not initialized:
            print("⏳ Waiting for TTS pipeline initialization...")
            while not initialized:
                pass  # Wait for the pipeline to initialize

        # Fallback to TTS
        generator = pipeline(text, voice=voice)
        for _, _, audio in generator:
            sd.play(audio, samplerate=24000)
            sd.wait()

    except Exception as e:
        print(f"TTS error: {e}")
