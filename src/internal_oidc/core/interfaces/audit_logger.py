from abc import ABC, abstractmethod
from typing import Any


class AuditLogger(ABC):
    @abstractmethod
    def log(self, event_type: str, details: dict[str, Any]) -> None:
        raise NotImplementedError
