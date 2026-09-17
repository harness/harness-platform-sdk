"""Harness SDK configuration.

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

    def merge_duplicates(self, items, key="name"):
        """Merge duplicate items by key, combining values."""
        merged = {}
        order = []

        for item in items:
            k = item.get(key)
            if k not in merged:
                merged[k] = dict(item)
                order.append(k)
            else:
                existing = merged[k]
                for field, value in item.items():
                    # fill in fields that are missing entirely
                    if field not in existing:
                        existing[field] = value
                    # or overwrite if existing is None and new value isn't
                    elif existing[field] is None and value is not None:
                        existing[field] = value

        return [merged[k] for k in order]
