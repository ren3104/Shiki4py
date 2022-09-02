from datetime import datetime
from typing import Optional

from attrs import define, field
from attrs.converters import optional

from shiki4py.types.user import User


@define
class Comment:
    id: int
    commentable_id: int
    commentable_type: str
    body: str
    user_id: int
    created_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    updated_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    is_offtopic: bool


@define
class Ban:
    id: int
    user_id: int
    comment: Optional[Comment] = field(converter=optional(lambda d: Comment(**d)))
    moderator_id: int
    reason: str
    created_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    duration_minutes: int
    user: User = field(converter=lambda d: User(**d))
    moderator: User = field(converter=lambda d: User(**d))
