from datetime import datetime

from attrs import define, field

from shiki4py.types.user import User


@define
class Comment:
    id: int
    user_id: int
    commentable_id: int
    commentable_type: str
    body: str
    html_body: str
    created_at: datetime = field(repr=str)
    updated_at: datetime = field(repr=str)
    is_offtopic: bool
    is_summary: bool
    can_be_edited: bool
    user: User
