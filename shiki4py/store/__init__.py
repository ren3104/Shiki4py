class BaseTokenStore:
    def save(self, client_id, token):
        raise NotImplementedError

    def fetch(self, client_id):
        raise NotImplementedError
