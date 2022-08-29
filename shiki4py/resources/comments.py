from shiki4py.base import Client
from shiki4py.types.comment import Comment
from typing import Optional, List
from aiohttp import hdrs
from pyrate_limiter import Limiter, RequestRate


class Comments:
    _comments_limiter = Limiter(RequestRate(1, 3))

    def __init__(self, client: Client) -> None:
        self._client = client
    
    async def show_one(self, comment_id: int) -> Comment:
        resp = await self._client.request(f"/api/comments/{comment_id}")
        return Comment(**resp)

    async def show_part(
        self,
        commentable_id: int,
        commentable_type: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        desc: Optional[int] = None
    ) -> List[Comment]:
        resp = await self._client.request("/api/comments", params={
            "commentable_id": commentable_id,
            "commentable_type": commentable_type,
            "page": page,
            "limit": limit,
            "desc": desc
        })
        return [Comment(**item) for item in resp]
    
    @_comments_limiter.ratelimit("comments_shikimori", delay=True)
    async def create(
        self,
        body: str,
        commentable_id: int,
        commentable_type: str,
        is_offtopic: Optional[bool] = None,
        broadcast: Optional[bool] = None,
    ) -> Comment:
        resp = await self._client.request("", hdrs.METH_POST, json={
            "comment": {
                "body": body,
                "commentable_id": commentable_id,
                "commentable_type": commentable_type,
                "is_offtopic": is_offtopic
            },
            "broadcast": broadcast
        })
        return Comment(**resp)
    
    async def update(self, comment_id: int, body: str) -> Comment:
        resp = await self._client.request(f"/api/comments/{comment_id}", hdrs.METH_PATCH, json={
            "comment": {
                "body": body
            }
        })
        return Comment(**resp)
    
    async def delete(self, comment_id: int) -> None:
        resp = await self._client.request(f"/api/comments/{comment_id}", hdrs.METH_DELETE)
        print(resp)
