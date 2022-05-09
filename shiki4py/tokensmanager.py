import os.path
import configparser


TOKEN_MAP = {
    'access_token': str,
    'token_type': str,
    'expires_in': int,
    'refresh_token': str,
    'scope': str,
    'created_at': int
}


class TokensManager:
    def __init__(self, client_id, file_name='tokens'):
        self.client_id = client_id
        self.file = file_name + '.ini'
        self.config = configparser.ConfigParser()

        if os.path.isfile(self.file):
            self.config.read(self.file)
        
        if not self.config.has_section(self.client_id):
            self.config.add_section(self.client_id)

    def get(self):
        d = self.config.items(self.client_id)
        return dict((k, TOKEN_MAP[k](v)) for k, v in d)

    def set(self, token):
        new_token = {self.client_id: token}
        self.config.update(new_token)
        self.config.write(open(self.file, 'w'))
