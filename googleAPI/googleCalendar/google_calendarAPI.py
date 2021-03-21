from __future__ import print_function
import datetime
import os.path

import pytz
from tzlocal import get_localzone
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from additional_functions.logger import get_logger

SCOPES = ['https://www.googleapis.com/auth/calendar']

logger = get_logger("google_calendar")


def authenticate_google_calendar():
    logger.info("Authenticating user to Google Calendar")
    credentials = None
    if os.path.exists('googleAPI/googleCalendar/secret_token.json'):
        logger.info("Secret Calendar token exists. User was found")
        credentials = Credentials.from_authorized_user_file('googleAPI/googleCalendar/secret_token.json', SCOPES)
    if not credentials or not credentials.valid:
        logger.info("Secret Calendar token does not exists. Redirecting user to Google")
        if credentials and credentials.expired and credentials.refresh_token:
            logger.info("Refreshing Google Calendar token")
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'googleAPI/googleCalendar/credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('googleAPI/googleCalendar/secret_token.json', 'w') as token:
            logger.info("Creating new Google Calendar token")
            token.write(credentials.to_json())
        logger.info("New Google Calendar token was created successfully")
    google_calendar_service = build('calendar', 'v3', credentials=credentials)
    return google_calendar_service


def get_google_calendar_events(date, google_calendar_service):
    logger.info("Getting events from Google Calendar")
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(date, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = google_calendar_service.events().list(calendarId='primary',
                                                          timeMin=date.isoformat(),
                                                          timeMax=end_date.isoformat(), singleEvents=True,
                                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def create_google_calendar_event(google_calendar_service):
    logger.info("Creating new event from Google Calendar")
    summary = input("Summary: ")
    location = input("Location (optional): ")
    description = input("Description (optional): ")
    start_time_date = input("Start date and time (For example: 2021-03-13 18:00:00)")
    end_time_date = input("Start date and time (For example: 2021-03-13 18:00:00)")

    return google_calendar_service.events().insert(
        calendarId='primary',
        body={
            'summary': '%s' % summary,
            'location': '%s' % location,
            'description': '%s' % description,
            'start': {
                'dateTime': '%s' % datetime.datetime.strptime(start_time_date, "%Y-%m-%d %H:%M:%S").isoformat(),
                'timeZone': "%s" % get_localzone(),
            },
            'end': {
                'dateTime': '%s' % datetime.datetime.strptime(end_time_date, "%Y-%m-%d %H:%M:%S").isoformat(),
                'timeZone': "%s" % get_localzone(),
            }
        }
    ).execute()
