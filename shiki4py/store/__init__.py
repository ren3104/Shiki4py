from typing import Any, Dict, Optional


class BaseTokenStore:
    def save(self, client_id: str, token: Dict[str, Any]) -> None:
        raise NotImplementedError

    def fetch(self, client_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
