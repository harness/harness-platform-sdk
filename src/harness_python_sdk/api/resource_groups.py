"""
Resource Groups API client for Harness SDK.

Provides CRUD operations for resource group resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.resource_groups import (
    ResourceGroupCreateRequest,
    ResourceGroupResponse,
    ResourceGroupUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class ResourceGroupsApi:
    """API client for resource group operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ResourceGroupsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def _unwrap_response(self, raw_data: dict) -> dict:
        """Unwrap resource group response envelope.

        API returns: {"resourceGroup": {...}, "createdAt": ..., "lastModifiedAt": ..., "harnessManaged": ...}
        Merge wrapper metadata with resource group data for model construction.

        Args:
            raw_data: The "data" field from API response.

        Returns:
            Merged dict with resource group fields + metadata.
        """
        resource_group = raw_data.get("resourceGroup", {})
        # Merge resource group fields with sibling metadata
        return {**resource_group, **{k: v for k, v in raw_data.items() if k != "resourceGroup"}}

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[ResourceGroupResponse]:
        """List resource groups in the specified organization.

        Args:
            scope: Scope containing org. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            ResourceGroupResponse: Individual resource group items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/resource-groups",
            resolved,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=ResourceGroupResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
            unwrap_field="resourceGroup",
        )

    def get(
        self, resource_group_id: str, scope: Scope | None = None
    ) -> ResourceGroupResponse:
        """Get a single resource group by ID.

        Args:
            resource_group_id: Resource group identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ResourceGroupResponse: The requested resource group.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/resource-groups/{resource_group_id}",
            resolved,
            resource_group_id=resource_group_id,
        )
        response = self._client._get(url, params=None, response_model=None)
        # Unwrap envelope: response["data"] contains {"resourceGroup": {...}, metadata...}
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ResourceGroupResponse(**unwrapped)

    def create(
        self, body: ResourceGroupCreateRequest, scope: Scope | None = None
    ) -> ResourceGroupResponse:
        """Create a new resource group.

        Args:
            body: Resource group creation request with required fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ResourceGroupResponse: The created resource group.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/resource-groups",
            resolved,
        )
        # Wrap request body: {"resourceGroup": {...}}
        wrapped_body = {"resourceGroup": body.model_dump(exclude_none=True, by_alias=True)}
        response = self._client._post(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ResourceGroupResponse(**unwrapped)

    def update(
        self,
        resource_group_id: str,
        body: ResourceGroupUpdateRequest,
        scope: Scope | None = None,
    ) -> ResourceGroupResponse:
        """Update an existing resource group.

        Args:
            resource_group_id: Resource group identifier.
            body: Resource group update request with updated fields.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            ResourceGroupResponse: The updated resource group.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/resource-groups/{resource_group_id}",
            resolved,
            resource_group_id=resource_group_id,
        )
        # Wrap request body: {"resourceGroup": {...}}
        wrapped_body = {"resourceGroup": body.model_dump(exclude_none=True, by_alias=True)}
        response = self._client._put(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ResourceGroupResponse(**unwrapped)

    def delete(
        self, resource_group_id: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a resource group.

        Args:
            resource_group_id: Resource group identifier.
            scope: Scope containing org. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/resource-groups/{resource_group_id}",
            resolved,
            resource_group_id=resource_group_id,
        )
        return self._client._delete(url, params=None, response_model=None)
