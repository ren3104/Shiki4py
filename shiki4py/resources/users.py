from shiki4py.resources.base_resource import BaseResource
from shiki4py.types.user import User
from shiki4py.types.user_info import UserInfo
from shiki4py.types.user_profile import UserProfile
from shiki4py.types.club import Club
from shiki4py.utils import prepare_params
from typing import Optional, List


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

    # TODO
    # async def anime_rates(self, user_id: int) -> None:
    #     resp = await self._client.request(f"/api/users/{user_id}/anime_rates")

    # async def manga_rates(self) -> None:
    #     resp = await self._client.request()

    # async def favourites(self) -> None:
    #     resp = await self._client.request()

    # async def my_messages(self) -> None:
    #     resp = await self._client.request()

    # async def my_unread_messages(self) -> None:
    #     resp = await self._client.request()

    # async def history(self) -> None:
    #     resp = await self._client.request()

    # async def bans(self) -> None:
    #     resp = await self._client.request()
