import os

import boto3

from internal_oidc.core.config import OIDCConfig
from internal_oidc.handlers import discovery, health, jwks
from internal_oidc.providers.aws.kms_key_provider import KMSKeyProvider


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
    method = (event or {}).get("httpMethod", "GET").upper()
    path = (event or {}).get("path", "")

    if method == "GET" and path == "/health":
        return health.handle()

    config = _build_config()

    if method == "GET" and path == "/.well-known/openid-configuration":
        return discovery.handle(config)

    if method == "GET" and path == "/jwks":
        secret_arn = os.environ["KEY_PROVIDER_SECRET_ARN"]
        secrets_client = boto3.client("secretsmanager")
        kms_client = boto3.client("kms")
        key_provider = KMSKeyProvider(secret_arn, secrets_client, kms_client)
        return jwks.handle(key_provider)

    return {"statusCode": 404, "body": '{"error":"not_found"}'}
