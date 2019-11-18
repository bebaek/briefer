import smtplib
import ssl

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
    **kwargs
        sender, password, receiver, server, port
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
            kwargs['server'], kwargs['port'], context=context) as server:
        server.login(kwargs['sender'], kwargs['password'])
        server.sendmail(kwargs['sender'], kwargs['receiver'], message)


def main():
    """Entry point"""
    # Get config
    cfg = Config()
    try:
        cfg.load()
    except FileNotFoundError:
        cfg = update_config_cli()

    # Compose message
    message = 'Test email'

    # Send mail
    send_mail(message, **cfg.smtp)


if __name__ == '__main__':
    main()
