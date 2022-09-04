from datetime import datetime
from typing import Optional

from attrs import define, field

from shiki4py.types.anime import Anime
from shiki4py.types.manga import Manga
from shiki4py.types.user import User


@define
class UserRateFull:
    id: int
    score: int
    status: str
    text: Optional[str]
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    text_html: Optional[str]
    rewatches: int
    created_at: datetime = field(repr=str)
    updated_at: datetime = field(repr=str)
    user: Optional[User]
    anime: Optional[Anime]
    manga: Optional[Manga]
