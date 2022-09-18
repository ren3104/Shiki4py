from datetime import datetime
from typing import Union

from attrs import define, field

from shiki4py.types.anime import Anime
from shiki4py.types.manga import Manga
from shiki4py.types.user import User


@define
class Topic:
    id: int
    topic_title: str
    body: str
    html_body: str
    html_footer: str
    created_at: datetime = field(repr=str)
    comments_count: int
    forum: dict
    user: User
    type: str
    linked_id: int
    linked_type: str
    linked: Union[Anime, Manga]
    viewed: bool
    last_comment_viewed: bool
    event: str
    episode: int
