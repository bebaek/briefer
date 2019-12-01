from datetime import datetime, timedelta

import pytz
import requests
from requests.utils import quote


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
            'timeMin': lo_dt.isoformat(),
            'timeMax': hi_dt.isoformat()},
        headers={'Authorization': f'Bearer {access_token}'},
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
    return res


if __name__ == '__main__':
    from briefer.config import Config

    cfg = Config()
    res = get_calendar_events(cfg)
    print(res)
