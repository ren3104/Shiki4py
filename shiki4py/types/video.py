from typing import Optional

from attrs import define


@define
class Video:
    id: int
    url: str
    image_url: str
    player_url: str
    name: Optional[str]
    kind: str
    hosting: str
