import pyttsx3
import platform
import speech_recognition as sr


def get_speak_engine():
    engine = None
    try:
        if platform.system() == "Windows":  # Windows
            engine = pyttsx3.init(driverName='sapi5')
        elif platform.system() == "Linux":  # Linux
            engine = pyttsx3.init(driverName='espeak')
        elif platform.system() == "Darwin":  # Mac
            engine = pyttsx3.init(driverName='nsss')
    except ImportError as iError:
        print("The requested pyttsx3 driver is not found. Error: ", iError)
    except RuntimeError as rError:
        print("The pyttsx3 driver fails to initialize with error: ", rError)
    finally:
        return engine


def speak(engine, text):
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
