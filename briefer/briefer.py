import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config, update_config_cli


def send_mail_local():
    port = 1025
    smtp_server = 'localhost'
    sender_email = 'foo@mymail.com'
    receiver_email = 'bar@mymail.com'
    message = 'Test email'

    with smtplib.SMTP(smtp_server, port) as server:
        server.sendmail(sender_email, receiver_email, message)


def send_mail(message, **kwargs):
    """Send email through secure SMTP server.

    Parameters
    ----------
    message : MIMEMultipart
    **kwargs
        sender, password, receiver, server, port
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
            kwargs['server'], kwargs['port'], context=context) as server:
        server.login(kwargs['sender'], kwargs['password'])
        server.sendmail(
            kwargs['sender'], kwargs['receiver'], message.as_string())


def get_news(api_key):
    """Return news headline string"""
    url = f'https://newsapi.org/v2/top-headlines?country=us&apikey={api_key}'
    response = requests.get(url).json()
    selected_news = response['articles'][:3]
    titles = []
    urls = []
    for news in selected_news:
        titles += [news['title']]
        urls += [news['url']]

    # Compose HTML content
    msg = '<p><b>News Headlines</p>\n\n'
    for title, url in zip(titles, urls):
        msg += f'<p><a href="{url}">{title}</a></p>\n'

    # Add attribution:
    msg += (
        '<p>Powered by <a href="https://newsapi.org">NewsAPI.org</a></p>\n\n')
    return msg


def main():
    """Entry point"""
    # Get config
    cfg = Config()
    try:
        cfg.load()
    except FileNotFoundError:
        cfg = update_config_cli()

    # Prep message
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Daily briefing by Briefer'
    message['From'] = cfg.smtp['sender']
    message['To'] = cfg.smtp['receiver']
    html_tmpl = """
      <html>
        <body>
          {content}
        </body>
      </html>
    """
    content = ''

    # Get news
    content += get_news(cfg.smtp['news api key'])

    # Complete message
    html_str = html_tmpl.format(content=content)
    html_part = MIMEText(html_str, 'html')
    message.attach(html_part)

    # Send mail
    send_mail(message, **cfg.smtp)


if __name__ == '__main__':
    main()
