from __future__ import print_function

import base64
import os.path
import pickle
from email import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from additional_functions.logger import get_logger
from additional_functions.before_start import is_valid_email
from additional_functions.VA_config import speak, get_speak_engine, get_audio

SCOPES = ["https://mail.google.com/"]
ENGINE = get_speak_engine()

logger = get_logger("google_gmail")


def authenticate_google_gmail():
    logger.info("Authenticating user to Google Gmail")
    credentials = None
    if os.path.exists('googleAPI/googleGmail/secret_token.json'):
        logger.info("Secret Gmail token exists. User was found")
        credentials = Credentials.from_authorized_user_file('googleAPI/googleGmail/secret_token.json', SCOPES)
    if not credentials or not credentials.valid:
        logger.info("Secret Gmail token does not exists. Redirecting user to Google")
        if credentials and credentials.expired and credentials.refresh_token:
            logger.info("Refreshing Google Gmail token")
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('googleAPI/googleGmail/credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('googleAPI/googleGmail/secret_token.json', 'w') as token:
            logger.info("Creating new Google Gmail token")
            token.write(credentials.to_json())
        logger.info("New Google Gmail token was created successfully")
    gmail_service = build('gmail', 'v1', credentials=credentials)
    return gmail_service


def get_unread_gmail_messages(gmail_service):
    global msg
    logger.info("Getting unread messages")
    results = gmail_service.users().messages().list(userId='me', labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        logger.info("Zero messages found")
        speak(ENGINE, "You have no messages")
    else:
        message_count = 0
        for message in messages:
            msg = gmail_service.users().messages().get(userId="me", id=message['id']).execute()
            message_count += 1
        logger.info("%s unread messages found" % str(message_count))
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
        else:
            speak(ENGINE, "Oki, I won't show it.")
        mark_as_read(gmail_service, messages)
        delete_message(gmail_service, messages)


def mark_as_read(gmail_service, messages: list):
    speak(ENGINE, "Would you like to mark these messages as read?")
    if "yes" in get_audio().lower():
        speak(ENGINE, "Ok, I'll mark these messages as read.")
        logger.info("Marking messages as read")
        return gmail_service.users().messages().batchModify(
            userId="me",
            body={'removeLabelIds': ["UNREAD"], 'ids': [message["id"] for message in messages]}
        ).execute()
    else:
        speak(ENGINE, "Okay, I won't mark these messages as read.")


def delete_message(gmail_service, messages: list):
    speak(ENGINE, "Would you like to delete these messages?")
    if "yes" in get_audio().lower():
        logger.info("Deleting unread messages")
        speak(ENGINE, "Ok, I'll delete these messages.")
        return gmail_service.users().messages().batchDelete(
            userId="me",
            body={"ids": [message["id"] for message in messages]}
        ).execute()
    else:
        speak(ENGINE, "Okay, I won't delete these messages.")


def send_email_message(gmail_service):
    global email_content
    speak(ENGINE, "Who do you want to send the letter to?")
    send_to_user = input("Receiver:\n")
    while not is_valid_email(send_to_user):
        speak(ENGINE, "This email is not correct")
        send_to_user = input("Your email address is:\n")
    speak(ENGINE, "What is the subject of this letter?")
    email_subject = input("Email subject:\n")
    speak(ENGINE, "Okay. Do you want to say or type your message? (Say 'type' or 'say')")
    user_response = get_audio().lower()
    if "say" in user_response:
        speak(ENGINE, "What is the content of this message?")
        email_content = get_audio().lower()
    elif "type" in user_response:
        speak(ENGINE, "What is the content of this message?")
        email_content = input("Your message below:\n")
    with open("user_info.pickle", "rb") as openfile:
        try:
            user_email = pickle.load(openfile)["email"]
        except EOFError:
            print("Sorry, I don't know your email address. Type below your Google Gmail Address")
            user_email = input("Your email address is:\n")
            while not is_valid_email(user_email):
                speak(ENGINE, "This email is not correct")
                user_email = input("Your email address is:\n")
    message = MIMEText(email_content)
    message["to"] = send_to_user
    message["from"] = user_email
    message["subject"] = email_subject
    try:
        gmail_service.users().messages().send(
            userId='me',
            body={'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        ).execute()
        speak(ENGINE, "Your message has been sent.")
    except errors.MessageError as error:
        print("An ERROR occurred: %s" % error)
