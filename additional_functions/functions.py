import getpass
import os
import platform
import shutil
import distutils.dir_util
from VA_config import speak


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
    from_path = input("Path to your file:\n")
    if os.path.isfile(from_path):
        speak("I found it. Paste a path where you want to copy your file")
        to_path = input("Path to folder where file will be copied:\n")
        if os.path.isdir(to_path):
            return [from_path.replace('"', ""), to_path.replace('"', "")]
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
    from_path = input("Path to your folder:\n")
    if os.path.isdir(from_path):
        speak("I found it. Paste a path where you want to copy your folder")
        to_path = input("Path to folder where folder will be copied:\n")
        if os.path.isdir(to_path):
            return [from_path.replace('"', ""), to_path.replace('"', "")]
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
