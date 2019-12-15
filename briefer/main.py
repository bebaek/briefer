import argparse
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from briefer.config import Config, update_config_cli
from briefer.content_view import get_html_part


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
    """Run config command. Make configuration changes and save them."""
    update_config_cli()


def send():
    """Run send command. Compose and send an email."""

    # Get config
    cfg = Config()

    # Prep message
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Daily briefing by Briefer'
    message['From'] = cfg.smtp['sender']
    message['To'] = cfg.smtp['receiver']

    # Get contents
    html_str = get_html_part(cfg)

    # Complete message
    html_part = MIMEText(html_str, 'html')
    message.attach(html_part)

    # Send mail
    send_mail(message, **cfg.smtp)


def html():
    """Run html command. Compose and show HTML message to send."""
    import os
    from tempfile import NamedTemporaryFile
    from urllib.request import pathname2url

    # Get config
    cfg = Config()

    # Get contents
    html_str = get_html_part(cfg)

    # Save to a tempfile to render
    with NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_str)

    # Use BROWSER environment variable for browser preference
    if 'BROWSER' not in os.environ:
        os.environ['BROWSER'] = f'firefox{os.pathsep}w3m'

    # Somehow webbrowser should be imported after the env variable is set.
    # Otherwise, 'firefox:w3m' doesn't get parsed correctly.
    import webbrowser
    webbrowser.open(pathname2url(f.name))


def main():
    """Entry point"""

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='config, send, or html')
    args = parser.parse_args()

    # Run command
    if args.command == 'config':
        config()
    elif args.command == 'send':
        send()
    elif args.command == 'html':
        html()


if __name__ == '__main__':
    main()
