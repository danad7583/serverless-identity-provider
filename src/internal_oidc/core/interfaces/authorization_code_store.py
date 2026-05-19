from abc import ABC, abstractmethod
from typing import Any


class AuthorizationCodeStore(ABC):
    @abstractmethod
    def create_code(self, code: str, payload: dict[str, Any], expires_at_epoch: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def consume_code(self, code: str) -> dict[str, Any] | None:
        raise NotImplementedError
