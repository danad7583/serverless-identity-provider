from internal_oidc.core.errors import UnsupportedOperationError


def handle(event: dict) -> dict:
    raise UnsupportedOperationError(
        "Introspection is not implemented in this starter package. Implement authenticated caller policy and token-type rules first."
    )
