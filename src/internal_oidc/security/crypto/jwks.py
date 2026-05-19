from typing import Any


def build_jwk_from_rsa_numbers(*, kid: str, n: int, e: int, alg: str = "RS256") -> dict[str, Any]:
    """Convert RSA public numbers into a JWK document.

    This is intentionally simple. Production code should normalize key encoding carefully.
    """
    import base64

    def b64url_uint(value: int) -> str:
        raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    return {
        "kty": "RSA",
        "use": "sig",
        "kid": kid,
        "alg": alg,
        "n": b64url_uint(n),
        "e": b64url_uint(e),
    }
