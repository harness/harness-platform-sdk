"""
Role Assignments API client for Harness SDK.

Provides CRUD operations for role assignment resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.role_assignments import (
    RoleAssignmentCreateRequest,
    RoleAssignmentResponse,
    RoleAssignmentUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class RoleAssignmentsApi:
    """API client for role assignment operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize RoleAssignmentsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def _unwrap_response(self, raw_data: dict) -> dict:
        """Unwrap role assignment response envelope.

        API returns: {"role-assignment": {...}, "created": ..., "updated": ..., "harness_managed": ...}
        Merge wrapper metadata with role assignment data for model construction.

        Args:
            raw_data: The "data" field from API response.

        Returns:
            Merged dict with role assignment fields + metadata.
        """
        role_assignment = raw_data.get("role-assignment", {})
        # Merge role assignment fields with sibling metadata
        return {**role_assignment, **{k: v for k, v in raw_data.items() if k != "role-assignment"}}

    def list(
        self, scope: Scope | None = None, **kwargs
    ) -> Iterator[RoleAssignmentResponse]:
        """List role assignments in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            RoleAssignmentResponse: Individual role assignment items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/role-assignments",
            resolved,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=RoleAssignmentResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
            unwrap_field="role-assignment",
        )

    def get(
        self, role_assignment_id: str, scope: Scope | None = None
    ) -> RoleAssignmentResponse:
        """Get a single role assignment by ID.

        Args:
            role_assignment_id: Role assignment identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            RoleAssignmentResponse: The requested role assignment.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/role-assignments/{role_assignment_id}",
            resolved,
            role_assignment_id=role_assignment_id,
        )
        response = self._client._get(url, params=None, response_model=None)
        # Unwrap envelope: response["data"] contains {"role-assignment": {...}, metadata...}
        unwrapped = self._unwrap_response(response.get("data", {}))
        return RoleAssignmentResponse(**unwrapped)

    def create(
        self, body: RoleAssignmentCreateRequest, scope: Scope | None = None
    ) -> RoleAssignmentResponse:
        """Create a new role assignment.

        Args:
            body: Role assignment creation request with required fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            RoleAssignmentResponse: The created role assignment.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/role-assignments",
            resolved,
        )
        # Wrap request body: {"role-assignment": {...}}
        wrapped_body = {"role-assignment": body.model_dump(exclude_none=True, by_alias=True)}
        response = self._client._post(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return RoleAssignmentResponse(**unwrapped)

    def update(
        self,
        role_assignment_id: str,
        body: RoleAssignmentUpdateRequest,
        scope: Scope | None = None,
    ) -> RoleAssignmentResponse:
        """Update an existing role assignment.

        Args:
            role_assignment_id: Role assignment identifier.
            body: Role assignment update request with updated fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            RoleAssignmentResponse: The updated role assignment.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/role-assignments/{role_assignment_id}",
            resolved,
            role_assignment_id=role_assignment_id,
        )
        # Wrap request body: {"role-assignment": {...}}
        wrapped_body = {"role-assignment": body.model_dump(exclude_none=True, by_alias=True)}
        response = self._client._put(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return RoleAssignmentResponse(**unwrapped)

    def delete(
        self, role_assignment_id: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a role assignment.

        Args:
            role_assignment_id: Role assignment identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/role-assignments/{role_assignment_id}",
            resolved,
            role_assignment_id=role_assignment_id,
        )
        return self._client._delete(url, params=None, response_model=None)
