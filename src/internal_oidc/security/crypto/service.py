from typing import Any

import jwt

from internal_oidc.core.config import OIDCConfig
from internal_oidc.core.interfaces.key_provider import KeyProvider


class CryptoService:
    """JWT signing and verification boundary.

    Keep platform-specific key retrieval out of this class.
    """

    def __init__(self, config: OIDCConfig, key_provider: KeyProvider) -> None:
        self._config = config
        self._key_provider = key_provider

    def sign_jwt(self, claims: dict[str, Any], algorithm: str = "RS256") -> str:
        headers = {"kid": self._key_provider.get_active_kid()}
        signing_key = self._key_provider.get_signing_key()
        return jwt.encode(claims, signing_key, algorithm=algorithm, headers=headers)

    def verify_jwt(self, token: str, algorithms: list[str] | None = None) -> dict[str, Any]:
        jwks = self._key_provider.get_public_jwks()
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        key = self._select_jwk(jwks, kid)
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        return jwt.decode(
            token,
            key=public_key,
            algorithms=algorithms or [key.get("alg", "RS256")],
            issuer=self._config.issuer,
            audience=self._config.audience,
            options={"require": ["exp", "iat", "iss", "aud", "jti"]},
        )

    @staticmethod
    def _select_jwk(jwks: dict[str, Any], kid: str | None) -> str:
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return __import__("json").dumps(key)
        raise ValueError("No matching JWK found for token kid")
