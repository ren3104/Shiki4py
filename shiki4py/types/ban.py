from datetime import datetime
from typing import Optional

from attrs import define, field

from shiki4py.types.user import User


@define
class Comment:
    id: int
    commentable_id: int
    commentable_type: str
    body: str
    user_id: int
    created_at: datetime = field(repr=str)
    updated_at: datetime = field(repr=str)
    is_offtopic: bool


@define
class Ban:
    id: int
    user_id: int
    comment: Optional[Comment]
    moderator_id: int
    reason: str
    created_at: datetime = field(repr=str)
    duration_minutes: int
    user: User
    moderator: User
