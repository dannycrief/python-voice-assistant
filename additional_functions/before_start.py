import re
import winreg
import pickle
import os.path
import json
from random import choices

from VA_config import speak
from additional_functions.functions import get_installed_programs


def get_info_before_begin():
    speak("Hello, my name is Mark. I am your virtual voice assistant. Give me few minutes to configure settings")
    print("Mark starts configuration...")
    installed_apps = get_installed_apps_before_begin()
    print("Collected data about programs")
    print("Getting some information about user for better work")
    user_info = get_user_info_before_begin()
    print("Collected data about user")
    print("Mark ended configuration...")
    speak("Thank you for choosing me as your own assistant. Let's get started")
    return installed_apps, user_info


def get_installed_apps_before_begin():
    installed_apps = None
    if os.path.exists('installed_programs.pickle'):
        with open('installed_programs.pickle', 'rb') as token:
            installed_apps = json.dumps(pickle.load(token), indent=4, sort_keys=True)
    if not installed_apps:
        installed_apps = get_installed_programs(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + \
                         get_installed_programs(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + \
                         get_installed_programs(winreg.HKEY_CURRENT_USER, 0)
        with open("installed_programs.pickle", "wb") as pickle_file:
            pickle.dump(installed_apps, pickle_file)
    return installed_apps


def get_user_info_before_begin():
    user_info = None
    if os.path.exists('user_info.pickle'):
        with open('user_info.pickle', 'rb') as token:
            user_info = json.dumps(pickle.load(token), indent=4, sort_keys=True)
    if not user_info:
        speak("What is your name?")
        first_name = input().capitalize()
        speak("What is your surname?")
        last_name = input().capitalize()
        speak(f"Nice to meet you {first_name}! I will also need your email for sending your messages")
        email = input()
        while not is_valid_email(email):
            answers = ["Please give me correct email", "This email is not correct"]
            speak(choices(answers)[0])
            email = input()
        user_info = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
        with open("user_info.pickle", "wb") as pickle_file:
            pickle.dump(user_info, pickle_file)
    return user_info


def is_valid_email(email_address):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email_address):
        return True
    return False
