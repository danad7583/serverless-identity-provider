from internal_oidc.core.errors import ValidationError
from internal_oidc.core.services.revocation_service import RevocationService
from internal_oidc.security.claims.validator import ClaimsValidator
from internal_oidc.security.crypto.service import CryptoService


class LambdaJWTAuthorizer:
    """Thin AWS adapter.

    The security model is still platform-neutral:
    - verify JWT
    - require jti
    - always check revocation
    """

    def __init__(
        self,
        crypto_service: CryptoService,
        claims_validator: ClaimsValidator,
        revocation_service: RevocationService,
    ) -> None:
        self._crypto = crypto_service
        self._claims = claims_validator
        self._revocation = revocation_service

    def authorize(self, token: str) -> dict:
        if not token:
            raise ValidationError("Missing bearer token")
        claims_dict = self._crypto.verify_jwt(token)
        claims = self._claims.validate_required_claims(claims_dict)
        self._revocation.assert_not_revoked(claims)
        return {
            "principalId": claims.sub,
            "context": {
                "sub": claims.sub,
                "jti": claims.jti,
                "client_id": claims.client_id or "",
            },
        }
