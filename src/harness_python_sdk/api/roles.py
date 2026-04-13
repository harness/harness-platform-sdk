"""
Roles API client for Harness SDK.

Provides CRUD operations for role resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.roles import (
    RoleCreateRequest,
    RoleResponse,
    RoleUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class RolesApi:
    """API client for role operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize RolesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[RoleResponse]:
        """List roles in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            RoleResponse: Individual role items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/roles",
            resolved,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=RoleResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
        )

    def get(self, role_id: str, scope: Scope | None = None) -> RoleResponse:
        """Get a single role by ID.

        Args:
            role_id: Role identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            RoleResponse: The requested role.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/roles/{role_id}",
            resolved,
            role_id=role_id,
        )
        return self._client._get(
            url, params=None, response_model=RoleResponse
        )

    def create(
        self, body: RoleCreateRequest, scope: Scope | None = None
    ) -> RoleResponse:
        """Create a new role.

        Args:
            body: Role creation request with required fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            RoleResponse: The created role.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/roles",
            resolved,
        )
        return self._client._post(
            url, params=None, body=body, response_model=RoleResponse
        )

    def update(
        self,
        role_id: str,
        body: RoleUpdateRequest,
        scope: Scope | None = None,
    ) -> RoleResponse:
        """Update an existing role.

        Args:
            role_id: Role identifier.
            body: Role update request with updated fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            RoleResponse: The updated role.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/roles/{role_id}",
            resolved,
            role_id=role_id,
        )
        return self._client._put(
            url, params=None, body=body, response_model=RoleResponse
        )

    def delete(
        self, role_id: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a role.

        Args:
            role_id: Role identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/roles/{role_id}",
            resolved,
            role_id=role_id,
        )
        return self._client._delete(url, params=None, response_model=None)
