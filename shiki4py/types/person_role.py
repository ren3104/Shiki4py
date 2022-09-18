from attrs import define
from typing import List, Optional


@define
class PersonRole:
    roles: List[str]
    roles_russian: List[str]
    character: Optional[dict]
    person: Optional[dict]