from attrs import define
from typing import List


@define
class Link:
    id: int
    source_id: int
    target_id: int
    source: int
    target: int
    weight: int
    relation: str


@define
class Node:
    id: int
    date: int
    name: str
    image_url: str
    url: str
    year: int
    kind: str
    weight: int


@define
class Franchise:
    links: List[Link]
    nodes: List[Node]
    current_id: int
