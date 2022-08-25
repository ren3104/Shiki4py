from typing import Any, Dict

from aiohttp import hdrs
from pyrate_limiter import Limiter, RequestRate

from shiki4py.base import Client


class Shikimori(Client):
    _comments_limiter = Limiter(RequestRate(1, 4))

    @_comments_limiter.ratelimit("comments_shikimori", delay=True)
    def create_comment(
        self,
        body: str,
        commentable_id: int,
        commentable_type: str,
        is_offtopic: bool = False,
        broadcast: bool = False,
    ) -> Dict[str, Any]:
        return self.request(
            "/api/comments",
            hdrs.METH_POST,
            json={
                "comment": {
                    "body": body,
                    "commentable_id": commentable_id,
                    "commentable_type": commentable_type,
                    "is_offtopic": is_offtopic,
                },
                "broadcast": broadcast,
            },
        )
