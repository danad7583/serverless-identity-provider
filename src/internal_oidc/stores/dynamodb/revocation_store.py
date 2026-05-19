from __future__ import annotations

from internal_oidc.core.interfaces.revocation_store import RevocationStore


class DynamoDBRevocationStore(RevocationStore):
    """AWS adapter for revocation storage.

    Table shape:
    - PK: jti (string)
    - expires_at: number (TTL attribute)
    """

    def __init__(self, table_name: str, dynamodb_resource) -> None:
        self._table = dynamodb_resource.Table(table_name)

    def revoke(self, jti: str, expires_at_epoch: int) -> None:
        self._table.put_item(Item={"jti": jti, "expires_at": expires_at_epoch})

    def is_revoked(self, jti: str) -> bool:
        response = self._table.get_item(Key={"jti": jti}, ConsistentRead=True)
        return "Item" in response
