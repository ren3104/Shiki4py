from attrs import define
from typing import Optional


@define
class Video:
    id: int
    url: str
    image_url: str
    player_url: str
    name: Optional[str]
    kind: str
    hosting: str