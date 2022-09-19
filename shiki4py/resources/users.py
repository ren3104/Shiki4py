from typing import List, Optional

import cattrs

from shiki4py.resources.base_resource import BaseResource
from shiki4py.types import (
    Ban,
    Club,
    Favourites,
    Message,
    UnreadMessages,
    User,
    UserHistory,
    UserInfo,
    UserProfile,
    UserRateFull,
)
from shiki4py.utils import prepare_params


class Users(BaseResource):
    async def show_one(self, user_id: int) -> UserProfile:
        resp = await self._request(f"/api/users/{user_id}")
        return cattrs.structure(resp, UserProfile)

    async def show_part(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> List[UserProfile]:
        resp = await self._request(
            "/api/users", params=prepare_params(page=page, limit=limit)
        )
        return [cattrs.structure(item, UserProfile) for item in resp]

    async def info(self, user_id: int) -> UserInfo:
        resp = await self._request(f"/api/users/{user_id}/info")
        return cattrs.structure(resp, UserInfo)

    async def my_info(self) -> UserInfo:
        resp = await self._request("/api/users/whoami")
        return cattrs.structure(resp, UserInfo)

    async def sign_out(self) -> bool:
        resp = await self._request("/api/users/sign_out")
        if resp == "signed out":
            return True
        return False

    async def friends(self, user_id: int) -> List[User]:
        resp = await self._request(f"/api/users/{user_id}/friends")
        return [cattrs.structure(item, User) for item in resp]

    async def clubs(self, user_id: int) -> List[Club]:
        resp = await self._request(f"/api/users/{user_id}/clubs")
        return [cattrs.structure(item, Club) for item in resp]

    async def anime_rates(
        self,
        user_id: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        status: Optional[str] = None,
        censored: Optional[bool] = None,
    ) -> List[UserRateFull]:
        resp = await self._request(
            f"/api/users/{user_id}/anime_rates",
            params=prepare_params(
                page=page, limit=limit, status=status, censored=censored
            ),
        )
        return [cattrs.structure(item, UserRateFull) for item in resp]

    async def manga_rates(
        self,
        user_id: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        status: Optional[str] = None,
        censored: Optional[bool] = None,
    ) -> List[UserRateFull]:
        resp = await self._request(
            f"/api/users/{user_id}/manga_rates",
            params=prepare_params(
                page=page, limit=limit, status=status, censored=censored
            ),
        )
        return [cattrs.structure(item, UserRateFull) for item in resp]

    async def favourites(self, user_id: int) -> Favourites:
        resp = await self._request(f"/api/users/{user_id}/favourites")
        return cattrs.structure(resp, Favourites)

    async def my_messages(
        self,
        user_id: int,
        type: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Message]:
        resp = await self._request(
            f"/api/users/{user_id}/messages",
            params=prepare_params(type=type, page=page, limit=limit),
        )
        return [cattrs.structure(item, Message) for item in resp]

    async def my_unread_messages(self, user_id: int) -> UnreadMessages:
        resp = await self._request(f"/api/users/{user_id}/unread_messages")
        return cattrs.structure(resp, UnreadMessages)

    async def history(
        self,
        user_id: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        target_id: Optional[int] = None,
        target_type: Optional[str] = None,
    ) -> List[UserHistory]:
        resp = await self._request(
            f"/api/users/{user_id}/history",
            params=prepare_params(
                page=page, limit=limit, target_id=target_id, target_type=target_type
            ),
        )
        return [cattrs.structure(item, UserHistory) for item in resp]

    async def bans(self, user_id: int) -> List[Ban]:
        resp = await self._request(f"/api/users/{user_id}/bans")
        return [cattrs.structure(item, Ban) for item in resp]
