import pyttsx3
import logging
import platform
import speech_recognition as sr

logging.basicConfig(filename='logs/configuration.log', level=logging.INFO,
                    format='%(asctime)s-%(levelname)s:%(name)s:%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


def get_speak_engine():
    engine = None
    logging.info("Start configuring voice engine")
    try:
        if platform.system() == "Windows":  # Windows
            logging.info("Configuring voice engine on Windows OS")
            engine = pyttsx3.init()
            engine.setProperty("rate", 178)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
        elif platform.system() == "Linux":  # Linux
            logging.info("Configuring voice engine on Linux OS")
            engine = pyttsx3.init(driverName='espeak')
        elif platform.system() == "Darwin":  # Mac
            logging.info("Configuring voice engine on MacOS")
            engine = pyttsx3.init(driverName='nsss')
    except ImportError as iError:
        logging.error("The requested pyttsx3 driver is not found. Error: ", iError)
        print("The requested pyttsx3 driver is not found.")
    except RuntimeError as rError:
        logging.error("The pyttsx3 driver fails to initialize with error: ", rError)
        print("The pyttsx3 driver fails to initialize with error.")
    finally:
        logging.info("Configuring of voice engine was successfully")
        return engine


def speak(engine, text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    logging.info("Microphone configuring was started")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
            logging.info("Microphone configuring ended with success")
        except Exception as microphoneError:
            logging.error("Microphone configuring ended with error: ", microphoneError)
    return said.lower()
