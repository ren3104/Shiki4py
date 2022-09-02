from attrs import define, field


@define
class Image:
    original: str
    main: str
    x96: str
    x73: str
    x48: str


@define
class Club:
    id: int
    name: str
    logo: Image = field(converter=lambda d: Image(**d))
    is_censored: bool
    join_policy: str
    comment_policy: str
