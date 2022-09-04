from typing import Optional

from attrs import define


@define
class Favourite:
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]
