# core/wake_word_listener.py

import speech_recognition as sr

# All acceptable transcriptions of the name "Sami"
SAMI_WAKE_WORDS = {
    "sami", "sammy", "samy", "samee", "saami", "sahmi", "sammi", "sam"
}

def listen_for_wake_word(callback_func=None):
    """
    Listen for wake word using speech recognition.
    
    Args:
        callback_func: Function to call when wake word is detected
    
    Returns:
        str: Detected wake word or None if error
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
        
        while True:
            try:
                with mic as source:
                    # Listen with timeout
                    audio = recognizer.listen(
                        source, 
                        timeout=None, 
                        phrase_time_limit=3
                    )
                
                # Use Google Speech Recognition
                transcript = recognizer.recognize_google(audio).lower().strip()
                
                # Match whole words only
                words = transcript.split()
                detected_word = None
                
                # Check for any wake word in the transcript
                for word in words:
                    if word in SAMI_WAKE_WORDS:
                        detected_word = "sami"
                        break
                
                if detected_word:
                    if callback_func:
                        callback_func(detected_word)
                    
                    return detected_word
                
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                return None
                
    except KeyboardInterrupt:
        return None
    except Exception as e:
        return None
def listen_continuously(wake_word_callback):
    """
    Continuously listen for wake word using speech recognition.
    
    Args:
        wake_word_callback: Function to call when wake word is detected
    """
    try:
        while True:
            detected = listen_for_wake_word(callback_func=wake_word_callback)
            if detected:
                # Continue listening for next wake word
                pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        pass

# Remove the unnecessary CustomWakeWordDetector class since we only use speech recognition