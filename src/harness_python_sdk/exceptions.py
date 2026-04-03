"""
Harness SDK exception hierarchy.

All exceptions inherit from HarnessSdkError. API errors expose status_code,
body, and headers without exposing API keys.
"""


class HarnessSdkError(Exception):
    """Base exception for all Harness SDK errors."""

    pass


class ScopeNotSetError(HarnessSdkError):
    """Raised when required scope fields are not set or provided."""

    pass


class ApiError(HarnessSdkError):
    """Raised for non-2xx API responses (other than 401/403)."""

    def __init__(self, status_code: int, body: str, headers: dict):
        self.status_code = status_code
        self.body = body
        self.headers = headers
        super().__init__(
            f"API error: status_code={status_code}, body_length={len(body)}"
        )


class AuthError(ApiError):
    """Raised for 401 (Unauthorized) and 403 (Forbidden) responses."""

    pass
