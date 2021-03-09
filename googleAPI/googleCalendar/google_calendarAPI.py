from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_google_calendar():
    credentials = None

    if os.path.exists('googleAPI/googleCalendar/token.pickle'):
        with open('googleAPI/googleCalendar/token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('googleAPI/googleCalendar/credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('googleAPI/googleCalendar/token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('calendar', 'v3', credentials=credentials)
    return service
