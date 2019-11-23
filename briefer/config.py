from getpass import getpass
from pathlib import Path
from string import capwords

import ruamel.yaml as yaml

DEFAULT_CFG_DIR = Path('~/.config/briefer').expanduser()
DEFAULT_CFG_FILE = DEFAULT_CFG_DIR / Path('app_config.yaml')
CFG_KEYS = ['sender', 'password', 'receiver', 'server', 'port', 'news api key']


class Config:
    """Main config"""
    def __init__(self):
        self.cfg_dir = DEFAULT_CFG_DIR
        self.cfg_file = DEFAULT_CFG_FILE

        # App defaults
        self.smtp = {
            'sender': '',
            'password': '',
            'receiver': '',
            'server': 'smtp.gmail.com',
            'port': 465,
            'news api key': '',
        }

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
    print('Note: Enter blank to make no change.')
    for key in CFG_KEYS:
        if key == 'password':
            cfg.smtp[key] = (
                getpass(f'{capwords(key, sep=". ")} [*]? ').strip()
                or
                cfg.smtp[key])
        else:
            cfg.smtp[key] = (
                input(f'{capwords(key, sep=". ")} [{cfg.smtp[key]}]? ').strip()
                or
                cfg.smtp[key])

    cfg.save()
    return cfg


if __name__ == '__main__':
    update_config_cli()
