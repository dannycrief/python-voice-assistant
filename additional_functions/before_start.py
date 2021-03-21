import re
import pickle
import getpass
import os.path
from random import choices

from additional_functions.logger import get_logger
from additional_functions.VA_config import speak, get_speak_engine

logger = get_logger("before_start")
ENGINE = get_speak_engine()


def get_info_before_begin():
    logger.info('Getting user information before begin')
    installed_apps = get_installed_apps_before_begin()
    user_info = get_user_info_before_begin()
    return installed_apps, user_info


def get_installed_programs():
    logger.info('Getting folders where installed programs are')
    apps = []
    path = os.path.join("C:/Users", getpass.getuser(), "AppData/Roaming/Microsoft/Windows/Start Menu/Programs")
    for root, folders, files in os.walk(path):
        apps.append({
            "root": root,
            "folders": folders,
            "files": files
        })
    path = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs"
    for root, folders, files in os.walk(path):
        apps.append({
            "root": root,
            "folders": folders,
            "files": files
        })
    for i in apps:
        for file in i['files']:
            if file.lower().__contains__('uninstall'):
                i['files'].remove(file)
    logger.info('Folders were successfully found')
    return apps


def get_installed_apps_before_begin():
    logger.info('Getting installed apps')
    installed_apps = None
    if os.path.exists('installed_programs.pickle'):
        logger.info('File with installed programs was found')
        with open('installed_programs.pickle', 'rb') as token:
            installed_apps = pickle.load(token)
    if not installed_apps:
        logger.info('File with installed programs was not found. Getting installed programs')
        speak(ENGINE,
              "Hello, my name is Sarah. I am your virtual voice assistant. Give me few seconds to configure settings")
        logger.info("Sarah starts configuration.")
        installed_apps = get_installed_programs()
        with open("installed_programs.pickle", "wb") as pickle_file:
            pickle.dump(installed_apps, pickle_file)
    logger.info('Installed applications was added to pickle file.')
    return installed_apps


def get_user_info_before_begin():
    user_info = None
    if os.path.exists('user_info.pickle'):
        logger.info("File with user information was found")
        with open('user_info.pickle', 'rb') as token:
            user_info = pickle.load(token)
            speak(ENGINE, "Hello {}!".format(user_info['first_name']))
    if not user_info:
        logger.info("File with user information was not found")
        logger.info("Getting some information about user for better work")
        speak(ENGINE, "What is your name?")
        first_name = input().capitalize()
        speak(ENGINE, "What is your surname?")
        last_name = input().capitalize()
        speak(ENGINE, "Nice to meet you %s! I will also need your email for sending your messages" % first_name)
        email = input()
        while not is_valid_email(email):
            answers = ["Please give me correct email", "This email is not correct"]
            speak(ENGINE, choices(answers)[0])
            email = input()
        user_info = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
        with open("user_info.pickle", "wb") as pickle_file:
            pickle.dump(user_info, pickle_file)
    logger.info("Got user information. File with user information was successfully created")
    logger.info("Collected data about user")
    logger.info("Sarah successfully ended configuration...")
    return user_info


def is_valid_email(email_address):
    logger.info("Validation of user email")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email_address):
        logger.info("Email is valid")
        return True
    logger.warning("Email is invalid")
    return False
