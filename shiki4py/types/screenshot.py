from attrs import define


@define
class Screenshot:
    original: str
    preview: str