from typing import List, Optional

from attrs import define


@define
class PersonRole:
    roles: List[str]
    roles_russian: List[str]
    character: Optional[dict]
    person: Optional[dict]
