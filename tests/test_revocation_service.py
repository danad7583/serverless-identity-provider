from internal_oidc.core.models.token import TokenClaims
from internal_oidc.core.services.revocation_service import RevocationService
from internal_oidc.stores.memory.revocation_store import MemoryRevocationStore


def test_revoke_and_check() -> None:
    store = MemoryRevocationStore()
    service = RevocationService(store)
    claims = TokenClaims(
        iss="https://issuer.example",
        sub="user-1",
        aud="api://test",
        exp=4102444800,
        iat=1700000000,
        jti="test-jti-123",
    )
    service.revoke(claims)
    try:
        service.assert_not_revoked(claims)
        raise AssertionError("expected token to be revoked")
    except Exception as exc:
        assert exc.__class__.__name__ == "RevokedTokenError"
