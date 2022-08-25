from json import dumps, loads
from typing import Any, Dict, Optional

from dotenv import find_dotenv, set_key
from dotenv.main import DotEnv

from shiki4py.store.memory import MemoryTokenStore


class EnvTokenStore:
    def __init__(self, file_path: str = ".env") -> None:
        self._memory_token_store = MemoryTokenStore()

        self._dotenv_file = find_dotenv(file_path)
        if len(self._dotenv_file) == 0:
            self._dotenv_file = file_path

    def save(self, client_id: str, token: Dict[str, Any]) -> None:
        self._memory_token_store.save(client_id, token)
        set_key(self._dotenv_file, client_id, dumps(token))

    def fetch(self, client_id: str) -> Optional[Dict[str, Any]]:
        memory_token = self._memory_token_store.fetch(client_id)
        if memory_token:
            return memory_token

        token = DotEnv(self._dotenv_file, encoding="utf-8").get(client_id)
        if token:
            token = loads(token)
            self._memory_token_store.save(client_id, token)
            return token
