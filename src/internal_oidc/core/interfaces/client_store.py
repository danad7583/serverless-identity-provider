from abc import ABC, abstractmethod
from typing import Any


class ClientStore(ABC):
    @abstractmethod
    def get_client(self, client_id: str) -> dict[str, Any] | None:
        raise NotImplementedError
