from jinja2 import Environment, PackageLoader, select_autoescape

from briefer.calendar_access import get_calendar_events
from briefer.news_access import get_news


def get_html_part(config):
    """Return html email content."""
    # Prep template
    env = Environment(
        loader=PackageLoader('briefer', 'templates'),
        autoescape=select_autoescape(['html']),
    )
    template = env.get_template('main.html')

    # Get news
    titles, urls = get_news(config.smtp['news api key'])

    # Get calendar
    events = get_calendar_events(config)

    # Render
    html = template.render(news=zip(titles, urls), events=events)
    return html


def get_text_part():
    """Return text email content."""
    # FIXME: implement this placeholder
    pass
