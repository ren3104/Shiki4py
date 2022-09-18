from typing import List, Optional, Union
from cattrs import structure
from shiki4py.resources.base_resource import BaseResource
from shiki4py.types import Anime, AnimeProfile
from shiki4py.utils import prepare_params


class Animes(BaseResource):
    async def show_one(self, anime_id: int) -> AnimeProfile:
        resp = await self._client.request(f"/api/animes/{anime_id}")
        return structure(resp, AnimeProfile)

    async def show_part(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        order: Optional[str] = None,
        kind: Optional[Union[str, List[str]]] = None,
        status: Optional[Union[str, List[str]]] = None,
        season: Optional[Union[str, List[str]]] = None,
        score: Optional[int] = None,
        duration: Optional[Union[str, List[str]]] = None,
        rating: Optional[Union[str, List[str]]] = None,
        genre: Optional[Union[int, List[int]]] = None,
        studio: Optional[Union[int, List[int]]] = None,
        franchise: Optional[Union[int, List[int]]] = None,
        censored: Optional[bool] = None,
        mylist: Optional[Union[str, List[str]]] = None,
        ids: Optional[Union[int, List[int]]] = None,
        exclude_ids: Optional[Union[int, List[int]]] = None,
        search: Optional[str] = None,
    ) -> List[Anime]:
        resp = await self._client.request(
            "/api/animes",
            params=prepare_params(
                page=page,
                limit=limit,
                order=order,
                kind=kind,
                status=status,
                season=season,
                score=score,
                duration=duration,
                rating=rating,
                genre=genre,
                studio=studio,
                franchise=franchise,
                censored=censored,
                mylist=mylist,
                ids=ids,
                exclude_ids=exclude_ids,
                search=search,
            ),
        )
        return [structure(item, Anime) for item in resp]

    # async def roles(self) -> None:
    #     resp = await self._client.request("")

    # async def similar(self) -> None:
    #     resp = await self._client.request("")

    # async def related(self) -> None:
    #     resp = await self._client.request("")

    # async def screenshots(self) -> None:
    #     resp = await self._client.request("")

    # async def videos(self) -> None:
    #     resp = await self._client.request("")

    # async def franchise(self) -> None:
    #     resp = await self._client.request("")

    # async def external_links(self) -> None:
    #     resp = await self._client.request("")

    # async def search(self) -> None:
    #     resp = await self._client.request("")

    # async def topics(self) -> None:
    #     resp = await self._client.request("")
