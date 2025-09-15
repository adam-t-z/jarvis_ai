import requests
import simpleaudio as sa

API_URL = "https://coqui-xtts.hf.space/run/predict"
text_input = "Hello, this is Coqui XTTS speaking."
language = "en"

payload = {
    "data": [
        text_input,  # text
        None,        # optional speaker audio (set to None)
        language,    # language code
        0.75,        # temperature (defaults are fine)
        1.0,         # length scale
        1.0,         # stability
        1.0,         # similarity boost
    ]
}

print("Sending request to Coqui XTTS Space...")
response = requests.post(API_URL, json=payload)

if response.status_code == 200:
    output_url = response.json()["data"][0]  # URL to generated WAV
    print("Audio URL:", output_url)

    # Download and play the audio
    audio_response = requests.get(output_url)
    if audio_response.status_code == 200:
        print("Playing audio...")
        wave_obj = sa.WaveObject(audio_response.content, num_channels=1, bytes_per_sample=2, sample_rate=22050)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    else:
        print("Failed to download audio:", audio_response.status_code)
else:
    print("Request failed:", response.status_code)
    print(response.text)
