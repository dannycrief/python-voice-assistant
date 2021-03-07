import pyttsx3
import platform
import speech_recognition as sr

from additional_functions.logger import get_logger

logger = get_logger("configuration")


def get_speak_engine():
    engine = None
    logger.info("Start configuring voice engine")
    try:
        if platform.system() == "Windows":  # Windows
            logger.info("Configuring voice engine on Windows OS")
            engine = pyttsx3.init()
            engine.setProperty("rate", 178)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
        elif platform.system() == "Linux":  # Linux
            logger.info("Configuring voice engine on Linux OS")
            engine = pyttsx3.init(driverName='espeak')
        elif platform.system() == "Darwin":  # Mac
            logger.info("Configuring voice engine on MacOS")
            engine = pyttsx3.init(driverName='nsss')
    except ImportError as iError:
        logger.error("The requested pyttsx3 driver is not found. Error: ", iError)
        print("The requested pyttsx3 driver is not found.")
    except RuntimeError as rError:
        logger.error("The pyttsx3 driver fails to initialize with error: ", rError)
        print("The pyttsx3 driver fails to initialize with error.")
    finally:
        logger.info("Configuring of voice engine was successfully")
        return engine


def speak(engine, text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    logger.info("Microphone configuring was started")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            logger.info("Recognizing audio with google recognizer")
            said = r.recognize_google(audio)
            print(said)
        except Exception:
            logger.warning("Recognizing audio failed")
    return said.lower()
