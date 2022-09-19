from typing import List, Optional, Union

from cattrs import structure

from shiki4py.resources.base_resource import BaseResource
from shiki4py.types import (
    Anime,
    AnimeProfile,
    ExternalLink,
    Franchise,
    PersonRole,
    Relation,
    Screenshot,
    Topic,
    Video,
)
from shiki4py.utils import prepare_params


class Animes(BaseResource):
    async def show_one(self, anime_id: int) -> AnimeProfile:
        resp = await self._request(f"/api/animes/{anime_id}")
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
        resp = await self._request(
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

    async def roles(self, anime_id: int) -> List[PersonRole]:
        resp = await self._request(f"/api/animes/{anime_id}/roles")
        return [structure(item, PersonRole) for item in resp]

    async def similar(self, anime_id: int) -> List[Anime]:
        resp = await self._request(f"/api/animes/{anime_id}/similar")
        return [structure(item, Anime) for item in resp]

    async def related(self, anime_id: int) -> List[Relation]:
        resp = await self._request(f"/api/animes/{anime_id}/related")
        return [structure(item, Relation) for item in resp]

    async def screenshots(self, anime_id: int) -> List[Screenshot]:
        resp = await self._request(f"/api/animes/{anime_id}/screenshots")
        return [structure(item, Screenshot) for item in resp]

    async def videos(self, anime_id: int) -> List[Video]:
        resp = await self._request(f"/api/animes/{anime_id}/videos")
        return [structure(item, Video) for item in resp]

    async def franchise(self, anime_id: int) -> Franchise:
        resp = await self._request(f"/api/animes/{anime_id}/franchise")
        return structure(resp, Franchise)

    async def external_links(self, anime_id: int) -> List[ExternalLink]:
        resp = await self._request(f"/api/animes/{anime_id}/external_links")
        return [structure(item, ExternalLink) for item in resp]

    async def topics(self, anime_id: int) -> List[Topic]:
        resp = await self._request(f"/api/animes/{anime_id}/topics")
        return [structure(item, Topic) for item in resp]
