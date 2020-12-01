import pytz
import datetime

from VA_date import get_date
from VA_config import speak, get_audio
from VA_note import note
from googleAPI.googleCalendar.google_calendarAPI import authenticate_google_calendar
from googleAPI.googleGmail.google_gmail_API import authenticate_google_gmail


WAKE = "hello mark"
STOP = ["bye", "see you", "goodbye"]
CALENDAR_STRS = ["what do i have", "do i have plans", "do i have any plans", "am i busy"]
GMAIL_STRS = ["do i have new messages", "do i have messages"]
NOTE_STRS = ["make a note", "write this down", "remember this"]

CALENDAR_SERVICE = authenticate_google_calendar()
GMAIL_SERVICE = authenticate_google_gmail()


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


def get_messages_from_gmail(service):
    results = service.users().messages().list(userId='me',
                                              labelIds=['INBOX'],
                                              q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        gmails = []
        messages_count = 0
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            messages_count += 1
            gmails.append(msg)

        print(f"You have {str(messages_count)} unread messages.")
        speak(f"You have {str(messages_count)} unread messages.")
        print("Would you like to see your messages: ")
        speak("Would you like to see your messages: ")
        message_choice = get_audio().lower()

        if message_choice == "yes":
            speak("How many messages you want to display:")
            print("How many messages you want to display:")
            number_of_emails = int(get_audio())
            if number_of_emails == isinstance(number_of_emails, int):
                for gmail in gmails[:number_of_emails]:
                    email_data = gmail["payload"]["headers"]
                    for values in email_data:
                        name = values["name"]
                        if name == "From":
                            from_name = values["value"]
                            print(f"You have a new message from: {from_name}")
                            speak(f"You have a new message from: {from_name}")
                            print(f"\t{gmail['snippet'][:50]} etc.")
                            speak(f"{gmail['snippet'][:50]} etc.")
            else:
                print("I didn't understand")
                speak("I didn't understand")



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
                        get_events(date, CALENDAR_SERVICE)
                    else:
                        speak("I don't understand")

            for phrase in NOTE_STRS:
                if phrase in text:
                    speak("What would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I've made a note of that.")

            for phrase in GMAIL_STRS:
                if phrase in text:
                    get_messages_from_gmail(GMAIL_SERVICE)

            for phrase in STOP:
                if phrase in text:
                    to_stop.append(phrase)

            if len(to_stop) > 0:
                speak("See you soon!")
                break