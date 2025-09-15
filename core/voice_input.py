import speech_recognition as sr

def listen(timeout=5, phrase_time_limit=7):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Please speak clearly.")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return None

    try:
        text = recognizer.recognize_google(audio)
        text = text.strip().lower()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def listen_with_timeout(user_timeout=15):
    """Listen for user input with a specified timeout. Returns None if timeout occurs."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Please speak clearly.")
        try:
            # Use the user-specified timeout
            audio = recognizer.listen(source, timeout=user_timeout, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            print(f"Listening timed out after {user_timeout} seconds.")
            return "TIMEOUT"

    try:
        text = recognizer.recognize_google(audio)
        text = text.strip().lower()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
