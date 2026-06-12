import base64
import hashlib
import json
from typing import Any

from cryptography.hazmat.primitives import serialization

from internal_oidc.core.interfaces.key_provider import KeyProvider


def _b64url_uint(value: int) -> str:
    raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


class KMSKeyProvider(KeyProvider):
    """KMS-backed key provider.

    The secret contains provider config, not key material:

    {
      "provider": "aws:kms",
      "external_provider_enabled": "false",
      "kms_key_arn": "arn:aws:kms:..."
    }
    """

    def __init__(self, secret_id: str, secrets_client, kms_client) -> None:
        self._secret_id = secret_id
        self._secrets_client = secrets_client
        self._kms_client = kms_client
        self._config_cache: dict[str, Any] | None = None
        self._jwks_cache: dict[str, Any] | None = None

    def get_signing_key(self) -> Any:
        raise NotImplementedError("KMS-backed signing must use kms.sign; private key is not exportable")

    def get_public_jwks(self) -> dict:
        if self._jwks_cache is not None:
            return self._jwks_cache

        config = self._load_config()
        key_id = config["kms_key_arn"]

        response = self._kms_client.get_public_key(KeyId=key_id)
        der_public_key = response["PublicKey"]

        public_key = serialization.load_der_public_key(der_public_key)
        numbers = public_key.public_numbers()

        kid = self.get_active_kid()

        self._jwks_cache = {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": kid,
                    "alg": "RS256",
                    "n": _b64url_uint(numbers.n),
                    "e": _b64url_uint(numbers.e),
                }
            ]
        }
        return self._jwks_cache

    def get_active_kid(self) -> str:
        config = self._load_config()
        key_arn = config["kms_key_arn"]
        return hashlib.sha256(key_arn.encode("utf-8")).hexdigest()[:16]

    def _load_config(self) -> dict[str, Any]:
        if self._config_cache is None:
            response = self._secrets_client.get_secret_value(SecretId=self._secret_id)
            self._config_cache = json.loads(response["SecretString"])

            if self._config_cache.get("provider") != "aws:kms":
                raise ValueError("Unsupported key provider config; expected provider=aws:kms")

            if "kms_key_arn" not in self._config_cache:
                raise KeyError("kms_key_arn")

        return self._config_cache