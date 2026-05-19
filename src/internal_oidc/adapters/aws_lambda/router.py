import json
from typing import Callable

from internal_oidc.core.errors import OIDCError


class LambdaRouter:
    def __init__(self) -> None:
        self._routes: dict[tuple[str, str], Callable[[dict], dict]] = {}

    def register(self, method: str, path: str, handler: Callable[[dict], dict]) -> None:
        self._routes[(method.upper(), path)] = handler

    def handle(self, event: dict, context: dict | None = None) -> dict:
        route_key = (event.get("httpMethod", "GET").upper(), event.get("path", "/"))
        handler = self._routes.get(route_key)
        if handler is None:
            return {"statusCode": 404, "body": json.dumps({"error": "not_found"})}
        try:
            return handler(event)
        except OIDCError as exc:
            return {"statusCode": 400, "body": json.dumps({"error": exc.__class__.__name__, "message": str(exc)})}
        except Exception:
            return {"statusCode": 500, "body": json.dumps({"error": "internal_server_error"})}
