from __future__ import print_function

import pytz
import datetime

from VA_date import get_date
from VA_config import speak, get_audio
from VA_note import note
from google_auth import authenticate_google

WAKE = "hello mark"
STOP = ["bye", "see you", "goodbye"]
CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
NOTE_STRS = ["make a note", "write this down", "remember this"]

SERVICE = authenticate_google()


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
        print('No upcoming events found.')
        speak('No upcoming events found.')
    else:
        print(f'You have {len(events)} events on this day')
        speak(f'You have {len(events)} events on this day')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "AM"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "PM"
            print(event["summary"] + " at " + start_time)
            speak(event["summary"] + " at " + start_time)


to_stop = []

if __name__ == '__main__':
    print("Listening")
    text = get_audio()
    if text.count(WAKE) > 0:
        speak("Hello, what do you want me to do?")
        while True:
            print("Listening")
            text = get_audio()

            for phrase in CALENDAR_STRS:
                if phrase in text:
                    date = get_date(text)
                    if date:
                        get_events(date, SERVICE)
                    else:
                        speak("I don't understand")

            for phrase in NOTE_STRS:
                if phrase in text:
                    speak("What would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I've made a note of that.")

            for phrase in STOP:
                if phrase in text:
                    to_stop.append(phrase)

            if len(to_stop) > 0:
                speak("See you soon!")
                break
