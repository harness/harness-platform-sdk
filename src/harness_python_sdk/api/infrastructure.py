"""
Infrastructure API client for Harness SDK.

Provides CRUD operations for infrastructure resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.infrastructure import (
    InfrastructureCreateRequest,
    InfrastructureResponse,
    InfrastructureUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class InfrastructureApi:
    """API client for infrastructure operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize InfrastructureApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def list(
        self, scope: Scope | None = None, **kwargs
    ) -> Iterator[InfrastructureResponse]:
        """List infrastructures in the specified scope.

        Args:
            scope: Scope containing org and project. Account is required.
            **kwargs: Additional query parameters (e.g., searchTerm, deploymentType).

        Yields:
            InfrastructureResponse: Individual infrastructure items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url("/ng/api/infrastructures", resolved)
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=InfrastructureResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
            unwrap_field="infrastructure",  # API wraps each item in an "infrastructure" field
        )

    def get(
        self, infra_identifier: str, scope: Scope | None = None
    ) -> InfrastructureResponse:
        """Get a single infrastructure by identifier.

        Args:
            infra_identifier: Infrastructure identifier.
            scope: Scope containing org and project (optional).

        Returns:
            InfrastructureResponse: The requested infrastructure.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/infrastructures/{infraIdentifier}",
            resolved,
            infraIdentifier=infra_identifier,
        )
        return self._client._get(
            url, params=None, body=None, response_model=InfrastructureResponse
        )

    def create(
        self, body: InfrastructureCreateRequest, scope: Scope | None = None
    ) -> InfrastructureResponse:
        """Create a new infrastructure.

        Args:
            body: Infrastructure creation request with required fields.
            scope: Scope containing org and project (optional).

        Returns:
            InfrastructureResponse: The created infrastructure.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url("/ng/api/infrastructures", resolved)
        return self._client._post(
            url, params=None, body=body, response_model=InfrastructureResponse
        )

    def update(
        self,
        infra_identifier: str,
        body: InfrastructureUpdateRequest,
        scope: Scope | None = None,
    ) -> InfrastructureResponse:
        """Update an existing infrastructure.

        Note: API does not support PATCH; implementation uses DELETE + CREATE pattern.

        Args:
            infra_identifier: Infrastructure identifier.
            body: Infrastructure update request with updated fields.
            scope: Scope containing org and project (optional).

        Returns:
            InfrastructureResponse: The updated infrastructure.

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/infrastructures/{infraIdentifier}",
            resolved,
            infraIdentifier=infra_identifier,
        )
        return self._client._put(
            url, params=None, body=body, response_model=InfrastructureResponse
        )

    def delete(
        self, infra_identifier: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete an infrastructure.

        Args:
            infra_identifier: Infrastructure identifier.
            scope: Scope containing org and project (optional).

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If account scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/ng/api/infrastructures/{infraIdentifier}",
            resolved,
            infraIdentifier=infra_identifier,
        )
        return self._client._delete(url, params=None, body=None, response_model=None)
