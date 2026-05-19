from abc import ABC, abstractmethod
from typing import Any


class KeyProvider(ABC):
    """Abstraction for loading signing and verification key material."""

    @abstractmethod
    def get_signing_key(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_public_jwks(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_active_kid(self) -> str:
        raise NotImplementedError
