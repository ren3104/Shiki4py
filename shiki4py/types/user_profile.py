from datetime import datetime
from typing import List, Optional

from attrs import define, field

from shiki4py.types.user import User


@define
class UserProfile(User):
    name: Optional[str]
    sex: Optional[str]
    full_years: Optional[int]
    last_online: str
    last_online_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    website: Optional[str]
    location: Optional[str]
    banned: bool
    about: str
    about_html: str
    common_info: List[str]
    show_comments: bool
    in_friends: bool
    is_ignored: bool
    stats: dict
    style_id: int
