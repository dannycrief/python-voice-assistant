import re
import pickle
import getpass
import os.path
from random import choices

from additional_functions.VA_config import speak, get_speak_engine

ENGINE = get_speak_engine()


def get_info_before_begin():
    installed_apps = get_installed_apps_before_begin()
    user_info = get_user_info_before_begin()
    return installed_apps, user_info


def get_installed_programs():
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
    return apps


def get_installed_apps_before_begin():
    installed_apps = None
    if os.path.exists('installed_programs.pickle'):
        with open('installed_programs.pickle', 'rb') as token:
            installed_apps = pickle.load(token)
    if not installed_apps:
        speak(ENGINE,
              "Hello, my name is Mark. I am your virtual voice assistant. Give me few minutes to configure settings")
        print("Mark starts configuration...")
        installed_apps = get_installed_programs()
        with open("installed_programs.pickle", "wb") as pickle_file:
            pickle.dump(installed_apps, pickle_file)
    print("Collected data about programs")
    return installed_apps


def get_user_info_before_begin():
    user_info = None
    if os.path.exists('user_info.pickle'):
        with open('user_info.pickle', 'rb') as token:
            user_info = pickle.load(token)
            speak(ENGINE, "Hello {}!".format(user_info['first_name']))
    if not user_info:
        print("Getting some information about user for better work")
        speak(ENGINE, "What is your name?")
        first_name = input().capitalize()
        speak(ENGINE, "What is your surname?")
        last_name = input().capitalize()
        speak(ENGINE, f"Nice to meet you {first_name}! I will also need your email for sending your messages")
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
    print("Collected data about user")
    print("Mark successfully ended configuration...")
    return user_info


def is_valid_email(email_address):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email_address):
        return True
    return False
