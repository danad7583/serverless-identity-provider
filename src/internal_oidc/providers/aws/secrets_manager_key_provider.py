import json
from typing import Any

from internal_oidc.core.interfaces.key_provider import KeyProvider


class SecretsManagerKeyProvider(KeyProvider):
    """AWS adapter for retrieving signing material and JWKS documents.

    Expected secret layout:
    {
      "private_key_pem": "...",
      "public_jwks": {"keys": [...]},
      "active_kid": "kid-123"
    }
    """

    def __init__(self, secret_id: str, secrets_client) -> None:
        self._secret_id = secret_id
        self._client = secrets_client
        self._cache: dict[str, Any] | None = None

    def get_signing_key(self) -> Any:
        return self._load_secret()["private_key_pem"]

    def get_public_jwks(self) -> dict:
        return self._load_secret()["public_jwks"]

    def get_active_kid(self) -> str:
        return self._load_secret()["active_kid"]

    def _load_secret(self) -> dict[str, Any]:
        if self._cache is None:
            response = self._client.get_secret_value(SecretId=self._secret_id)
            self._cache = json.loads(response["SecretString"])
        return self._cache
