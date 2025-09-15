from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='a')

# text = '''
# [Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
# '''

text = "Goodbye, Sir."

generator = pipeline(text, voice='af_heart')

for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    # Save output WAV files
    sf.write(f'{i}.wav', audio, 24000)

print("Done! Audio files saved as 0.wav, 1.wav, ...")
