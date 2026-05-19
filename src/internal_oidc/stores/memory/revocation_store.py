import time

from internal_oidc.core.interfaces.revocation_store import RevocationStore


class MemoryRevocationStore(RevocationStore):
    """Simple local store for testing and development only."""

    def __init__(self) -> None:
        self._entries: dict[str, int] = {}

    def revoke(self, jti: str, expires_at_epoch: int) -> None:
        self._entries[jti] = expires_at_epoch

    def is_revoked(self, jti: str) -> bool:
        exp = self._entries.get(jti)
        if exp is None:
            return False
        if exp <= int(time.time()):
            self._entries.pop(jti, None)
            return False
        return True
