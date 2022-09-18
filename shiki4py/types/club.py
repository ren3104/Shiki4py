from attrs import define


@define
class ClubAvatar:
    original: str
    main: str
    x96: str
    x73: str
    x48: str


@define
class Club:
    id: int
    name: str
    logo: ClubAvatar
    is_censored: bool
    join_policy: str
    comment_policy: str
