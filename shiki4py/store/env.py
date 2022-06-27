from shiki4py.store import BaseTokenStore
from typing import Any, Dict, Optional
from json import dumps, loads
from dotenv import find_dotenv, set_key
from dotenv.main import DotEnv


class EnvTokenStore(BaseTokenStore):
    def __init__(self, file_path: str = '.env') -> None:
        self._dotenv_file = find_dotenv(file_path)
        if len(self._dotenv_file) == 0:
            self._dotenv_file = file_path

    def save(self, client_id: str, token: Dict[str, Any]) -> None:
        return set_key(self._dotenv_file,
                       client_id,
                       dumps(token))

    def fetch(self, client_id: str) -> Optional[Dict[str, Any]]:
        token = DotEnv(self._dotenv_file,
                       encoding='utf-8').get(client_id)
        if token is not None:
            return loads(token)
        return None
