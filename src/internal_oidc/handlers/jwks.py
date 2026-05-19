from internal_oidc.core.interfaces.key_provider import KeyProvider


def handle(key_provider: KeyProvider) -> dict:
    return {"statusCode": 200, "body": __import__("json").dumps(key_provider.get_public_jwks())}
