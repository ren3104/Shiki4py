from datetime import datetime
from typing import Optional

from attrs import define, field
from attrs.converters import optional

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
    created_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    updated_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    user: Optional[User] = field(converter=optional(lambda d: User(**d)))
    anime: Optional[Anime] = field(converter=optional(lambda d: Anime(**d)))
    manga: Optional[Manga] = field(converter=optional(lambda d: Manga(**d)))
