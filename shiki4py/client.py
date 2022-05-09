from .tokensmanager import TokensManager
from .logmanager import LogManager
from datetime import datetime as dt
from requests import RequestException, HTTPError, JSONDecodeError
from requests_ratelimiter import LimiterSession, Limiter, RequestRate


class Client:
    RPS = 5
    RPM = 90

    comments_limiter = Limiter(RequestRate(1, 4))

    def __init__(self, app_name, api_endpoint='https://shikimori.one/api/'):
        self.api_endpoint = api_endpoint
        self.app_name = app_name
        self.isAuth = False

        self.lm = LogManager()

        self.headers = {
            'User-Agent': self.app_name
        }

        self.session = LimiterSession(per_second=self.RPS, per_minute=self.RPM)
        self.session.headers.update(self.headers)
    
    def auth(self, client_id, client_secret,
             token_endpoint='https://shikimori.one/oauth/token',
             redirect_uri='urn:ietf:wg:oauth:2.0:oob'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.redirect_uri = redirect_uri
        self.tm = TokensManager(client_id)

        token = self.tm.get()
        if len(token) > 0:
            self._applyAccessToken(token)
        else:
            self._getAccessToken()
        self.isAuth = True

        return self

    def _getAccessToken(self):
        code = input('Введи код авторизации (Authorization Code): ')

        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        token = self._request('post', self.token_endpoint, data=data)
        self.tm.set(token)
        self._applyAccessToken(token)

    def _refreshAccessToken(self):
        old_token = self.tm.get()
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': old_token['refresh_token']
        }
        self.session.headers.pop('Authorization')
        new_token = self._request('post', self.token_endpoint, data=data)
        self.tm.set(new_token)
        self._applyAccessToken(new_token)

    def _applyAccessToken(self, token):
        self.headers['Authorization'] = f"{token['token_type']} {token['access_token']}"
        self.session.headers.update(self.headers)

    def _checkAccessToken(self):
        token = self.tm.get()
        return dt.now() > dt.fromtimestamp(token['created_at'] + token['expires_in'])

    def _request(self, method, url, **kwargs):
        try:
            r = self.session.request(method, url, **kwargs)
            r.raise_for_status()
        except (RequestException, HTTPError):
            self.lm.requestError(r)
            print(f"Request error: {r.status_code} {r.reason}. Check the logs.")
            return None

        try:
            if len(r.text) > 0:
                data = r.json()
        except JSONDecodeError:
            self.lm.requestError(r)
            print(f"JSONDecodeError. Check the logs.")
            data = None

        return data

    def _api_request(self, method, path, **kwargs):
        if self.isAuth and self._checkAccessToken():
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
    
    @comments_limiter.ratelimit('comments_limiter', delay=True)
    def create_comment(self, body, commentable_id, commentable_type,
                       broadcast=False, is_offtopic=False):
        return self.post('comments', json={
            'broadcast': broadcast,
            'comment': {
                'body': body,
                'commentable_id': commentable_id,
                'commentable_type': commentable_type,
                'is_offtopic': is_offtopic
            },
            'frontend': False
        })
