from internal_oidc.core.config import OIDCConfig
from internal_oidc.core.errors import ValidationError
from internal_oidc.core.models.token import TokenClaims


class ClaimsValidator:
    """Claim validation policy.

    This intentionally requires `jti` on every token so revocation is always supported.
    """

    def __init__(self, config: OIDCConfig) -> None:
        self._config = config

    def validate_required_claims(self, claims: dict) -> TokenClaims:
        required = ["iss", "sub", "aud", "exp", "iat", "jti"]
        missing = [name for name in required if name not in claims or claims[name] in (None, "")]
        if missing:
            raise ValidationError(f"Missing required claims: {', '.join(missing)}")

        if claims["iss"] != self._config.issuer:
            raise ValidationError("Issuer mismatch")

        aud = claims["aud"]
        if isinstance(aud, list):
            if self._config.audience not in aud:
                raise ValidationError("Audience mismatch")
        elif aud != self._config.audience:
            raise ValidationError("Audience mismatch")

        return TokenClaims(
            iss=claims["iss"],
            sub=claims["sub"],
            aud=claims["aud"],
            exp=int(claims["exp"]),
            iat=int(claims["iat"]),
            jti=claims["jti"],
            token_use=claims.get("token_use"),
            client_id=claims.get("client_id"),
            scope=claims.get("scope"),
            raw_claims=claims,
        )
