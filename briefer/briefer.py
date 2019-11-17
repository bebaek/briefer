import smtplib

from config import Config


def send_mail():
    port = 1025
    smtp_server = 'localhost'
    sender_email = 'foo@mymail.com'
    receiver_email = 'bar@mymail.com'
    message = 'Test email'

    with smtplib.SMTP(smtp_server, port) as server:
        server.sendmail(sender_email, receiver_email, message)


def main():
    """Entry point"""
    cfg = Config()
    cfg.load()
    print(cfg.sender)
    print(cfg.receiver)


if __name__ == '__main__':
    main()
