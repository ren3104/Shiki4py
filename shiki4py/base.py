from __future__ import annotations

import logging
import textwrap
from datetime import datetime as dt
from typing import Any, Dict, MutableMapping, Optional, Union

from aiohttp import ClientError, ClientSession, hdrs
from pyrate_limiter import Duration, Limiter, RequestRate

from shiki4py.exceptions import TooManyRequests
from shiki4py.store import BaseTokenStore
from shiki4py.store.env import EnvTokenStore
from shiki4py.utils import retry_backoff

log = logging.getLogger("shiki4py")


class Client:
    _base_limiter = Limiter(
        RequestRate(5, Duration.SECOND), RequestRate(90, Duration.MINUTE)
    )

    def __init__(
        self,
        app_name: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        store: Optional[BaseTokenStore] = None,
        base_url: str = "https://shikimori.one",
        token_url: str = "/oauth/token",
        redirect_uri: str = "urn:ietf:wg:oauth:2.0:oob",
    ) -> None:
        self._app_name = app_name
        self._client_id = client_id
        self._client_secret = client_secret

        self._store = store

        self._base_url = base_url
        self._token_url = token_url
        self._redirect_uri = redirect_uri

        self._session = None

    @property
    def closed(self) -> bool:
        return self._session == None

    async def open(self) -> Client:
        if self.closed:
            self._session = ClientSession(self._base_url)
            self._session.headers.update(
                {
                    "User-Agent": self._app_name,
                    "Accept": "application/json, text/plain, */*",
                }
            )

            if self._client_id and self._client_secret:
                if not self._store:
                    self._store = EnvTokenStore()

                cur_token = self._store.fetch(self._client_id)
                if cur_token:
                    self._apply_access_token(cur_token)
                else:
                    await self._get_access_token()
        return self

    async def close(self) -> None:
        if not self.closed:
            await self._session.close()
            self._session = None

    @retry_backoff(TooManyRequests, max_time=5)
    @_base_limiter.ratelimit("base_shikimori", delay=True)
    async def request(
        self, url: str, method: str = hdrs.METH_GET, **kwargs
    ) -> Optional[Union[Dict[str, Any], str]]:
        if self.closed:
            return

        if url != self._token_url and self._check_access_token():
            await self._refresh_access_token()

        try:
            resp = await self._session.request(method, url, **kwargs)
            if resp.status == 429:
                raise TooManyRequests()
            else:
                resp.raise_for_status()
        except ClientError as e:
            await self.close()
            log.error(
                textwrap.dedent(
                    """
                ---------------- request ----------------
                {req.method} {req.url}
                {reqhdrs}
                ---------------- response ---------------
                {res.status} {res.reason} {res.url}
                {reshdrs}

                {res.text}
            """
                ).format(
                    req=resp.request_info,
                    res=resp,
                    reqhdrs=self._formatHeaders(resp.request_info.headers),
                    reshdrs=self._formatHeaders(resp.headers),
                )
            )
            raise e

        log.info(f"{resp.method} {resp.status} {resp.url}")

        if resp.content_type == "application/json":
            return await resp.json()
        else:
            return await resp.text()

    def _formatHeaders(self, d: MutableMapping) -> str:
        return "\n".join(f"{k}: {v}" for k, v in d.items())

    async def _get_access_token(self) -> None:
        code = input("Введи код авторизации (Authorization Code): ")
        token = await self.request(
            self._token_url,
            hdrs.METH_POST,
            data={
                "grant_type": "authorization_code",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "code": code,
                "redirect_uri": self._redirect_uri,
            },
        )
        self._store.save(self._client_id, token)
        log.info(f"Get access token for {self._client_id}")
        self._apply_access_token(token)

    async def _refresh_access_token(self) -> None:
        cur_token = self._store.fetch(self._client_id)
        if cur_token:
            self._session.headers.pop("Authorization")
            new_token = await self.request(
                self._token_url,
                hdrs.METH_POST,
                data={
                    "grant_type": "refresh_token",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "refresh_token": cur_token["refresh_token"],
                },
            )
            self._store.save(self._client_id, new_token)
            log.info(f"Refresh access token for {self._client_id}")
            self._apply_access_token(new_token)

    def _apply_access_token(self, token: Dict[str, Any]) -> None:
        self._session.headers.update(
            {"Authorization": f"{token['token_type']} {token['access_token']}"}
        )
        log.info(f"Apply access token for {self._client_id}")

    def _check_access_token(self) -> bool:
        if self._client_id and self._client_secret:
            cur_token = self._store.fetch(self._client_id)
            if cur_token:
                token_expire_at = dt.fromtimestamp(
                    int(cur_token["created_at"]) + int(cur_token["expires_in"])
                )
                return dt.now() > token_expire_at
        return False

    async def __aenter__(self) -> Client:
        return await self.open()

    async def __aexit__(self, *args) -> None:
        await self.close()
