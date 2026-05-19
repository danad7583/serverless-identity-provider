from internal_oidc.core.errors import UnsupportedOperationError


def handle(event: dict) -> dict:
    raise UnsupportedOperationError(
        "Authorize flow is not implemented in this starter package. Implement client registry, exact redirect validation, state, and PKCE first."
    )
