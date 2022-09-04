from datetime import datetime
from typing import Optional

from attrs import define, field

from shiki4py.types.user import User


@define
class UserInfo(User):
    name: Optional[str]
    sex: Optional[str]
    website: Optional[str]
    birth_on: Optional[datetime] = field(repr=str)
    full_years: Optional[int]
    locale: str
