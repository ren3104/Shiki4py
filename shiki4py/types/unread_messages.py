from attrs import define


@define
class UnreadMessages:
    messages: int
    news: int
    notifications: int
