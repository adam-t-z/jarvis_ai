from core.voice_input import listen

if __name__ == "__main__":
    print("Say something!")
    text = listen()
    print(f"Recognized: {text}")
