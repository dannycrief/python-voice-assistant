import os
import pickle
import re

import pytz
import time
import ntpath
import shutil
import datetime
import subprocess
from pathlib import Path
import distutils.dir_util
from threading import Timer

from additional_functions.logger import get_logger
from additional_functions.VA_config import speak, get_speak_engine
from additional_functions.before_start import get_installed_apps_before_begin

logger = get_logger("functions")

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]

ENGINE = get_speak_engine()


def note(text):
    Path("notes/").mkdir(parents=True, exist_ok=True)
    logger.info("Making note")
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    try:
        with open(os.path.join("notes/", file_name), "a") as f:
            f.write(text)
        subprocess.Popen(["notepad.exe", os.path.join("notes/", file_name)])
    except FileNotFoundError as error:
        logger.error("Error with making a note. See error:", error)


def get_date(text):
    logger.info("Getting date")
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if text.count("tomorrow") > 0:
        return tomorrow

    if text.count("yesterday") > 0:
        return yesterday

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)


def start_browser(browser_name):
    if browser_name.lower() in ["google chrome", "chrome", "google chrome browser"]:
        logger.info("Starting {}".format(browser_name))
        return 'start chrome'
    elif browser_name.lower() in ["edge", "microsoft browser", "microsoft edge browser"]:
        logger.info("Starting {}".format(browser_name))
        return 'start MicrosoftEdge'
    elif browser_name.lower() in ["opera", "opera browser"]:
        logger.info("Starting {}".format(browser_name))
        return 'start opera'
    else:
        logger.warning("Cannot find this browser")
        return "Cannot find this browser"


def text2int(textnum, numwords=None):
    if numwords is None:
        numwords = {}
    logger.info("Converting text to integer")
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    logger.info("Text to integer. Input {}; Output {}".format(textnum, result + current))
    return result + current


def get_numbers_from_string(phrase, text):
    logger.info("Getting numbers from string.")
    first_number = None
    second_number = None
    while len(text) != 0:
        try:
            text2int(text)
        except Exception as e:
            e = e.__str__().replace("Illegal word: ", "")
            if e in phrase:
                first_number = text2int(text.split(phrase)[0])
                second_number = text2int(text.split(phrase)[1])
                text = ""
            else:
                text = text.replace(e, "")
    return first_number, second_number


def execute_math(phrase, text):
    logger.info("Executing math function {}".format(phrase))
    numbers = get_numbers_from_string(phrase, text)
    if phrase in ["add", "plus", "+"]:
        return numbers[0] + numbers[1]
    elif phrase in ["subtract", "minus", "-"]:
        return numbers[0] - numbers[1]
    elif phrase in ["divide", "divided by", "/"]:
        try:
            return numbers[0] / numbers[1]
        except ZeroDivisionError as e:
            logger.warning("Zero Division Error")
            return e
    elif phrase in ["multiply", "multiplied by", "times", "*"]:
        return numbers[0] * numbers[1]


def get_file_path() -> list:
    speak(ENGINE, "OK, all I need is you paste path to your file")
    from_path = input("Path to your file:\n").replace('"', "")
    if os.path.isfile(from_path):
        speak(ENGINE, "I found it. Paste a path where you want to copy your file")
        to_path = input("Path to folder where file will be copied:\n").replace('"', "")
        if os.path.isdir(to_path):
            return [from_path, to_path]
        else:
            logger.warning("Copy function cannot copy file to directory %s "
                           "because it doesn't exist. Creating folder" % to_path)
            speak(ENGINE, "Folder does not exist. I'll create this folder")
            os.mkdir(to_path)
            return [from_path, to_path]
    else:
        return ["Not a file"]


def copy_file(source, destination) -> str:
    logger.info("Coping file function started.")
    try:
        shutil.copy(source, destination)
        logger.info("Coping file function ended successfully")
        return "OK"
    except OSError as exc:
        logger.error("Coping file function with error", exc)
        return "Error: %s" % exc


def get_directory_path() -> list:
    logger.info("Getting directory path.")
    speak(ENGINE, "OK, all I need is you paste path to your folder")
    from_path = input("Path to your folder:\n").replace('"', "")
    if os.path.isdir(from_path):
        speak(ENGINE, "I found it. Paste a path where you want to copy your folder")
        to_path = input("Path to folder where folder will be copied:\n").replace('"', "")
        if os.path.isdir(to_path):
            return [from_path, to_path]
        else:
            logger.warning("Getting directory path function ended with warning. User tried to copy folder into file.")
            return ["Folder into file"]
    else:
        logger.warning("Getting directory path function ended with warning: Not a folder.")
        return ["Not a folder"]


def copy_directory(source, destination) -> str:
    logger.info("Copy directory function started.")
    folder_name = source.split('\\')[-1]
    destination = os.path.join(destination, folder_name)
    try:
        os.mkdir(destination)
        distutils.dir_util.copy_tree(source, destination)
    except OSError as exc:
        logger.warning("Cannot copy directory. Error occurred: %s" % exc)
        return "Cannot copy directory. Error occurred: %s" % exc
    else:
        logger.info("Directory successfully copied to %s" % destination.removesuffix(folder_name))
        return "Directory successfully copied to %s" % destination.removesuffix(folder_name)


def get_timer(text: str) -> tuple[int, int]:
    logger.info("Getting time for setting timer.")
    first_number = 0
    second_number = 0
    text = text.lower()
    for word in ["minutes", "minute"]:
        if word in text:
            text = text.split(word)
            first_text = text[0]
            while len(first_text) != 1:
                try:
                    try:
                        first_number = int(re.search(r'\d+', first_text).group())
                    except:
                        first_number = text2int(first_text)
                    text.pop(0)
                    break
                except Exception as e:
                    e = e.__str__().replace("Illegal word: ", "")
                    first_text = first_text.replace(e, "", 1)
    if not isinstance(text, list):
        text = [text]
    if "second" in text[0] or "seconds" in text[0]:
        text = text[0].split("second") if "second" in text[0] else text[0].split("seconds")
        second_text = text[0]
        while len(second_text) != 1:
            try:
                try:
                    second_number = int(re.search(r'\d+', second_text).group())
                except:
                    second_number = text2int(second_text)
                break
            except Exception as e:
                e = e.__str__().replace("Illegal word: ", "")
                second_text = second_text.replace(e, "", 1)
    logger.info("Timer found: %s:%s." % (first_number, second_number))
    return first_number, second_number


def set_timer(text):
    logger.info("Setting timer.")
    print("Setting a timer")
    timer = get_timer(text)
    seconds = float(timer[1] + timer[0] * 60)
    t = Timer(seconds, stop_timer)
    t.start()


def stop_timer():
    speak(ENGINE, "Timer is done!")


def open_program(program_name: str):
    logger.info("Opening program function started")
    programs = []
    installed_apps = get_installed_apps_before_begin()
    for app in installed_apps:
        for file in app['files']:
            if file.lower().__contains__(program_name):
                programs.append(os.path.join(app['root'], file))
    if len(programs) > 1:
        program_number = None
        speak(ENGINE,
              "These are the programs I found. Please enter a number of program.")
        for program in programs:
            print(ntpath.basename(program))
        try:
            program_number = int(input("")) - 1
        except ValueError:
            logger.error("Number of founded programs was expected. But user provides something else.")
            speak(ENGINE, "It is not a number.")
        try:
            os.startfile(programs[program_number])
        except IndexError:
            logger.error("Sarah found %s programs, but user tried to open %s" % (len(programs), program_number))
            speak(ENGINE, "I think I found fewer programs.")
        except TypeError as terror:
            logger.error("Cannot open program. Error is: %s" % terror)
            pass

    elif len(programs) == 0:
        logger.warning("Sarah cannot find any program")
        speak(ENGINE, "Sorry, I can't find this program.")
    else:
        logger.info("Opening %s" % ntpath.basename(programs[0]))
        speak(ENGINE, "Opening %s" % ntpath.basename(programs[0]))
        os.startfile(programs[0])
