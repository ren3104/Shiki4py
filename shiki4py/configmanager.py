import os.path
import configparser


class ConfigManager:
    def __init__(self, client_id):
        self.client_id = client_id
        self.config = configparser.ConfigParser()
        self._load()

    def add(self, token):
        self.config.add_section(self.client_id)
        self.config.set(self.client_id, 'token', token)
        self._save()

    def update(self, option, value):
        self.config.set(self.client_id, option, value)
        self._save()

    def get(self):
        if self.config.has_section(self.client_id):
            return dict(self.config.items(self.client_id))
        else:
            return None

    def _save(self):
        self.config.write(open('config.ini', 'w'))

    def _load(self):
        if not os.path.exists('config.ini'):
            return None

        self.config.read('config.ini')
