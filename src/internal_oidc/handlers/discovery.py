from internal_oidc.core.config import OIDCConfig


def handle(config: OIDCConfig) -> dict:
    discovery = {
        "issuer": config.issuer,
        "jwks_uri": f"{config.issuer}/jwks",
        "authorization_endpoint": f"{config.issuer}/authorize",
        "token_endpoint": f"{config.issuer}/token",
        "userinfo_endpoint": f"{config.issuer}/userinfo",
        "revocation_endpoint": f"{config.issuer}/revoke",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "client_credentials"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"],
    }
    return {"statusCode": 200, "body": __import__("json").dumps(discovery)}
