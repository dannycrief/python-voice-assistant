import os
import re
import time
import winreg
import shutil
import getpass
import platform
import distutils.dir_util
from threading import Timer

from VA_config import speak


def start_browser(browser_name):
    if browser_name.lower() in ["google chrome", "chrome", "google chrome browser"]:
        return 'start chrome'
    elif browser_name.lower() in ["edge", "microsoft browser", "microsoft edge browser"]:
        return 'start MicrosoftEdge'
    elif browser_name.lower() in ["opera", "opera browser"]:
        return 'start opera'
    else:
        return "Cannot find this browser"


def text2int(textnum, numwords={}):
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

    return result + current


def get_numbers_from_string(phrase, text):
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
    numbers = get_numbers_from_string(phrase, text)
    first_number = numbers[0]
    second_number = numbers[1]
    if phrase in ["add", "plus", "+"]:
        return first_number + second_number
    elif phrase in ["subtract", "minus", "-"]:
        return first_number - second_number
    elif phrase in ["divide", "divided by", "/"]:
        try:
            return first_number / second_number
        except ZeroDivisionError as e:
            return e
    elif phrase in ["multiply", "multiplied by", "times", "*"]:
        return first_number * second_number


def get_full_path(filename, search_folder, disk):
    disk = f"{disk}:/".upper()
    if platform.system() == "Windows":  # Windows
        for root, folders, _ in os.walk(os.path.join(disk, "Users", getpass.getuser())):
            folders[:] = [d for d in folders if not d[0] == '.']
            if search_folder in folders:
                for root_, _, files in os.walk(os.path.join(root, search_folder)):
                    files = [f for f in files if not f[0] == '.']
                    find_files = list(filter(lambda elem: filename in elem, files))
                    if len(find_files) > 0:
                        return [os.path.join(root_, elem) for elem in find_files]
    elif platform.system() == "Linux":  # Linux
        return
    elif platform.system() == "Darwin":  # Mac
        return


def get_file_path() -> list:
    speak("OK, all I need is you paste path to your file")
    from_path = input("Path to your file:\n").replace('"', "")
    if os.path.isfile(from_path):
        speak("I found it. Paste a path where you want to copy your file")
        to_path = input("Path to folder where file will be copied:\n").replace('"', "")
        if os.path.isdir(to_path):
            return [from_path, to_path]
        else:
            return ["File into file"]
    else:
        return ["Not a file"]


def copy_file(source, destination) -> str:
    try:
        shutil.copy(source, destination)
        return "OK"
    except OSError as exc:
        return f"Error: {exc}"


def get_directory_path() -> list:
    speak("OK, all I need is you paste path to your folder")
    from_path = input("Path to your folder:\n").replace('"', "")
    if os.path.isdir(from_path):
        speak("I found it. Paste a path where you want to copy your folder")
        to_path = input("Path to folder where folder will be copied:\n").replace('"', "")
        if os.path.isdir(to_path):
            return [from_path, to_path]
        else:
            return ["Folder into file"]
    else:
        return ["Not a folder"]


def copy_directory(source, destination) -> str:
    folder_name = source.split('\\')[-1]
    destination = os.path.join(destination, folder_name)
    try:
        os.mkdir(destination)
        distutils.dir_util.copy_tree(source, destination)
    except OSError as exc:
        return f"Cannot copy directory. Error occurred: {exc}"
    else:
        return f"Directory successfully copied to {destination.removesuffix(folder_name)}"


def get_timer(text: str) -> tuple[int, int]:
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

    return first_number, second_number


def set_timer(text):
    speak("Setting a timer")
    timer = get_timer(text)
    seconds = timer[1] + timer[0] * 60
    t = Timer(float(seconds), say_timer_over)
    t.start()


def say_timer_over():
    speak("Timer is done!")


def start_timer(seconds):
    for second in range(seconds, 0, -1):
        time.sleep(1)


def get_installed_programs(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)
    count_subkey = winreg.QueryInfoKey(aKey)[0]
    software_list = []

    for i in range(count_subkey):
        try:
            software = {}
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue
    return software_list
