from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TokenClaims:
    iss: str
    sub: str
    aud: str | list[str]
    exp: int
    iat: int
    jti: str
    token_use: str | None = None
    client_id: str | None = None
    scope: str | None = None
    raw_claims: dict[str, Any] | None = None
