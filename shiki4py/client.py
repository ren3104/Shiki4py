from .configmanager import ConfigManager
from .logmanager import LogManager
import json
from datetime import datetime as dt
from requests import RequestException, JSONDecodeError
from requests_ratelimiter import LimiterSession


class Client:
    RPS = 5
    RPM = 90

    def __init__(self, app_name, client_id=None, client_secret=None,
                 api_endpoint='https://shikimori.one/api/',
                 token_endpoint='https://shikimori.one/oauth/token',
                 redirect_uri='urn:ietf:wg:oauth:2.0:oob'):

        self.api_endpoint = api_endpoint
        self.token_endpoint = token_endpoint

        self.app_name = app_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.lm = LogManager()

        self.headers = {
            'User-Agent': self.app_name
        }

        self.session = LimiterSession(per_second=self.RPS, per_minute=self.RPM)
        self.session.headers.update(self.headers)

        self.token = None
        if self.client_id is not None and self.client_secret is not None:
            self.cm = ConfigManager(self.client_id)
            config_section = self.cm.get()
            if config_section is None:
                self._getAccessToken()
            else:
                self.token = json.loads(config_section['token'])
            self._applyAccessToken()

    def _getAccessToken(self):
        code = input('Введи код авторизации (Authorization Code): ')

        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        r = self._request('post', self.token_endpoint, data=data)
        self.token = r
        self.cm.add(json.dumps(self.token))

    def _refreshAccessToken(self):
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.token['refresh_token']
        }
        self.session.headers.pop('Authorization')
        data = self._request('post', self.token_endpoint, data=data)
        if data is not None:
            self.token = data
            self.cm.update('token', json.dumps(self.token))
            self._applyAccessToken()

    def _applyAccessToken(self):
        self.headers['Authorization'] = f"{self.token['token_type']} {self.token['access_token']}"
        self.session.headers.update(self.headers)

    def _request(self, method, url, **kwargs):
        try:
            r = self.session.request(method, url, **kwargs)
        except RequestException:
            self.lm.requestError(r)
            print('Request error. Check the logs.')
            return None

        try:
            data = r.json()
        except JSONDecodeError:
            return None

        if 'error' in data:
            self.lm.requestError(r)
            print(f"Shikimori API error: {data['error']}. Check the logs.")
        elif 'errors' in data:
            self.lm.requestError(r)
            print(f"Shikimori API error: {data['errors']}. Check the logs.")

        return data

    def _api_request(self, method, path, **kwargs):
        if self.token is not None and dt.now() > dt.fromtimestamp(self.token['created_at'] + self.token['expires_in']):
            self._refreshAccessToken()

        if method != 'get':
            kwargs.update(({'headers': {'Content-Type': 'application/json'}}))

        url = self.api_endpoint + path
        return self._request(method, url, **kwargs)

    def get(self, path, params=None, **kwargs):
        kwargs.update({'params': params})
        return self._api_request('get', path, **kwargs)

    def post(self, path, json, **kwargs):
        kwargs.update({'json': json})
        return self._api_request('post', path, **kwargs)

    def put(self, path, json, **kwargs):
        kwargs.update({'json': json})
        return self._api_request('put', path, **kwargs)

    def patch(self, path, json, **kwargs):
        kwargs.update({'json': json})
        return self._api_request('patch', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._api_request('delete', path, **kwargs)
