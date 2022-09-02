from attrs import define


@define
class LinkedTopic:
    id: int
    type: str
    topic_url: str
    thread_id: int
    topic_id: int
