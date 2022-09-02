from datetime import datetime
from typing import Any, Dict, Optional, Union

from attrs import define, field
from attrs.converters import optional

from shiki4py.types.anime import Anime
from shiki4py.types.manga import Manga


def history_target(target: Dict[str, Any]) -> Union[Anime, Manga]:
    try:
        return Anime(**target)
    except TypeError:
        return Manga(**target)


@define
class UserHistory:
    id: int
    created_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    description: str
    target: Optional[Union[Anime, Manga]] = field(converter=optional(history_target))
