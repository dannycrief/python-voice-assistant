import pyttsx3
import speech_recognition as sr


def speak(text):
    engine = pyttsx3.init()
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception:
            pass
    return said.lower()
