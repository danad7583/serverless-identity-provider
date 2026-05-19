from internal_oidc.core.errors import AuthenticationError, ValidationError
from internal_oidc.core.services.revocation_service import RevocationService
from internal_oidc.security.claims.validator import ClaimsValidator
from internal_oidc.security.crypto.service import CryptoService


class RevokeHandler:
    """Developer-ready revocation flow boundary.

    Expected flow:
    1. authenticate caller using admin/client trust model
    2. verify token to revoke using trusted key material
    3. require jti
    4. write jti to revocation store with TTL = exp
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

    def handle(self, event: dict) -> dict:
        token = self._extract_token_from_body(event)
        self._assert_authenticated_revocation_caller(event)
        claims_dict = self._crypto.verify_jwt(token)
        claims = self._claims.validate_required_claims(claims_dict)
        self._revocation.revoke(claims)
        return {"statusCode": 200, "body": '{"revoked":true}'}

    @staticmethod
    def _extract_token_from_body(event: dict) -> str:
        body = event.get("json") or {}
        token = body.get("token")
        if not token:
            raise ValidationError("Missing token in request body")
        return token

    @staticmethod/
    def _assert_authenticated_revocation_caller(event: dict) -> None:
        principal = event.get("requestContext", {}).get("authorizer", {}).get("principalId")
        if not principal:
            raise AuthenticationError("Revocation caller must be authenticated")
