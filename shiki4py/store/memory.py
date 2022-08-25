from typing import Any, Dict, Optional

from shiki4py.store import BaseTokenStore


class MemoryTokenStore(BaseTokenStore):
    def __init__(self) -> None:
        self._data = {}

    def save(self, client_id: str, token: Dict[str, Any]) -> None:
        self._data[client_id] = token

    def fetch(self, client_id: str) -> Optional[Dict[str, Any]]:
        return self._data.get(client_id)
