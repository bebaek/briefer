from getpass import getpass
from pathlib import Path
from string import capwords

import ruamel.yaml as yaml

DEFAULT_CFG_DIR = Path('~/.config/briefer').expanduser()
DEFAULT_CFG_FILE = DEFAULT_CFG_DIR / Path('app_config.yaml')
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


class Config:
    """Main config"""
    def __init__(self):
        self.cfg_dir = DEFAULT_CFG_DIR
        self.cfg_file = DEFAULT_CFG_FILE

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
        with self.cfg_file.open(mode='r') as f:
            self.smtp.update(yaml.safe_load(f))

    def save(self):
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
            self.cfg_file.unlink()
        except FileNotFoundError:
            pass
        self.cfg_file.touch(mode=0o600)  # Contains secret
        with self.cfg_file.open(mode='w') as f:
            yaml.dump(self.smtp, f, default_flow_style=False)


def update_config_cli():
    """Get config from command line and write to a file"""
    cfg = Config()

    # FIXME: improve CLI experience
    print('Note: Enter blank to keep the current value.')
    for key in CFG_KEYS:
        # Show (or hide) current value
        if key in ['news api key', 'password']:
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
