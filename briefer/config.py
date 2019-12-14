from copy import deepcopy
from getpass import getpass
from pathlib import Path
from string import capwords

from cryptography.fernet import Fernet
import ruamel.yaml as yaml

CFG_DIR = Path('~/.config/briefer').expanduser()
CFG_FILE = CFG_DIR / Path('app_config.yaml')
OLD_CFG_FILE = CFG_DIR / Path('app_config.yaml.old')
CFG_KEYS = [
    # SMTP
    'sender',
    'password',
    'receiver',
    'server',
    'port',

    # News API
    'news api key',

    # Google calendar
    'calendar client ID',
    'calendar client secret',
    'calendar refresh token',
]

# Some fields are encrypted only to avoid the risk associated with a stolen
# config file and a brute-force attack on it without the knowledge of the
# implementation details. A better way could be the use of keyring or such to
# save the encryption key.
ENCRYPTED = [
    'password',
    'news api key',
    'calendar client secret',
    'calendar refresh token',
]
KEY = b'm2xKR8pN8LSJJ1ONkTwASrJvJYzyVu7bs_IYmKOhEUQ='


class Config:
    """Main config"""
    def __init__(self):
        self.cfg_dir = CFG_DIR
        self.cfg_file = CFG_FILE

        # App defaults
        # FIXME: rename or reorganize config variable
        self.smtp = {}
        for key in CFG_KEYS:
            self.smtp[key] = ''
        self.smtp['server'] = 'smtp.gmail.com'
        self.smtp['port'] = 465

        # Update from existing config file
        # FIXME: check required fields
        try:
            self.load()
        except FileNotFoundError:
            pass

    def load(self):
        smtp_copy = deepcopy(self.smtp)
        with self.cfg_file.open(mode='r') as f:
            smtp_copy.update(yaml.safe_load(f))

        # Decrypt some
        f = Fernet(KEY)
        for item in ENCRYPTED:
            msg = f.decrypt(smtp_copy[item].encode()).decode()
            smtp_copy[item] = msg

        self.smtp = smtp_copy

    def save(self):
        # Create a deep copy of parameter dict
        smtp_copy = deepcopy(self.smtp)

        # Encrypt some
        f = Fernet(KEY)
        for item in ENCRYPTED:
            token = f.encrypt(smtp_copy[item].encode()).decode()
            assert f.decrypt(token.encode()).decode() == self.smtp[item]
            smtp_copy[item] = token

        # Create config dir as needed
        self.cfg_dir.parent.mkdir(mode=0o700, exist_ok=True)
        self.cfg_dir.mkdir(mode=0o700, exist_ok=True)

        # Check dir mode
        mode = self.cfg_dir.stat().st_mode
        if mode & 0o077:
            print(
                f'Insecure ({mode & 0o07777:o}) config dir {self.cfg_dir}.')
            return

        # Write to config file
        try:
            self.cfg_file.rename(OLD_CFG_FILE)
        except FileNotFoundError:
            pass
        self.cfg_file.touch(mode=0o600)  # Contains secret
        with self.cfg_file.open(mode='w') as f:
            yaml.dump(smtp_copy, f, default_flow_style=False)


def update_config_cli():
    """Get config from command line and write to a file"""
    cfg = Config()

    # FIXME: improve CLI experience
    print('Note: Enter blank to keep the current value.')
    for key in CFG_KEYS:
        # Show (or hide) current value
        if key in ENCRYPTED:
            current = '*' if cfg.smtp[key] else ''
            cfg.smtp[key] = (
                getpass(f'{capwords(key, sep=". ")} [{current}]? ').strip()
                or
                cfg.smtp[key])
        else:
            current = cfg.smtp[key]
            cfg.smtp[key] = (
                input(f'{capwords(key, sep=". ")} [{current}]? ').strip()
                or
                cfg.smtp[key])

    cfg.save()
    return cfg


if __name__ == '__main__':
    update_config_cli()
