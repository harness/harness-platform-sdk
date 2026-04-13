"""
Organizations API client for Harness SDK.

Provides CRUD operations for organization resources.
"""

from __future__ import annotations

from collections.abc import Iterator

from harness_python_sdk.client import HarnessClient
from harness_python_sdk.models.organizations import (
    OrganizationCreateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest,
)
from harness_python_sdk.pagination import PaginationStyle
from harness_python_sdk.scope import Scope


class OrganizationsApi:
    """API client for organization operations."""

    def __init__(self, client: HarnessClient) -> None:
        """Initialize OrganizationsApi with HarnessClient.

        Args:
            client: HarnessClient instance for making requests.
        """
        self._client = client

    def _unwrap_response(self, raw_data: dict) -> dict:
        """Unwrap organization response envelope.

        API returns: {"organization": {...}, "createdAt": ..., "lastModifiedAt": ..., "harnessManaged": ...}
        Merge wrapper metadata with organization data for model construction.

        Args:
            raw_data: The "data" field from API response.

        Returns:
            Merged dict with organization fields + metadata.
        """
        org = raw_data.get("organization", {})
        # Merge organization fields with sibling metadata
        return {**org, **{k: v for k, v in raw_data.items() if k != "organization"}}

    def list(self, **kwargs) -> Iterator[OrganizationResponse]:
        """List organizations in the account.

        Args:
            **kwargs: Additional query parameters (e.g., searchTerm).

        Yields:
            OrganizationResponse: Individual organization items across all pages.

        Raises:
            ApiError: For non-2xx responses.
        """
        # Organizations are account-scoped, no Scope needed
        url = self._client._build_url(
            "/ng/api/organizations",
            self._client._default_scope,
        )
        return self._client._paginate(
            url,
            params=kwargs,
            response_model=OrganizationResponse,
            pagination_style=PaginationStyle.OFFSET,  # per pagination_inventory.md
            scope=self._client._default_scope,
            unwrap_field="organization",
        )

    def get(self, identifier: str) -> OrganizationResponse:
        """Get a single organization by identifier.

        Args:
            identifier: Organization identifier.

        Returns:
            OrganizationResponse: The requested organization.

        Raises:
            ApiError: For non-2xx responses.
        """
        url = self._client._build_url(
            "/ng/api/organizations/{identifier}",
            self._client._default_scope,
            identifier=identifier,
        )
        response = self._client._get(url, params=None, response_model=None)
        # Unwrap envelope: response["data"] contains {"organization": {...}, metadata...}
        unwrapped = self._unwrap_response(response.get("data", {}))
        return OrganizationResponse(**unwrapped)

    def create(self, body: OrganizationCreateRequest) -> OrganizationResponse:
        """Create a new organization.

        Args:
            body: Organization creation request with required fields.

        Returns:
            OrganizationResponse: The created organization.

        Raises:
            ApiError: For non-2xx responses.
        """
        url = self._client._build_url(
            "/ng/api/organizations",
            self._client._default_scope,
        )
        # Wrap request body: {"organization": {...}}
        wrapped_body = {"organization": body.model_dump(exclude_none=True)}
        response = self._client._post(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return OrganizationResponse(**unwrapped)

    def update(
        self,
        identifier: str,
        body: OrganizationUpdateRequest,
    ) -> OrganizationResponse:
        """Update an existing organization.

        Args:
            identifier: Organization identifier.
            body: Organization update request with updated fields.

        Returns:
            OrganizationResponse: The updated organization.

        Raises:
            ApiError: For non-2xx responses.
        """
        url = self._client._build_url(
            "/ng/api/organizations/{identifier}",
            self._client._default_scope,
            identifier=identifier,
        )
        # Wrap request body: {"organization": {...}}
        wrapped_body = {"organization": body.model_dump(exclude_none=True)}
        response = self._client._put(
            url, params=None, body=wrapped_body, response_model=None
        )
        # Unwrap response envelope
        unwrapped = self._unwrap_response(response.get("data", {}))
        return OrganizationResponse(**unwrapped)

    def delete(self, identifier: str) -> dict | None:
        """Delete an organization.

        Args:
            identifier: Organization identifier.

        Returns:
            dict | None: Response data (typically empty for DELETE).

        Raises:
            ApiError: For non-2xx responses.
        """
        url = self._client._build_url(
            "/ng/api/organizations/{identifier}",
            self._client._default_scope,
            identifier=identifier,
        )
        return self._client._delete(url, params=None, response_model=None)
