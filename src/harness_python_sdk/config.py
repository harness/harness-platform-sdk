"""
Harness SDK configuration.

HarnessConfig holds all configuration needed for the SDK client.
API keys are never exposed in __repr__ or error messages.
"""

from pydantic import BaseModel, ConfigDict


class HarnessConfig(BaseModel):
    """Configuration for HarnessClient.

    Attributes:
        api_key: Harness API key for authentication.
        account_id: Harness account identifier.
        base_url: Base URL for Harness API (default: https://app.harness.io).
        timeout: Request timeout in seconds (default: 30.0).
        max_retries: Maximum number of connection retries (default: 3).
        retry_status_codes: HTTP status codes to retry on (default: [429, 503]).
        retry_enabled: Whether to retry failed requests (default: True).
        verify_ssl: Whether to verify SSL certificates (default: True).
    """

    api_key: str
    account_id: str
    base_url: str = "https://app.harness.io"
    timeout: float = 30.0
    max_retries: int = 3
    retry_status_codes: list[int] = [429, 503]
    retry_enabled: bool = True
    verify_ssl: bool = True

    model_config = ConfigDict(frozen=False)

    def __repr__(self) -> str:
        """Return representation with redacted API key."""
        return (
            f"HarnessConfig(api_key='***', account_id={self.account_id!r}, "
            f"base_url={self.base_url!r}, timeout={self.timeout}, "
            f"max_retries={self.max_retries}, retry_enabled={self.retry_enabled})"
        )
