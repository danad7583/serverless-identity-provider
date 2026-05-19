from dataclasses import dataclass
import os

from internal_oidc.core.errors import ConfigurationError


@dataclass(frozen=True)
class OIDCConfig:
    issuer: str
    audience: str
    jwks_cache_ttl_seconds: int = 300
    revocation_namespace: str = "revoke:jti"
    strict_fail_closed_on_revocation_error: bool = True

    @classmethod
    def from_env(cls) -> "OIDCConfig":
        issuer = os.getenv("OIDC_ISSUER")
        audience = os.getenv("OIDC_AUDIENCE")
        if not issuer or not audience:
            raise ConfigurationError("OIDC_ISSUER and OIDC_AUDIENCE are required")
        return cls(
            issuer=issuer,
            audience=audience,
            jwks_cache_ttl_seconds=int(os.getenv("JWKS_CACHE_TTL_SECONDS", "300")),
            revocation_namespace=os.getenv("REVOCATION_NAMESPACE", "revoke:jti"),
            strict_fail_closed_on_revocation_error=os.getenv(
                "STRICT_FAIL_CLOSED_ON_REVOCATION_ERROR", "true"
            ).lower() == "true",
        )
