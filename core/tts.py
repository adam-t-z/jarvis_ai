# core/tts.py

from kokoro import KPipeline
import sounddevice as sd
import soundfile as sf
import os
import time

# Initialize the TTS pipeline once
pipeline = KPipeline(lang_code='a')

# Optional: set an output directory for saved audio
OUTPUT_DIR = "tts_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def speak(text: str, voice: str = 'af_heart'):
    """
    Speaks the given text using Kokoro TTS and saves the audio to disk.
    
    Args:
        text (str): The text to be spoken.
        voice (str): Voice preset to use for synthesis (default: 'af_heart').
    """
    print(f"Assistant: {text}")
    try:
        generator = pipeline(text, voice=voice)
        for i, (_, _, audio) in enumerate(generator):
            # Play audio
            sd.play(audio, samplerate=24000)
            sd.wait()
            
            # Save audio
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{timestamp}_{i}.wav"
            filepath = os.path.join(OUTPUT_DIR, filename)
            sf.write(filepath, audio, 24000)
            print(f"Audio saved to {filepath}")

    except Exception as e:
        print(f"TTS error: {e}")
