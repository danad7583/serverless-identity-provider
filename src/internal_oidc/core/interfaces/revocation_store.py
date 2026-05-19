from abc import ABC, abstractmethod


class RevocationStore(ABC):
    """Store revoked token identifiers using `jti` with TTL support."""

    @abstractmethod
    def revoke(self, jti: str, expires_at_epoch: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_revoked(self, jti: str) -> bool:
        raise NotImplementedError
