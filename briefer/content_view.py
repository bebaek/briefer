from datetime import datetime

from jinja2 import Environment, PackageLoader, select_autoescape
from requests import Timeout
from tzlocal import get_localzone

from briefer.calendar_access import get_calendar_events
from briefer.news_access import get_news
from briefer.weather_access import get_weather


def get_html_part(config):
    """Return html email content."""

    # Prep template
    env = Environment(
        loader=PackageLoader('briefer', 'templates'),
        autoescape=select_autoescape(['html']),
    )
    template = env.get_template('main.html')

    # Get today
    today = datetime.now(get_localzone()).strftime('%a %b %d %I:%M %p, %Y %Z')

    # Get weather forecasts
    try:
        weather = get_weather(
            (config.smtp['longitude'], config.smtp['latitude']))
    except Timeout:
        weather = None

    # Get calendar events
    try:
        events = get_calendar_events(config)
    except Timeout:
        events = None

    # Get news headlines
    try:
        titles, urls = get_news(config.smtp['news api key'])
    except Timeout:
        titles, urls = [None], [None]

    # Render
    html = template.render(
        today=today,
        weather=weather,
        events=events,
        news=zip(titles, urls),
    )
    return html


def get_text_part():
    """Return text email content."""
    # FIXME: implement this placeholder
    pass
