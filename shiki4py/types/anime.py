from datetime import date
from typing import Optional

from attrs import define, field


@define
class AnimeAvatar:
    original: str
    preview: str
    x96: str
    x48: str


@define
class Anime:
    id: int
    name: str
    russian: str
    image: AnimeAvatar
    url: str
    kind: Optional[str]
    score: float
    status: str
    episodes: int
    episodes_aired: int
    aired_on: Optional[date] = field(repr=str)
    released_on: Optional[date] = field(repr=str)
