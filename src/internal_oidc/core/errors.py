class OIDCError(Exception):
    """Base application error."""


class ConfigurationError(OIDCError):
    """Raised when required configuration is missing or invalid."""


class ValidationError(OIDCError):
    """Raised when a token or request fails validation."""


class AuthenticationError(OIDCError):
    """Raised when authentication fails."""


class AuthorizationError(OIDCError):
    """Raised when a caller is not authorized."""


class RevokedTokenError(ValidationError):
    """Raised when a token has been revoked."""


class UnsupportedOperationError(OIDCError):
    """Raised when an endpoint is not implemented yet."""
