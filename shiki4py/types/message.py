from datetime import datetime
from typing import Any, Dict, Optional, Union

from attrs import define, field
from attrs.converters import optional

from shiki4py.types.anime import Anime
from shiki4py.types.linked_topic import LinkedTopic
from shiki4py.types.user import User


def message_linked(linked: Dict[str, Any]) -> Union[Anime, LinkedTopic]:
    try:
        return Anime(**linked)
    except TypeError:
        return LinkedTopic(**linked)


@define
class Message:
    id: int
    kind: str
    read: bool
    body: str
    html_body: str
    created_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    linked_id: int
    linked_type: Optional[str]
    linked: Optional[Union[Anime, LinkedTopic]] = field(
        converter=optional(message_linked)
    )
    from_user: User = field(converter=lambda d: User(**d))
    to_user: User = field(converter=lambda d: User(**d))

    def __init__(self, **kwargs):
        kwargs["from_user"] = kwargs.pop("from")
        kwargs["to_user"] = kwargs.pop("to")
        self.__attrs_init__(**kwargs)
