from typing import List, Optional

from shiki4py.resources.base_resource import BaseResource
from shiki4py.types.ban import Ban
from shiki4py.types.club import Club
from shiki4py.types.favourites import Favourites
from shiki4py.types.message import Message
from shiki4py.types.unread_messages import UnreadMessages
from shiki4py.types.user import User
from shiki4py.types.user_history import UserHistory
from shiki4py.types.user_info import UserInfo
from shiki4py.types.user_profile import UserProfile
from shiki4py.types.user_rate_full import UserRateFull
from shiki4py.utils import prepare_params


class Users(BaseResource):
    async def show_one(self, user_id: int) -> UserProfile:
        resp = await self._client.request(f"/api/users/{user_id}")
        return UserProfile(**resp)

    async def show_part(
        self, page: Optional[int] = None, limit: Optional[int] = None
    ) -> List[UserProfile]:
        resp = await self._client.request(
            "/api/users", params=prepare_params(page=page, limit=limit)
        )
        return [UserProfile(**item) for item in resp]

    async def info(self, user_id: int) -> UserInfo:
        resp = await self._client.request(f"/api/users/{user_id}/info")
        return UserInfo(**resp)

    async def my_info(self) -> UserInfo:
        resp = await self._client.request("/api/users/whoami")
        return UserInfo(**resp)

    async def sign_out(self) -> bool:
        resp = await self._client.request("/api/users/sign_out")
        if resp == "signed out":
            return True
        return False

    async def friends(self, user_id: int) -> List[User]:
        resp = await self._client.request(f"/api/users/{user_id}/friends")
        return [User(**item) for item in resp]

    async def clubs(self, user_id: int) -> List[Club]:
        resp = await self._client.request(f"/api/users/{user_id}/clubs")
        return [Club(**item) for item in resp]

    async def anime_rates(
        self,
        user_id: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        status: Optional[str] = None,
        censored: Optional[bool] = None,
    ) -> List[UserRateFull]:
        resp = await self._client.request(
            f"/api/users/{user_id}/anime_rates",
            params=prepare_params(
                page=page, limit=limit, status=status, censored=censored
            ),
        )
        return [UserRateFull(**item) for item in resp]

    async def manga_rates(
        self,
        user_id: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        status: Optional[str] = None,
        censored: Optional[bool] = None,
    ) -> List[UserRateFull]:
        resp = await self._client.request(
            f"/api/users/{user_id}/manga_rates",
            params=prepare_params(
                page=page, limit=limit, status=status, censored=censored
            ),
        )
        return [UserRateFull(**item) for item in resp]

    async def favourites(self, user_id: int) -> Favourites:
        resp = await self._client.request(f"/api/users/{user_id}/favourites")
        return Favourites(**resp)

    async def my_messages(
        self,
        user_id: int,
        type: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Message]:
        resp = await self._client.request(
            f"/api/users/{user_id}/messages",
            params=prepare_params(type=type, page=page, limit=limit),
        )
        return [Message(**item) for item in resp]

    async def my_unread_messages(self, user_id: int) -> UnreadMessages:
        resp = await self._client.request(f"/api/users/{user_id}/unread_messages")
        return UnreadMessages(**resp)

    async def history(
        self,
        user_id: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        target_id: Optional[int] = None,
        target_type: Optional[str] = None,
    ) -> List[UserHistory]:
        resp = await self._client.request(
            f"/api/users/{user_id}/history",
            params=prepare_params(
                page=page, limit=limit, target_id=target_id, target_type=target_type
            ),
        )
        return [UserHistory(**item) for item in resp]

    async def bans(self, user_id: int) -> List[Ban]:
        resp = await self._client.request(f"/api/users/{user_id}/bans")
        return [Ban(**item) for item in resp]
