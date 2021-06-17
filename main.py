import os
import random
import logging
import datetime
import threading

from pathlib import Path
from additional_functions.logger import get_logger
from additional_functions.functions import note, get_date
from additional_functions.before_start import get_info_before_begin
from additional_functions.VA_config import speak, get_audio, get_speak_engine
from googleAPI.googleCalendar.google_calendarAPI import authenticate_google_calendar, get_google_calendar_events, \
    create_google_calendar_event
from googleAPI.googleGmail.google_gmail_API import authenticate_google_gmail, get_unread_gmail_messages, \
    send_email_message
from additional_functions.functions import copy_file, start_browser, execute_math, copy_directory, get_file_path, \
    get_directory_path, set_timer, open_program

Path("logs/").mkdir(parents=True, exist_ok=True)

logger = get_logger("main")

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)

logger.info("Authenticating google calendar")
CALENDAR_SERVICE = authenticate_google_calendar()
logger.info("Authenticating google gmail")
GMAIL_SERVICE = authenticate_google_gmail()
logger.info("Getting speak engine")
ENGINE = get_speak_engine()

WAKE = ["hi sarah", "hello sarah"]
STOP = ["bye", "see you", "goodbye"]
CALENDAR_STRS = ["what do i have", "do i have plans", "do i have any plans", "am i busy"]
EVENT_CALENDAR_STRS = ["create event", "create new event", "add event", "add new event"]
GMAIL_STRS = ["do I have new messages", "do I have messages", "do I have any messages",
              "do I have any new messages", "do i have new messages", "do i have messages",
              "do i have any messages"]
SEND_GMAIL_STRS = ["send message", "send email"]
NOTE_STRS = ["make a note", "write this down", "remember this"]
BROWSER_STRS = ["open browser"]
OPEN_PROGRAM_STRS = ['run', 'run program', 'open', 'open program', 'start', 'start program', 'launch',
                     'launch program']
MATH_STRS = ["add", "plus", "+", "subtract", "minus", "-", "divide", "divided by",
             "/", "multiply", "multiplied by", "times", "*"]
COPY_STRS = ["copy file", "copy folder", "move file", "move folder"]
TIME_NOW_STRS = ["current time", "time now", "what time is it"]
TIMER_STRS = ["set timer"]
END_STR = ["See you soon!", "Till next time", "Goodbye", "Bye", "See you"]

to_stop = []


def main():
    while True:
        logger.info("Sarah is running.")
        text = get_audio().lower()
        if text in WAKE:
            speak(ENGINE, "Hello, what do you want me to do?")
            text = get_audio().lower()

            for phrase in EVENT_CALENDAR_STRS:
                if phrase in text:
                    create_google_calendar_event(CALENDAR_SERVICE)

            for phrase in CALENDAR_STRS:
                if phrase in text:
                    logger.info("Found %s in CALENDAR_STRS" % phrase)
                    date = get_date(text)
                    if date:
                        events = get_google_calendar_events(date, CALENDAR_SERVICE)
                        if not events:
                            logger.info("Sarah notice that there are no events found.")
                            speak(ENGINE, 'No upcoming events found.')
                        else:
                            logger.info("Sarah found %s events." % len(events))
                            speak(ENGINE, 'You have %s events on this day' % len(events))

                            for event in events:
                                start = event['start'].get('dateTime', event['start'].get('date'))
                                start_time = str(start.split("T")[1].split("+")[0])
                                if int(start_time.split(":")[0]) < 12:
                                    start_time = start_time + "AM"
                                else:
                                    start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                                    start_time = start_time + "PM"
                                speak(ENGINE, event["summary"] + " at " + start_time)
                    else:
                        speak(ENGINE, "I don't understand")

            for phrase in NOTE_STRS:
                if phrase in text:
                    logger.info("Found %s. in NOTE_STRS" % phrase)
                    speak(ENGINE, "What would you like me to write down?")
                    note_text = get_audio().lower()
                    note(note_text)
                    speak(ENGINE, "I've made a note of that.")

            for phrase in GMAIL_STRS:
                if phrase in text:
                    logger.info("Found %s in GMAIL_STRS" % phrase)
                    get_unread_gmail_messages(GMAIL_SERVICE)

            for phrase in SEND_GMAIL_STRS:
                if phrase in text:
                    logger.info("Found %s in SEND_GMAIL_STRS" % phrase)
                    send_email_message(GMAIL_SERVICE)

            for phrase in BROWSER_STRS:
                if phrase in text:
                    logger.info("Found %s in BROWSER_STRS" % phrase)
                    speak(ENGINE, "Which browser?")
                    browser_name = get_audio().lower()
                    open_browser = start_browser(browser_name)
                    if open_browser == "Cannot find this browser":
                        speak(ENGINE, open_browser)
                    else:
                        speak(ENGINE, "I've got it. Just a second")
                        os.system(open_browser)

            for phrase in MATH_STRS:
                if phrase in text:
                    logger.info("Found %s in MATH_STRS" % phrase)
                    result = execute_math(phrase, text)
                    if result == "division by zero":
                        speak(ENGINE, "Hmm, division by zero is impossible")
                    else:
                        speak(ENGINE, "it is: %s" % result)

            for phrase in COPY_STRS:
                if phrase in text:
                    logger.info("Found %s in COPY_STRS" % phrase)
                    if "copy file" in phrase:
                        path = get_file_path()
                        if len(path) > 1:
                            speak(ENGINE, "On its way...")
                            speak(ENGINE, "Successfully copied") if copy_file(path[0], path[1]) == "OK" else speak(
                                ENGINE,
                                "Cannot copy file because of error")
                        elif path[0] == "Not a file":
                            speak(ENGINE, "Selected item must be a file, but not folder")
                    elif "copy folder" in phrase:
                        path = get_directory_path()
                        if len(path) > 1:
                            speak(ENGINE, "On it way...")
                            speak(ENGINE, "Successfully copied") if copy_directory(path[0], path[1]) == "OK" else speak(
                                ENGINE, "Cannot copy file because of error")
                        elif path[0] == "Folder into file":
                            speak(ENGINE, "Seriously? Do you want to copy folder to file? Think about it")
                        elif path[0] == "Not a folder":
                            speak(ENGINE, "Selected item must be a folder, but not file")

            for phrase in TIME_NOW_STRS:
                if phrase in text:
                    logger.info("Found %s in TIME_NOW_STRS" % phrase)
                    speak(ENGINE, "Current time is %s" % datetime.datetime.now().strftime('%H:%M'))

            for phrase in TIMER_STRS:
                if phrase in text:
                    logger.info("Found %s in TIMER_STRS" % phrase)
                    timer_thread = threading.Thread(target=set_timer, args=(text,))
                    timer_thread.start()

            for phrase in OPEN_PROGRAM_STRS:
                if phrase in text:
                    logger.info("Found %s in OPEN_PROGRAM_STRS" % phrase)
                    print(phrase, text)
                    program_name = text.replace(phrase, '')
                    open_program(program_name)

        for phrase in STOP:
            if phrase in text:
                logger.info("Found %s in STOP" % phrase)
                to_stop.append(phrase)
        if len(to_stop) > 0:
            logger.info("Sarah stops working")
            speak(ENGINE, random.choice(END_STR))
            break


if __name__ == '__main__':
    get_info_before_begin()
    logger.info("Collected user data. Sarah is listening..")
    print("Sarah's listening...")
    main()
