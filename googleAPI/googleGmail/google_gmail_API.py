from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from additional_functions.VA_config import speak, get_speak_engine, get_audio

SCOPES = ["https://mail.google.com/"]
ENGINE = get_speak_engine()


def authenticate_google_gmail():
    credentials = None
    if os.path.exists('googleAPI/googleGmail/secret_token.json'):
        credentials = Credentials.from_authorized_user_file('googleAPI/googleGmail/secret_token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'googleAPI/googleGmail/credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('googleAPI/googleGmail/secret_token.json', 'w') as token:
            token.write(credentials.to_json())

    service = build('gmail', 'v1', credentials=credentials)
    return service


def get_unread_gmail_messages(service):
    global msg
    results = service.users().messages().list(userId='me', labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        speak(ENGINE, "You have no messages")
    else:
        message_count = 0
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message['id']).execute()
            message_count += 1
        speak(ENGINE, "You have " + str(message_count) + " unread messages")
        speak(ENGINE, "Would you like to see your messages?")
        if "yes" in get_audio().lower():
            for _ in messages:
                email_data = msg["payload"]["headers"]
                for values in email_data:
                    name = values["name"]
                    if name == "From":
                        from_name = values["value"]
                        speak(ENGINE, "You have a new message from: " + from_name)
                        # speak(ENGINE, "      " + msg["snippet"][:50] + "...\n")
        else:
            speak(ENGINE, "Bye")
        mark_as_read(service, messages)
        delete_message(service, messages)


def mark_as_read(service, messages):
    speak(ENGINE, "Would you like to mark these messages as read?")

    if "yes" in get_audio().lower():
        speak(ENGINE, "Ok, I'll mark these messages as read.")
        return service.users().messages().batchModify(
            userId="me",
            body={'removeLabelIds': ["UNREAD"], 'ids': [message["id"] for message in messages]}
        ).execute()
    else:
        speak(ENGINE, "Okay, I won't mark these messages as read.")


def delete_message(service, messages):
    speak(ENGINE, "Would you like to delete these messages?")
    if "yes" in get_audio().lower():
        speak(ENGINE, "Ok, I'll delete these messages.")
        return service.users().messages().batchDelete(
            userId="me",
            body={"ids": [message["id"] for message in messages]}
        ).execute()
    else:
        pass
        speak(ENGINE, "Okay, I won't delete these messages.")

if __name__ == '__main__':
    service = authenticate_google_gmail()
    get_unread_gmail_messages(service)
