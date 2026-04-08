"""
Secrets API client for Harness SDK.

Provides CRUD operations for secret resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.secrets import (
    SecretCreateRequest,
    SecretResponse,
    SecretUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class SecretsApi:
    """API client for secret operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize SecretsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[SecretResponse]:
        """List secrets in the specified scope.

        Args:
            scope: Scope containing org and project. Account is required.
            **kwargs: Additional query parameters (e.g., searchTerm, type).

        Yields:
            SecretResponse: Individual secret items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url("/ng/api/v2/secrets", resolved)
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=SecretResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
            unwrap_field="secret",  # API wraps each item in a "secret" field
        )

    def get(
        self, identifier: str, scope: Scope | None = None
    ) -> SecretResponse:
        """Get a single secret by identifier.

        Args:
            identifier: Secret identifier.
            scope: Scope containing org and project (optional).

        Returns:
            SecretResponse: The requested secret.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/v2/secrets/{identifier}",
            resolved,
            identifier=identifier,
        )
        return self._client._get(
            url, params=None, body=None, response_model=SecretResponse
        )

    def create(
        self, body: SecretCreateRequest, scope: Scope | None = None
    ) -> SecretResponse:
        """Create a new secret.

        Args:
            body: Secret creation request with required fields.
            scope: Scope containing org and project (optional).

        Returns:
            SecretResponse: The created secret.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url("/ng/api/v2/secrets", resolved)
        return self._client._post(
            url, params=None, body=body, response_model=SecretResponse
        )

    def update(
        self,
        identifier: str,
        body: SecretUpdateRequest,
        scope: Scope | None = None,
    ) -> SecretResponse:
        """Update an existing secret.

        Args:
            identifier: Secret identifier.
            body: Secret update request with updated fields.
            scope: Scope containing org and project (optional).

        Returns:
            SecretResponse: The updated secret.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/v2/secrets/{identifier}",
            resolved,
            identifier=identifier,
        )
        return self._client._put(
            url, params=None, body=body, response_model=SecretResponse
        )

    def delete(
        self, identifier: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a secret.

        Args:
            identifier: Secret identifier.
            scope: Scope containing org and project (optional).

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/v2/secrets/{identifier}",
            resolved,
            identifier=identifier,
        )
        return self._client._delete(url, params=None, body=None, response_model=None)
