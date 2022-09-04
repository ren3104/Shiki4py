from datetime import datetime

from attrs import define, field


@define
class Image:
    x160: str
    x148: str
    x80: str
    x64: str
    x48: str
    x32: str
    x16: str


@define
class User:
    id: int
    nickname: str
    avatar: str
    image: Image
    last_online_at: datetime = field(repr=str)
    url: str
