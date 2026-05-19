from internal_oidc.core.errors import UnsupportedOperationError


def handle(event: dict) -> dict:
    raise UnsupportedOperationError(
        "UserInfo is not implemented in this starter package. Implement access-token validation policy and scope checks first."
    )
