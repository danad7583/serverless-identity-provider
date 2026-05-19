import json
import os

import boto3

from internal_oidc.core.config import OIDCConfig
from internal_oidc.core.services.revocation_service import RevocationService
from internal_oidc.handlers.revoke import RevokeHandler
from internal_oidc.providers.aws.secrets_manager_key_provider import SecretsManagerKeyProvider
from internal_oidc.security.claims.validator import ClaimsValidator
from internal_oidc.security.crypto.service import CryptoService
from internal_oidc.stores.dynamodb.revocation_store import DynamoDBRevocationStore


def _build_config() -> OIDCConfig:
    issuer = os.getenv("OIDC_ISSUER") or os.getenv("ISSUER_BASE_URL")
    audience = os.getenv("OIDC_AUDIENCE") or os.getenv("PROJECT_NAME") or "internal-issuer"
    if not issuer:
        raise RuntimeError("OIDC_ISSUER or ISSUER_BASE_URL must be set")
    return OIDCConfig(
        issuer=issuer,
        audience=audience,
        jwks_cache_ttl_seconds=int(os.getenv("JWKS_CACHE_TTL_SECONDS", "300")),
        revocation_namespace=os.getenv("REVOCATION_NAMESPACE", "revoke:jti"),
        strict_fail_closed_on_revocation_error=os.getenv(
            "STRICT_FAIL_CLOSED_ON_REVOCATION_ERROR", "true"
        ).lower() == "true",
    )


def lambda_handler(event: dict, context: dict | None = None) -> dict:
    event = event or {}
    if isinstance(event.get("body"), str):
        try:
            event["json"] = json.loads(event["body"])
        except json.JSONDecodeError:
            event["json"] = {}

    config = _build_config()
    secrets_client = boto3.client("secretsmanager")
    dynamodb_resource = boto3.resource("dynamodb")

    key_provider = SecretsManagerKeyProvider(os.environ["KEY_PROVIDER_SECRET_ARN"], secrets_client)
    crypto_service = CryptoService(config, key_provider)
    claims_validator = ClaimsValidator(config)
    revocation_store = DynamoDBRevocationStore(os.environ["REVOCATION_TABLE_NAME"], dynamodb_resource)
    revocation_service = RevocationService(revocation_store)
    handler = RevokeHandler(crypto_service, claims_validator, revocation_service)
    return handler.handle(event)
