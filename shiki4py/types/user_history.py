from datetime import datetime
from typing import Optional, Union

from attrs import define, field

from shiki4py.types.anime import Anime
from shiki4py.types.manga import Manga


@define
class UserHistory:
    id: int
    created_at: datetime = field(repr=str)
    description: str
    target: Optional[Union[Anime, Manga]]
