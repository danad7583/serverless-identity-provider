from internal_oidc.core.errors import UnsupportedOperationError


def handle(event: dict) -> dict:
    raise UnsupportedOperationError(
        "Token issuance is not implemented in this starter package. Implement client auth, claim policy, and mandatory jti issuance first."
    )
