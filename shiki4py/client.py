from shiki4py.store.ini import INITokenStore
from shiki4py.log import LogManager
from datetime import datetime as dt
from requests import RequestException, JSONDecodeError
from requests_ratelimiter import LimiterSession, Limiter, RequestRate


class Client:
    RPS = 5
    RPM = 90

    _comments_limiter = Limiter(RequestRate(1, 4))

    def __init__(self, app_name, client_id=None, client_secret=None,
                 debug=False, console=False, store=INITokenStore(),
                 api_endpoint='https://shikimori.one/api/',
                 token_endpoint='https://shikimori.one/oauth/token',
                 redirect_uri='urn:ietf:wg:oauth:2.0:oob'):
        self._api_endpoint = api_endpoint
        self._token_endpoint = token_endpoint
        self._redirect_uri = redirect_uri

        self._app_name = app_name
        self._client_id = client_id
        self._client_secret = client_secret

        self._log_manager = LogManager(debug, console)

        self._headers = {
            'User-Agent': self._app_name
        }

        self._session = LimiterSession(per_second=self.RPS, per_minute=self.RPM)
        self._session.headers.update(self._headers)

        if self._client_id and self._client_secret:
            self._store = store

            token = self._store.fetch(self._client_id)
            if token is None:
                self._getAccessToken()
            else:
                self._applyAccessToken(token)

    def _getAccessToken(self):
        code = input('Введи код авторизации (Authorization Code): ')
        data = {
            'grant_type': 'authorization_code',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'code': code,
            'redirect_uri': self._redirect_uri
        }
        token = self._request('post', self._token_endpoint, data=data)

        self._store.save(self._client_id, token)
        self._applyAccessToken(token)

    def _refreshAccessToken(self):
        old_token = self._store.fetch(self._client_id)
        data = {
            'grant_type': 'refresh_token',
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'refresh_token': old_token['refresh_token']
        }
        self._session.headers.pop('Authorization')
        new_token = self._request('post', self._token_endpoint, data=data)
        
        self._store.save(self._client_id, new_token)
        self._applyAccessToken(new_token)

    def _applyAccessToken(self, token):
        self._headers['Authorization'] = f"{token['token_type']} {token['access_token']}"
        self._session.headers.update(self._headers)

    def _checkAccessToken(self):
        if self._client_id and self._client_secret:
            token = self._store.fetch(self._client_id)
            if token is not None:
                return dt.now() > dt.fromtimestamp(int(token['created_at']) + int(token['expires_in']))
        return False

    def _request(self, method, url, **kwargs):
        try:
            r = self._session.request(method, url, **kwargs)
            r.raise_for_status()
        except RequestException as e:
            self._log_manager.requestError(r)
            raise e

        try:
            data = r.json()
        except JSONDecodeError:
            data = r.text

        return data

    def _api_request(self, method, path, **kwargs):
        if self._checkAccessToken():
            self._refreshAccessToken()

        if method != 'get':
            kwargs.update(({'headers': {'Content-Type': 'application/json'}}))

        url = self._api_endpoint + path
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

    @_comments_limiter.ratelimit('comments_limiter', delay=True)
    def create_comment(self, body, commentable_id, commentable_type,
                       broadcast=False, is_offtopic=False, frontend=False):
        return self.post('comments', json={
            'broadcast': broadcast,
            'comment': {
                'body': body,
                'commentable_id': commentable_id,
                'commentable_type': commentable_type,
                'is_offtopic': is_offtopic
            },
            'frontend': frontend
        })
