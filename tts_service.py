# app/tts_service.py

import pyttsx3

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 170)   # speed
        _engine.setProperty('volume', 1)   # max volume
    return _engine


def speak(text: str):
    engine = get_engine()
    engine.say(text)
    engine.runAndWait()