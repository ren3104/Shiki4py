from shiki4py.store import BaseTokenStore
from shiki4py.store.ini import INITokenStore
from shiki4py.log import LogManager
from typing import Any, Dict, Optional
from datetime import datetime as dt
from requests import RequestException
from requests_ratelimiter import LimiterSession, Limiter, RequestRate


class Client:
    RPS = 5
    RPM = 90

    _comments_limiter = Limiter(RequestRate(1, 4))

    def __init__(self,
                 app_name: str,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 debug: bool = False,
                 console: bool = False,
                 store: BaseTokenStore = INITokenStore(),
                 api_endpoint: str = 'https://shikimori.one/api/',
                 token_endpoint: str = 'https://shikimori.one/oauth/token',
                 redirect_uri: str = 'urn:ietf:wg:oauth:2.0:oob') -> None:
        self._api_endpoint = api_endpoint
        self._token_endpoint = token_endpoint
        self._redirect_uri = redirect_uri

        self._app_name = app_name

        self._log_manager = LogManager(debug, console)

        self._headers = {
            'User-Agent': self._app_name
        }

        self._session = LimiterSession(per_second=self.RPS,
                                       per_minute=self.RPM)
        self._session.headers.update(self._headers)

        if client_id and client_secret:
            self._client_id = client_id
            self._client_secret = client_secret

            self._store = store

            token = self._store.fetch(self._client_id)
            if token is None:
                self._getAccessToken()
            else:
                self._applyAccessToken(token)

    def _getAccessToken(self) -> None:
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

    def _refreshAccessToken(self) -> None:
        old_token = self._store.fetch(self._client_id)
        if old_token:
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

    def _applyAccessToken(self, token: Dict[str, Any]) -> None:
        self._headers['Authorization'] = f"{token['token_type']} {token['access_token']}"
        self._session.headers.update(self._headers)

    def _checkAccessToken(self) -> bool:
        if self._client_id and self._client_secret:
            token = self._store.fetch(self._client_id)
            if token is not None:
                return dt.now() > dt.fromtimestamp(int(token['created_at']) + int(token['expires_in']))
        return False

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        try:
            r = self._session.request(method, url, **kwargs)
            r.raise_for_status()
        except RequestException as e:
            self._log_manager.requestError(r)
            raise e
        return r.json()

    def _api_request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        if self._checkAccessToken():
            self._refreshAccessToken()

        if method != 'get':
            kwargs.update(({'headers': {'Content-Type': 'application/json'}}))

        url = self._api_endpoint + path
        return self._request(method, url, **kwargs)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        kwargs.update({'params': params})
        return self._api_request('get', path, **kwargs)

    def post(self, path: str, json: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        kwargs.update({'json': json})
        return self._api_request('post', path, **kwargs)

    def put(self, path: str, json: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        kwargs.update({'json': json})
        return self._api_request('put', path, **kwargs)

    def patch(self, path: str, json: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        kwargs.update({'json': json})
        return self._api_request('patch', path, **kwargs)

    def delete(self, path: str, **kwargs) -> Dict[str, Any]:
        return self._api_request('delete', path, **kwargs)

    @_comments_limiter.ratelimit('comments_limiter', delay=True)
    def create_comment(self,
                       body: str,
                       commentable_id: int,
                       commentable_type: str,
                       broadcast: bool = False,
                       is_offtopic: bool = False,
                       frontend: bool = False) -> Dict[str, Any]:
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
