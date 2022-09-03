from datetime import datetime
from typing import Optional, Union

from attrs import define, field
from cattr.gen import make_dict_structure_fn, override
from cattrs import global_converter

from shiki4py.types.anime import Anime
from shiki4py.types.linked_topic import LinkedTopic
from shiki4py.types.manga import Manga
from shiki4py.types.user import User


@define
class Message:
    id: int
    kind: str
    read: bool
    body: str
    html_body: str
    created_at: datetime = field(repr=str)
    linked_id: int
    linked_type: Optional[str]
    linked: Optional[Union[Anime, Manga, LinkedTopic]]
    from_user: User
    to_user: User


global_converter.register_structure_hook(
    Message,
    make_dict_structure_fn(
        Message,
        global_converter,
        from_user=override(rename="from"),
        to_user=override(rename="to"),
    ),
)
