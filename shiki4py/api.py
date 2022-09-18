from __future__ import annotations

from typing import Optional

from shiki4py.base import Client
from shiki4py.resources import *
from shiki4py.store import BaseTokenStore


class Shikimori:
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
        self.client = Client(
            app_name, client_id, client_secret, store, base_url, token_url, redirect_uri
        )
        self.animes = Animes(self.client)
        self.comments = Comments(self.client)
        self.users = Users(self.client)

    @property
    def closed(self) -> bool:
        return self.client.closed

    async def open(self) -> Shikimori:
        await self.client.open()
        return self

    async def close(self) -> None:
        await self.client.close()

    async def __aenter__(self) -> Shikimori:
        return await self.open()

    async def __aexit__(self, *args) -> None:
        await self.close()
