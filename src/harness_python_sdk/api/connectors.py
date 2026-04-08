"""
Connectors API client for Harness SDK.

Provides CRUD operations for connector resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.connectors import (
    ConnectorCreateRequest,
    ConnectorResponse,
    ConnectorUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class ConnectorsApi:
    """API client for connector operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ConnectorsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[ConnectorResponse]:
        """List connectors in the specified scope.

        Args:
            scope: Scope containing org and project. Account is required.
            **kwargs: Additional query parameters (e.g., searchTerm, type).

        Yields:
            ConnectorResponse: Individual connector items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url("/ng/api/connectors", resolved)
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=ConnectorResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
            unwrap_field="connector",  # API wraps each item in a "connector" field
        )

    def get(
        self, identifier: str, scope: Scope | None = None
    ) -> ConnectorResponse:
        """Get a single connector by identifier.

        Args:
            identifier: Connector identifier.
            scope: Scope containing org and project (optional).

        Returns:
            ConnectorResponse: The requested connector.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/connectors/{identifier}",
            resolved,
            identifier=identifier,
        )
        return self._client._get(
            url, params=None, body=None, response_model=ConnectorResponse
        )

    def create(
        self, body: ConnectorCreateRequest, scope: Scope | None = None
    ) -> ConnectorResponse:
        """Create a new connector.

        Args:
            body: Connector creation request with required fields.
            scope: Scope containing org and project (optional).

        Returns:
            ConnectorResponse: The created connector.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url("/ng/api/connectors", resolved)
        return self._client._post(
            url, params=None, body=body, response_model=ConnectorResponse
        )

    def update(
        self,
        identifier: str,
        body: ConnectorUpdateRequest,
        scope: Scope | None = None,
    ) -> ConnectorResponse:
        """Update an existing connector.

        Note: API does not support PATCH; implementation uses DELETE + CREATE pattern.

        Args:
            identifier: Connector identifier.
            body: Connector update request with updated fields.
            scope: Scope containing org and project (optional).

        Returns:
            ConnectorResponse: The updated connector.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/connectors/{identifier}",
            resolved,
            identifier=identifier,
        )
        return self._client._put(
            url, params=None, body=body, response_model=ConnectorResponse
        )

    def delete(
        self, identifier: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a connector.

        Args:
            identifier: Connector identifier.
            scope: Scope containing org and project (optional).

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/connectors/{identifier}",
            resolved,
            identifier=identifier,
        )
        return self._client._delete(url, params=None, body=None, response_model=None)
