from datetime import date, datetime

from cattrs import global_converter

from shiki4py.base import Client

global_converter.register_structure_hook(
    datetime, lambda v, _: datetime.fromisoformat(v)
)
global_converter.register_structure_hook(
    date, lambda v, _: datetime.strptime(v, "%Y-%m-%d").date()
)


class BaseResource:
    def __init__(self, client: Client) -> None:
        self._client = client
