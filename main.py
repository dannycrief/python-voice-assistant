import os
import pytz
import random
import datetime
import threading

from additional_functions.VA_note import note
from additional_functions.VA_date import get_date
from additional_functions.before_start import get_info_before_begin
from googleAPI.googleMaps.google_maps_API import get_google_map_travel
from googleAPI.googleGmail.google_gmail_API import authenticate_google_gmail
from additional_functions.VA_config import speak, get_audio, get_speak_engine
from googleAPI.googleCalendar.google_calendarAPI import authenticate_google_calendar
from additional_functions.functions import copy_file, start_browser, execute_math, copy_directory, get_file_path, \
    get_directory_path, set_timer, open_program

ENGINE = get_speak_engine()
CALENDAR_SERVICE = authenticate_google_calendar()
GMAIL_SERVICE = authenticate_google_gmail()

WAKE = "hello mark"
STOP = ["bye", "see you", "goodbye"]
CALENDAR_STRS = ["what do i have", "do i have plans", "do i have any plans", "am i busy"]
GMAIL_STRS = ["do i have new messages", "do i have messages"]
NOTE_STRS = ["make a note", "write this down", "remember this"]
GMAPS_STRS = ["how can i get", "create a road", "create road", "how long do i need to ride"]
BROWSER_STRS = ["open browser"]
OPEN_PROGRAM_STRS = ['run', 'run program', 'open', 'open program', 'start', 'start program', 'launch',
                     'launch program']
MATH_STRS = ["add", "plus", "+", "subtract", "minus", "-", "divide", "divided by",
             "/", "multiply", "multiplied by", "times", "*"]
COPY_STRS = ["copy file", "copy folder", "move file", "move folder"]
TIME_NOW_STRS = ["current time", "time now", "what time is it"]
TIMER_STRS = ["set timer"]
END_STR = ["See you soon!", "Till next time", "Goodbye", "Bye", "See you"]


def get_events(date, service):
    # Call the Calendar API
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(date, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(), singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak(ENGINE, 'No upcoming events found.')
    else:
        speak(ENGINE, f'You have {len(events)} events on this day')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "AM"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "PM"
            speak(ENGINE, event["summary"] + " at " + start_time)


def get_messages_from_gmail(service):
    results = service.users().messages().list(userId='me',
                                              labelIds=['INBOX'],
                                              q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        speak(ENGINE, 'No messages found.')
    else:
        gmails = []
        messages_count = 0
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            messages_count += 1
            gmails.append(msg)

        speak(ENGINE, f"You have {str(messages_count)} unread messages.")
        speak(ENGINE, "Would you like to see your messages: ")
        message_choice = get_audio().lower()

        if "yes" in message_choice:
            speak(ENGINE, "How many messages you want to display:")
            number_of_emails = int(get_audio())
            if number_of_emails == number_of_emails:
                for gmail in gmails[:number_of_emails]:
                    email_data = gmail["payload"]["headers"]
                    for values in email_data:
                        name = values["name"]
                        if name == "From":
                            from_name = values["value"]
                            speak(ENGINE, f"You have a new message from: {from_name}")
                            speak(ENGINE, f"{gmail['snippet'][:50]} etc.")
            else:
                speak(ENGINE, "I didn't understand")


to_stop = []


def main():
    while True:
        text = get_audio()
        if text.count(WAKE) > 0:
            speak(ENGINE, "Hello, what do you want me to do?")
            text = get_audio()
            for phrase in CALENDAR_STRS:
                if phrase in text:
                    date = get_date(text)
                    if date:
                        get_events(date, CALENDAR_SERVICE)
                        pass
                    else:
                        speak(ENGINE, "I don't understand")

            for phrase in NOTE_STRS:
                if phrase in text:
                    speak(ENGINE, "What would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak(ENGINE, "I've made a note of that.")

            for phrase in GMAIL_STRS:
                if phrase in text:
                    get_messages_from_gmail(GMAIL_SERVICE)

            for phrase in GMAPS_STRS:
                if phrase in text:
                    speak(ENGINE,
                          "Type your current address. Address first, city (optional) and postal code (optional)")
                    user_address_from = input("Type your current address (address, <city>, <postal code>): ")
                    speak(ENGINE, "Where you want to go (address, city)")
                    user_address_to = input("Where you want to go (address, city): ")
                    road_data = get_google_map_travel(user_address_from, user_address_to)
                    if road_data:
                        travel_duration = road_data[0]
                        travel_options = road_data[1]
                        speak(ENGINE,
                              f"Your travel will take a {travel_duration}. Do you want me to tell you travel options?")
                        if get_audio() == "yes" or input("Do you want me to tell you travel options? "):
                            for option in travel_options:
                                speak(ENGINE, option)
                        else:
                            speak(ENGINE, "Ok")

            for phrase in BROWSER_STRS:
                if phrase in text:
                    speak(ENGINE, "Which browser?")
                    browser_name = get_audio()
                    open_browser = start_browser(browser_name)
                    if open_browser == "Cannot find this browser":
                        speak(ENGINE, open_browser)
                    else:
                        speak(ENGINE, "I've got it. Just a second")
                        os.system(open_browser)

            for phrase in MATH_STRS:
                if phrase in text:
                    result = execute_math(phrase, text)
                    if result == "division by zero":
                        speak(ENGINE, "Hmm, division by zero is impossible")
                    else:
                        speak(ENGINE, f"it is: {result}")

            for phrase in COPY_STRS:
                if phrase in text:
                    if "copy file" in phrase:
                        path = get_file_path()
                        if len(path) > 1:
                            speak(ENGINE, "On its way...")
                            speak(ENGINE, "Successfully copied") if copy_file(path[0], path[1]) == "OK" else speak(
                                ENGINE,
                                "Cannot copy file because of error")
                        elif path[0] == "File into file":
                            speak(ENGINE, "Seriously? Do you want to copy file to file? Think about it")
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
                    speak(ENGINE, f"Current time is {datetime.datetime.now().strftime('%H:%M')}")

            for phrase in TIMER_STRS:
                if phrase in text:
                    timer_thread = threading.Thread(target=set_timer, args=(text,))
                    timer_thread.start()
            for phrase in OPEN_PROGRAM_STRS:
                if phrase in text:
                    print(phrase, text)
                    program_name = text.replace(phrase, '')
                    open_program(program_name)

        for phrase in STOP:
            if phrase in text:
                to_stop.append(phrase)
        if len(to_stop) > 0:
            speak(ENGINE, random.choice(END_STR))
            break


if __name__ == '__main__':
    get_info_before_begin()
    print("Mark's listening...")
    main()
