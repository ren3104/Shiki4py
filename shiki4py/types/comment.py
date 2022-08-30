from shiki4py.types.user import User
from attrs import define, field
from datetime import datetime


@define
class Comment:
    id: int
    user_id: int
    commentable_id: int
    commentable_type: str
    body: str
    html_body: str
    created_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    updated_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    is_offtopic: bool
    is_summary: bool
    can_be_edited: bool
    user: User = field(converter=lambda d: User(**d))
