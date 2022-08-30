from shiki4py.types.user_image import UserImage
from attrs import define, field
from datetime import datetime


@define
class User:
    id :int
    nickname: str
    avatar: str
    image: UserImage = field(converter=lambda d: UserImage(**d))
    last_online_at: datetime = field(converter=datetime.fromisoformat, repr=str)
    url: str
