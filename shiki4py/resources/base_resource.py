from shiki4py.base import Client


class BaseResource:
    def __init__(self, client: Client) -> None:
        self._client = client
