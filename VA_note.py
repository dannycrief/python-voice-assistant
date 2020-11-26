import subprocess
import os
import datetime


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(os.path.join("notes", file_name), "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", os.path.join("notes", file_name)])
