from getpass import getpass
from pathlib import Path

import ruamel.yaml as yaml

DEFAULT_CFG_DIR = Path('~/.config/briefer').expanduser()
DEFAULT_CFG_FILE = DEFAULT_CFG_DIR / Path('app_config.yaml')


class Config:
    """Main config"""
    def __init__(self):
        self.cfg_dir = DEFAULT_CFG_DIR
        self.cfg_file = DEFAULT_CFG_FILE
        self.smtp = {
            'sender': None,
            'password': None,
            'receiver': None,
            'server': 'smtp.gmail.com',
            'port': 465,
        }

    def load(self):
        with self.cfg_file.open(mode='r') as f:
            self.smtp = yaml.safe_load(f)

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

    # FIXME: Validate input formats
    cfg.smtp['sender'] = input('Sender address? ')
    cfg.smtp['password'] = getpass('Sender password? ')
    cfg.smtp['receiver'] = input('Receiver address? ')
    cfg.smtp['server'] = (
        input(f'SMTP server address? [{cfg.smtp["server"]}] ').strip()
        or cfg.smtp['server'])
    cfg.smtp['port'] = (
        input(f'SMTP port? [{cfg.smtp["port"]}] ').strip() or cfg.smtp['port'])

    cfg.save()
    return cfg


if __name__ == '__main__':
    update_config_cli()
