"""
Google API Access
"""
import datetime
from collections import namedtuple
import urllib2
import json

CALENDAR_ID = 't8e8kefpjj3jm430631q97mdcc@group.calendar.google.com'
API_KEY = 'AIzaSyArj3w57pt3zYtPnxxarFG_IwKn2oF_Wec'


Event = namedtuple('Event', ['title', 'date', 'link'])

cache = {}

def fetch_google_cal_events():
    """
    Fetches up to 10 Google Calendar events. Caches API calls to Google such
    that it only makes the request if the result was older than 5 minutes.

    Returns a list of Event objects.
    """

    d = datetime.datetime.now()
    last_fetch = cache.keys()

    if last_fetch and (d - last_fetch[0]).total_seconds < 300:
        return cache.values()[0]

    request_url = 'https://www.googleapis.com/calendar/v3/calendars/' \
        + CALENDAR_ID \
        + '/events?maxResults=10&orderBy=startTime&singleEvents=true&timeMin='\
        + str(d.year) + '-' + str(d.month) + '-' + str(d.day) + 'T' \
        + str(d.hour) + ':' + str(d.minute) + ':' + str(d.second) \
        + 'Z' '&key=' + API_KEY

    data = json.load(urllib2.urlopen(request_url))
    list_of_events = data['items']

    formatted_events = []
    for event in list_of_events:
        try:
            title = event['summary']
            date = event['start']['dateTime']
            date = date[5:10].replace("-", "/")
            link = event['htmlLink']
            formatted_events.append(Event(title, date, link))
        except:
            pass

    cache.clear()
    cache[d] = formatted_events

    return formatted_events




