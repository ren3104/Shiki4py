from shiki4py.types.club_image import ClubImage
from attrs import define, field


@define
class Club:
    id: int
    name: str
    logo: dict = field(converter=lambda d: ClubImage(**d))
    is_censored: bool
    join_policy: str
    comment_policy: str
