from typing import Optional

from attrs import define

from shiki4py.types.anime import Anime
from shiki4py.types.manga import Manga


@define
class Relation:
    relation: str
    relation_russian: str
    anime: Optional[Anime]
    manga: Optional[Manga]
