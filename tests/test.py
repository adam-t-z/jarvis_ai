import speech_recognition as sr
import pyttsx3
import time

"""
There was a problem with the TTS engine.
Solution: init the model every time you use it.
"""
def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS error: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            speak("Speech recognition service error.")
            print(f"Request error: {e}")
        except Exception as e:
            speak("Something went wrong while listening.")
            print(f"Listen error: {e}")
    return None

def handle_command(command):
    if not command:
        return True  # Keep going

    if "hello" in command or "hi" in command:
        speak("Hello there! How can I help?")
    elif "how are you" in command:
        speak("I'm doing great! Thanks for asking.")
    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "exit" in command or "quit" in command or "bye" in command:
        speak("Goodbye! Have a great day.")
        return False  # Stop the loop
    else:
        speak("I didn’t understand that. Can you repeat?")
    
    return True

# Main loop
if __name__ == "__main__":
    speak("Hi there. What do you want?")
    while True:
        command = listen()
        if not handle_command(command):
            break


