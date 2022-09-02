from datetime import date, datetime
from typing import Optional

from attrs import define, field
from attrs.converters import optional


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
    image: Image = field(converter=lambda d: Image(**d))
    url: str
    kind: str
    score: float = field(converter=float)
    status: str
    volumes: int
    chapters: int
    aired_on: Optional[date] = field(
        converter=optional(lambda s: datetime.strptime(s, "%Y-%m-%d").date()), repr=str
    )
    released_on: Optional[date] = field(
        converter=optional(lambda s: datetime.strptime(s, "%Y-%m-%d").date()), repr=str
    )
