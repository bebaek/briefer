from pathlib import Path
import sys

import ruamel.yaml as yaml

DEFAULT_CFG_DIR = Path('~/.config/briefer').expanduser()
DEFAULT_CFG_FILE = DEFAULT_CFG_DIR / Path('app_config.yaml')


class Config:
    """Main config"""
    def __init__(self):
        self.cfg_dir = DEFAULT_CFG_DIR
        self.cfg_file = DEFAULT_CFG_FILE
        self.sender = {'address': None, 'password': None}
        self.receiver = {'address': None, 'password': None}

    def load(self):
        with self.cfg_file.open(mode='r') as f:
            contents = yaml.safe_load(f)
        self.sender = contents['sender']
        self.receiver = contents['receiver']

    def save(self):
        contents = {'sender': self.sender, 'receiver': self.receiver}

        # Create config dir as needed
        self.cfg_dir.mkdir(mode=0o700, exist_ok=True)

        # Check dir mode
        mode = self.cfg_dir.stat().st_mode
        if mode & 0o077:
            print(
                f'Insecure ({mode & 0o07777:o}) config dir {self.cfg_dir}.')
            sys.exit(1)

        # Write to config file
        try:
            self.cfg_file.unlink()
        except FileNotFoundError:
            pass
        self.cfg_file.touch(mode=0o600)  # Contains secret
        with self.cfg_file.open(mode='w') as f:
            yaml.dump(contents, f, default_flow_style=False)


def update_config_cli():
    """Get config from command line and write to a file"""
    cfg = Config()

    # FIXME: Validate input formats
    cfg.sender['address'] = input('Sender address? ')
    cfg.sender['password'] = input('Sender password? ')
    cfg.receiver['address'] = input('Receiver address? ')
    cfg.receiver['password'] = input('Receiver password? ')

    cfg.save()


if __name__ == '__main__':
    update_config_cli()
