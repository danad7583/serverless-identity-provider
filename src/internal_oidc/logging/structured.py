import json
from typing import Any

from internal_oidc.core.interfaces.audit_logger import AuditLogger


class JsonAuditLogger(AuditLogger):
    def log(self, event_type: str, details: dict[str, Any]) -> None:
        payload = {"event_type": event_type, **details}
        print(json.dumps(payload, sort_keys=True))
