"""
Services API client for Harness SDK.

Provides CRUD operations for service resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.services import (
    ServiceCreateRequest,
    ServiceResponse,
    ServiceUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class ServicesApi:
    """API client for service operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize ServicesApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def _unwrap_response(self, raw_data: dict) -> dict:
        """Unwrap service response envelope.

        API returns: {"service": {...}, "created": ..., "updated": ...}
        Merge wrapper metadata with service data for model construction.

        Args:
            raw_data: The "data" field from API response.

        Returns:
            Merged dict with service fields + metadata.
        """
        service = raw_data.get("service", {})
        # Merge service fields with sibling metadata
        return {**service, **{k: v for k, v in raw_data.items() if k != "service"}}

    def list(self, scope: Scope | None = None, **kwargs) -> Iterator[ServiceResponse]:
        """List services in the specified project.

        Args:
            scope: Scope containing org and project. If None, uses client default scope.
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            ServiceResponse: Individual service items across all pages.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/services",
            resolved,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=ServiceResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=resolved,
        )

    def get(self, service_id: str, scope: Scope | None = None) -> ServiceResponse:
        """Get a single service by ID.

        Args:
            service_id: Service identifier.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            ServiceResponse: The requested service.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/services/{service_id}",
            resolved,
            service_id=service_id,
        )
        response = self._client._get(url, params=None, response_model=None)
        # Unwrap envelope: response["data"] contains {"service": {...}, metadata...}
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ServiceResponse(**unwrapped)

    def create(
        self, body: ServiceCreateRequest, scope: Scope | None = None
    ) -> ServiceResponse:
        """Create a new service.

        Args:
            body: Service creation request with required fields.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            ServiceResponse: The created service.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/services",
            resolved,
        )
        # Wrap request body: {"service": {...}}
        wrapped_body = {"service": body.model_dump(exclude_none=True, by_alias=True)}
        response = self._client._post(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ServiceResponse(**unwrapped)

    def update(
        self,
        service_id: str,
        body: ServiceUpdateRequest,
        scope: Scope | None = None,
    ) -> ServiceResponse:
        """Update an existing service.

        Args:
            service_id: Service identifier.
            body: Service update request with updated fields.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            ServiceResponse: The updated service.

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/services/{service_id}",
            resolved,
            service_id=service_id,
        )
        # Wrap request body: {"service": {...}}
        wrapped_body = {"service": body.model_dump(exclude_none=True, by_alias=True)}
        response = self._client._put(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return ServiceResponse(**unwrapped)

    def delete(
        self, service_id: str, scope: Scope | None = None
    ) -> dict | None:
        """Delete a service.

        Args:
            service_id: Service identifier.
            scope: Scope containing org and project. If None, uses client default scope.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ScopeNotSetError: If scope cannot be resolved.
            ApiError: For non-2xx responses.
        """
        resolved = self._client._resolve_scope(scope)
        url = self._client._build_url(
            "/v1/orgs/{org}/projects/{project}/services/{service_id}",
            resolved,
            service_id=service_id,
        )
        return self._client._delete(url, params=None, response_model=None)
