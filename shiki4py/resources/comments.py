from typing import List, Optional

import cattrs
from aiohttp import hdrs
from pyrate_limiter import Limiter, RequestRate

from shiki4py.resources.base_resource import BaseResource
from shiki4py.types import Comment
from shiki4py.utils import prepare_json, prepare_params


class Comments(BaseResource):
    _comments_limiter = Limiter(RequestRate(1, 3))

    async def show_one(self, comment_id: int) -> Comment:
        resp = await self._client.request(f"/api/comments/{comment_id}")
        return cattrs.structure(resp, Comment)

    async def show_part(
        self,
        commentable_id: int,
        commentable_type: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        desc: Optional[int] = None,
    ) -> List[Comment]:
        resp = await self._client.request(
            "/api/comments",
            params=prepare_params(
                commentable_id=commentable_id,
                commentable_type=commentable_type,
                page=page,
                limit=limit,
                desc=desc,
            ),
        )
        return [cattrs.structure(resp, Comment) for item in resp]

    @_comments_limiter.ratelimit("comments_shikimori", delay=True)
    async def create(
        self,
        body: str,
        commentable_id: int,
        commentable_type: str,
        is_offtopic: Optional[bool] = None,
        broadcast: Optional[bool] = None,
    ) -> Comment:
        resp = await self._client.request(
            "/api/comments",
            hdrs.METH_POST,
            json=prepare_json(
                {
                    "comment": {
                        "body": body,
                        "commentable_id": commentable_id,
                        "commentable_type": commentable_type,
                        "is_offtopic": is_offtopic,
                    },
                    "broadcast": broadcast,
                }
            ),
        )
        return cattrs.structure(resp, Comment)

    async def update(self, comment_id: int, body: str) -> Comment:
        resp = await self._client.request(
            f"/api/comments/{comment_id}",
            hdrs.METH_PATCH,
            json=prepare_json({"comment": {"body": body}}),
        )
        return cattrs.structure(resp, Comment)

    async def delete(self, comment_id: int) -> bool:
        resp = await self._client.request(
            f"/api/comments/{comment_id}", hdrs.METH_DELETE
        )
        if "notice" in resp:
            return True
        return False
