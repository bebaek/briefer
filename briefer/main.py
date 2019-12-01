import argparse
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from briefer.config import Config, update_config_cli
from briefer.calendar_access import get_calendar_events
from briefer.news_access import get_news


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


def config():
    """Run config command"""
    update_config_cli()


def send():
    """Run send command"""
    # Get config
    cfg = Config()

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

    # Get calendar
    content += get_calendar_events()

    # Complete message
    html_str = html_tmpl.format(content=content)
    html_part = MIMEText(html_str, 'html')
    message.attach(html_part)

    # Send mail
    send_mail(message, **cfg.smtp)


def main():
    """Entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='config or send')
    args = parser.parse_args()

    # Run command
    if args.command == 'config':
        config()
    elif args.command == 'send':
        send()


if __name__ == '__main__':
    main()
