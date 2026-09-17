"""Harness SDK exception hierarchy.

All exceptions inherit from HarnessSdkError. API errors expose status_code,
body, and headers without exposing API keys.
"""


class HarnessSdkError(Exception):
    """Base exception for all Harness SDK errors.

    All SDK exceptions inherit from this class, allowing callers to catch
    any Harness-specific error with a single except clause.
    """

    pass


class ScopeNotSetError(HarnessSdkError):
    """Raised when required scope fields are not set or provided.

    Indicates that required scope fields (account_id, org, project, etc.)
    are missing and cannot be resolved from defaults.
    """

    pass


class ApiError(HarnessSdkError):
    """Raised for non-2xx API responses (other than 401/403).

    Exposes HTTP status code, response body, and headers without revealing
    API keys or other secrets.

    Attributes:
        status_code: HTTP status code from API response.
        body: Response body as string.
        headers: Response headers dictionary.
        payload: Parsed JSON payload (if response was JSON), else None.
    """

    def __init__(
        self, status_code: int, body: str, headers: dict[str, str], payload: dict | None = None
    ) -> None:
        """Initialize ApiError.

        Args:
            status_code: HTTP status code from failed request.
            body: Raw response body as string.
            headers: Response headers as dictionary.
            payload: Parsed JSON payload from response (optional).
        """
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.payload = payload
        super().__init__(
            f"API error: status_code={status_code}, body_length={len(body)}, payload={payload}"
        )


class AuthError(ApiError):
    """Raised for 401 (Unauthorized) and 403 (Forbidden) responses.

    Indicates authentication or authorization failure. Typically means
    the API key is missing, invalid, expired, or lacks required permissions.
    """

    pass
