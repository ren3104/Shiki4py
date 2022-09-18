from attrs import define, field
from typing import Optional
from datetime import datetime


@define
class ExternalLink:
    id: Optional[int]
    kind: str
    url: str
    source: str
    entry_id: int
    entry_type: str
    created_at: Optional[datetime] = field(repr=str)
    updated_at: Optional[datetime] = field(repr=str)
    imported_at: Optional[datetime] = field(repr=str)