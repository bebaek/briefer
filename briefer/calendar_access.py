import re
from datetime import datetime, timedelta

import pytz
import requests
from requests.utils import quote

TIMEOUT = 10

# datetime formats
D_R_FMT = '%Y-%m-%d'
DT_R_FMT = '%Y-%m-%dT%H:%M:%S%z'
D_O_FMT = '%a %b %d, %Y'
DT_O_FMT = '%a %b %d %I:%M %p, %Y %Z'

# date/datetime patterns from the calendar API
p_date = re.compile(r'\d\d\d\d-\d\d-\d\d')
p_datetime = re.compile(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d')


def get_new_access_token(client_id, client_secret, refresh_token):
    """Use long-lived refresh token to get short-lived access token."""

    response = requests.post(
        'https://www.googleapis.com/oauth2/v4/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    access_token = response.json()['access_token']
    return access_token


def get_calendar_list(access_token):
    """Get all subscribed calendar IDs."""

    response = requests.get(
        'https://www.googleapis.com/calendar/v3/users/me/calendarList',
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    items = response.json()['items']
    calendar_ids = [item['id'] for item in items]
    tz = items[0]['timeZone']
    return calendar_ids, tz


def get_calendar_events(config):
    """Return today's calendar events."""

    # Get new access token
    access_token = get_new_access_token(
        config.smtp['calendar client ID'],
        config.smtp['calendar client secret'],
        config.smtp['calendar refresh token'],
    )

    # Get calendar IDs
    calendar_ids, tz = get_calendar_list(access_token)

    # Get calendar events
    events = {}
    for id_ in calendar_ids:
        events[id_] = _get_events(access_token, id_, tz)

    return _events_to_list(events)


def _get_events(access_token, id_, tz):
    """Return events from a single calendar."""

    # Filter with current datetime
    lo_dt = datetime.now(pytz.timezone(tz))
    hi_dt = lo_dt + timedelta(hours=48)

    response = requests.get(
        'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(
            quote(id_)),
        params={
            'maxResults': 25,
            'singleEvents': True,
            'timeMin': lo_dt.isoformat(),
            'timeMax': hi_dt.isoformat()},
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=TIMEOUT,
    )
    response.raise_for_status()

    res_list = []
    for item in response.json()['items']:
        try:
            res_dict = {
                'start': item['start']['dateTime'],
                'end': item['end']['dateTime'],
                'summary': item['summary'],
            }
        except KeyError:
            res_dict = {
                'start': item['start']['date'],
                'end': item['end']['date'],
                'summary': item['summary'],
            }
        res_list += [res_dict]
    return res_list


def _events_to_list(events):
    """Convert calendar event dictionary to chronologically-ordered list."""

    res = []
    for val in events.values():
        res.extend(val)
    res.sort(key=lambda x: x['start'])

    # Use human-friendly formats for date and datetime
    for item in res:
        try:
            item['start'] = _human_friendly_date(item['start'])
            item['end'] = _human_friendly_date(item['end'])
        except ValueError:
            item['start'] = _human_friendly_datetime(item['start'])
            item['end'] = _human_friendly_datetime(item['end'])

    return res


def _human_friendly_date(s):
    # Check the date format
    if not p_date.match(s):
        raise ValueError(f'Unexpected date string format: {s}')

    return datetime.strptime(s, D_R_FMT).strftime(D_O_FMT)


def _human_friendly_datetime(s):
    # Check the datetime format
    if not p_datetime.match(s):
        raise ValueError(f'Unexpected datetime string format: {s}')

    # Change timezone part from HH:MM to HHMM
    res = s[:-3] + s[-2:]

    return datetime.strptime(res, DT_R_FMT).strftime(DT_O_FMT)


if __name__ == '__main__':
    from briefer.config import Config

    cfg = Config()
    res = get_calendar_events(cfg)
    print(res)
