from shiki4py.store import BaseTokenStore
from typing import Any, Dict, Optional
import configparser
import sys
import os.path


class IniTokenStore(BaseTokenStore):
    def __init__(self) -> None:
        self._file_path = f"{os.path.splitext(sys.argv[0])[0]}.shiki4py.ini"
        self._config = configparser.ConfigParser()

        if os.path.isfile(self._file_path):
            self._config.read(self._file_path)

    def save(self, client_id: str, token: Dict[str, Any]) -> None:
        self._config.update({client_id: token})
        self._config.write(open(self._file_path, 'w'))

    def fetch(self, client_id: str) -> Optional[Dict[str, Any]]:
        if self._config.has_section(client_id):
            return dict(self._config.items(client_id))
        return None
