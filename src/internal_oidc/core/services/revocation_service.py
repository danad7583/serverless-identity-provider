from internal_oidc.core.errors import RevokedTokenError, ValidationError
from internal_oidc.core.interfaces.audit_logger import AuditLogger
from internal_oidc.core.interfaces.revocation_store import RevocationStore
from internal_oidc.core.models.token import TokenClaims


class RevocationService:
    """Central revocation service keyed by JTI.

    Rules:
    - every token must contain a JTI
    - revocation is a denylist lookup by JTI
    - no fallback path if JTI is missing
    """

    def __init__(self, store: RevocationStore, audit_logger: AuditLogger | None = None) -> None:
        self._store = store
        self._audit = audit_logger

    def revoke(self, claims: TokenClaims, reason: str = "manual") -> None:
        if not claims.jti:
            raise ValidationError("Cannot revoke a token without jti")
        self._store.revoke(claims.jti, claims.exp)
        if self._audit:
            self._audit.log(
                "token_revoked",
                {"jti": claims.jti, "sub": claims.sub, "exp": claims.exp, "reason": reason},
            )

    def assert_not_revoked(self, claims: TokenClaims) -> None:
        if not claims.jti:
            raise ValidationError("Token is missing required jti")
        if self._store.is_revoked(claims.jti):
            raise RevokedTokenError(f"Token jti {claims.jti} has been revoked")
