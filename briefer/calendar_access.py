import requests
from datetime import datetime, timedelta
from requests.utils import quote

import pytz

from briefer.config import Config


def get_new_access_token(client_id, client_secret, refresh_token):
    """Use long-lived refresh token to get short-lived access token."""
    response = requests.post(
        'https://www.googleapis.com/oauth2/v4/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
    )
    response.raise_for_status()
    access_token = response.json()['access_token']
    return access_token


def get_calendar_list(access_token):
    """Get all subscribed calendar IDs."""
    response = requests.get(
        'https://www.googleapis.com/calendar/v3/users/me/calendarList',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    response.raise_for_status()

    items = response.json()['items']
    calendar_ids = [item['id'] for item in items]
    tz = items[0]['timeZone']
    return calendar_ids, tz


def get_calendar_events():
    """Return today's calendar events."""
    cfg = Config()

    # Get new access token
    access_token = get_new_access_token(
        cfg.smtp['calendar client ID'],
        cfg.smtp['calendar client secret'],
        cfg.smtp['calendar refresh token'],
    )

    # Get calendar IDs
    calendar_ids, tz = get_calendar_list(access_token)

    # Get calendar events
    events = {}
    for id_ in calendar_ids:
        events[id_] = _get_events(access_token, id_, tz)

    return _events_to_html(events)


def _get_events(access_token, id_, tz):
    """Return events from a single calendar."""
    CAL_KEYS = ['start', 'end', 'summary']

    # Filter with current datetime
    lo_dt = datetime.now(pytz.timezone(tz))
    hi_dt = lo_dt + timedelta(days=30)

    response = requests.get(
        'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(
            quote(id_)),
        params={
            'maxResults': 5,
            'timeMin': lo_dt.isoformat(),
            'timeMax': hi_dt.isoformat()},
        headers={'Authorization': f'Bearer {access_token}'},
    )
    response.raise_for_status()

    res_list = []
    for item in response.json()['items']:
        res_dict = {}
        for key in CAL_KEYS:
            res_dict[key] = item[key]
        res_list += [res_dict]
    return res_list


def _events_to_html(events):
    """Convert calendar event dictionary to string for html doc."""
    # FIXME: improve
    msg = '<p><b>Calendars</b></p>\n\n'
    msg += f'<p>{str(events)}<p>\n\n'
    return msg


if __name__ == '__main__':
    html = get_calendar_events()
    print(html)
