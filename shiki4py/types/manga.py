from datetime import date
from typing import Optional

from attrs import define, field


@define
class Image:
    original: str
    preview: str
    x96: str
    x48: str


@define
class Manga:
    id: int
    name: str
    russian: str
    image: Image
    url: str
    kind: str
    score: float
    status: str
    volumes: int
    chapters: int
    aired_on: Optional[date] = field(repr=str)
    released_on: Optional[date] = field(repr=str)
